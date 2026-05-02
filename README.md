# Serverless Inventory Management System
## Project Overview
This project is a fully automated, cloud-native inventory tracking system built entirely on AWS serverless architecture. It was designed to modernize inventory management by eliminating the need for physical servers, reducing maintenance overhead, and providing real-time, event-driven alerts.

Walkthrough: https://youtu.be/U2gIQxZ-yQ0

## Architecture & Data Flow
The system processes inventory data asynchronously using a decoupled microservices architecture:
1. **Amazon API Gateway:** Acts as the secure entry point, receiving JSON payloads (product details and Base64 encoded images) from a client (simulated via Postman).
2. **AWS Lambda:** The core processing engine. A custom Python script parses the payload, generates unique UUIDs, decodes the image, and routes the data to storage.
3. **Amazon S3:** Hosts the decoded `.jpg` product images and generates secure, static URLs for frontend display.
4. **Amazon DynamoDB:** A high-speed NoSQL database that stores the product metadata (ID, Name, Stock Count, and S3 Image URL).
5. **Amazon SQS:** An automated message queue that receives critical alerts from Lambda whenever an item's stock count drops below the defined threshold (10 items).

## Tech Stack
* **Compute/Networking:** AWS Lambda, Amazon API Gateway
* **Storage/Database:** Amazon S3, Amazon DynamoDB
* **Messaging:** Amazon SQS
* **Languages/Formats:** Python (boto3), JSON, Base64
* **Testing:** Postman
