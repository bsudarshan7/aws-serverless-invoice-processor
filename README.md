# AWS Serverless Invoice Processing System

## Overview

This project automates invoice processing using AWS serverless services.

When an invoice image is uploaded to Amazon S3, an AWS Lambda function is automatically triggered. The Lambda function uses Amazon Rekognition OCR to extract invoice information from the uploaded image and stores the extracted data in Amazon DynamoDB.

The system demonstrates an event-driven serverless architecture for document processing.

---

## AWS Services Used

* Amazon S3
* AWS Lambda
* Amazon Rekognition
* Amazon DynamoDB
* Amazon CloudWatch

---

## Architecture

Invoice Upload → Amazon S3 → AWS Lambda → Amazon Rekognition OCR → Amazon DynamoDB

---

## Features

* Automatic invoice processing
* Event-driven architecture
* OCR-based text extraction
* Invoice metadata storage
* Serverless implementation
* CloudWatch monitoring and logging

---

## Workflow

1. Upload an invoice image to Amazon S3.
2. S3 triggers the Lambda function automatically.
3. Lambda extracts text using Amazon Rekognition OCR.
4. Invoice details are processed.
5. Extracted information is stored in DynamoDB.

---

## Sample DynamoDB Record

```json
{
  "record_id": "e4c8bcb1-1234-5678-abcd-1234567890ab",
  "invoice_id": "INV001",
  "buyer_name": "ABC Enterprises",
  "total_amount": "2950.00",
  "image_name": "invoice1.jpg",
  "s3_uri": "s3://invoice-storage-project/invoice1.jpg",
  "processing_status": "SUCCESS"
}
```

---

## Project Structure

```text
aws-serverless-invoice-processor/
│
├── lambda/
│   └── invoice_processor.py
│
├── sample-invoices/
│
├── screenshots/
│
└── README.md
```

---

## Challenges Faced

* OCR output varies across invoice formats.
* Different invoices use different labels for invoice number and total amount.
* Data extraction required pattern matching and validation logic.
* Handling incomplete OCR results without stopping the workflow.

---

## Future Improvements

* Amazon Textract integration
* Invoice validation workflow
* Email notifications
* Analytics dashboard
* REST API for invoice retrieval

---

## Author

Sudarshan Birajdar
Computer Engineering Student
AWS Cloud Enthusiast
