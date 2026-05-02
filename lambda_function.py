import json
import boto3
import base64
import uuid

# Initialize AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

BUCKET_NAME = 'inventory-images-njy'
TABLE_NAME = 'Inventory'
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/102459949052/Low-Stock-Alert'

def lambda_handler(event, context):
    try:
        # 1.Parse incoming JSON payload from API Gateway
        body = json.loads(event['body'])
        product_id = str(uuid.uuid4()) 
        item_name = body['item_name']
        stock_count = int(body['stock_count'])
        
        # Decode image file sent from Postman
        image_bytes = base64.b64decode(body['image_file'])

        # 2.Upload the Image to S3
        s3_key = f"{product_id}.jpg"
        s3.put_object(
            Bucket=BUCKET_NAME, 
            Key=s3_key, 
            Body=image_bytes, 
            ContentType='image/jpeg'
        )
        s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

        # 3.Write Metadata to DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                'ProductID': product_id,
                'ItemName': item_name,
                'StockCount': stock_count,
                'ImageURL': s3_url
            }
        )

        # 4.Check Stock and Alert via SQS
        if stock_count < 10:
            alert_message = f"ALERT: Stock for {item_name} is critically low ({stock_count} remaining)."
            sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=alert_message)

        # 5.Return Success to API Gateway
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Inventory successfully updated!', 
                's3_url': s3_url
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }