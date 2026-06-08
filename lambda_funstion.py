import boto3
import re
import uuid
from urllib.parse import unquote_plus
from datetime import datetime

rekognition = boto3.client("rekognition")
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("InvoiceDataV2")


def lambda_handler(event, context):

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = unquote_plus(
        event["Records"][0]["s3"]["object"]["key"]
    )

    print("Bucket:", bucket)
    print("Key:", key)

    s3_uri = f"s3://{bucket}/{key}"

    response = rekognition.detect_text(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key
            }
        }
    )

    lines = []

    for item in response["TextDetections"]:
        if item["Type"] == "LINE":
            lines.append(item["DetectedText"])

    print("===== OCR OUTPUT =====")

    for line in lines:
        print(line)

    print("======================")

    full_text = "\n".join(lines)

    # --------------------
    # Record ID
    # --------------------

    record_id = str(uuid.uuid4())

    # --------------------
    # Invoice Number
    # --------------------

    invoice_id = key

    invoice_patterns = [
        r'INV[-]?\d+',
        r'Invoice\s*No\.?\s*:?\s*([A-Za-z0-9\/\-]+)'
    ]

    for pattern in invoice_patterns:

        match = re.search(
            pattern,
            full_text,
            re.IGNORECASE
        )

        if match:

            if match.groups():
                invoice_id = match.group(1)
            else:
                invoice_id = match.group(0)

            break

    # --------------------
    # Buyer Name
    # --------------------

    buyer_name = "UNKNOWN"

    buyer_keywords = [
        "buyer name",
        "bill to",
        "invoice to",
        "customer",
        "customer detail",
        "customer details",
        "client",
        "m/s",
        "ship to"
    ]

    for i, line in enumerate(lines):

        lower_line = line.lower()

        for keyword in buyer_keywords:

            if keyword in lower_line:

                if ":" in line:

                    value = line.split(":")[-1].strip()

                    if len(value) > 2:
                        buyer_name = value

                elif i + 1 < len(lines):

                    candidate = lines[i + 1].strip()

                    if len(candidate) > 2:
                        buyer_name = candidate

                break

    # --------------------
    # Total Amount
    # --------------------

    total_amount = "UNKNOWN"

    amounts = []

    amount_pattern = r'[\£₹$]?\s?[\d,]+(?:\.\d{2})?'

    matches = re.findall(
        amount_pattern,
        full_text
    )

    for value in matches:

        cleaned = (
            value.replace("₹", "")
                 .replace("$", "")
                 .replace("£", "")
                 .replace(",", "")
                 .strip()
        )

        try:
            amounts.append(float(cleaned))
        except:
            pass

    if amounts:
        total_amount = str(max(amounts))

    # --------------------
    # Status
    # --------------------

    status = "SUCCESS"

    if buyer_name == "UNKNOWN":
        status = "PARTIAL"

    # --------------------
    # Save
    # --------------------

    table.put_item(
        Item={
            "record_id": record_id,
            "invoice_id": invoice_id,
            "buyer_name": buyer_name,
            "total_amount": total_amount,
            "image_name": key,
            "bucket_name": bucket,
            "s3_uri": s3_uri,
            "processing_status": status,
            "upload_time": datetime.utcnow().isoformat()
        }
    )

    return {
        "statusCode": 200,
        "record_id": record_id,
        "invoice_id": invoice_id,
        "buyer_name": buyer_name,
        "total_amount": total_amount,
        "processing_status": status
    }
