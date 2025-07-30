import json
import boto3
import os
import uuid
from datetime import datetime

# Initialize AWS clients outside the handler for better performance 
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")

    # Retrieve environment variables
    dynamodb_table = dynamodb.Table(os.environ['DYNAMODB_TABLE_NAME'])
    sentiment_lambda_name = os.environ['SENTIMENT_LAMBDA_NAME']

    for record in event['Records']:
        # Extract S3 bucket and key from the event
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        try:
            # 1. Read the file from S3
            s3_object = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            file_content = s3_object['Body'].read().decode('utf-8')

            
            # Assuming your S3 file contains a single JSON object like:
            # {"text": "This is a great product!", "author": "User123", "source": "Twitter"}

            social_media_text = ""
            author = "anonymous"
            source_platform = "unknown"

            try:
                post_data = json.loads(file_content)
                social_media_text = post_data.get('text', '') 
                author = post_data.get('author', 'anonymous')
                source_platform = post_data.get('source', 'unknown')
            except json.JSONDecodeError:
                # If it's not valid JSON, treat the whole content as text
                social_media_text = file_content
                source_platform = 'plain_text_file' # Indicate source for non-JSON

            if not social_media_text.strip(): # Check if text is empty or just whitespace
                print(f"Skipping empty or malformed text from {object_key}")
                continue

            # Generate a unique post ID and get current timestamp
            post_id = str(uuid.uuid4())
            current_timestamp_ms = int(datetime.now().timestamp() * 1000) # Milliseconds for consistency

            # 2. Store raw data in DynamoDB
            raw_item = {
                'post_id': post_id,
                's3_bucket': bucket_name,
                's3_key': object_key,
                'raw_content': social_media_text, 
                'author': author,
                'source_platform': source_platform,
                'ingestion_timestamp_ms': current_timestamp_ms # Use consistent naming
            }
            dynamodb_table.put_item(Item=raw_item)
            print(f"Stored raw post {post_id} in DynamoDB.")

            # 3. Invoke SentimentAnalysisLambda asynchronously
            payload = {
                'post_id': post_id,
                'text_to_analyze': social_media_text,
                'original_s3_bucket': bucket_name,
                'original_s3_key': object_key,
                'author': author,
                'source_platform': source_platform,
                'ingestion_timestamp_ms': current_timestamp_ms
            }

            lambda_client.invoke(
                FunctionName=sentiment_lambda_name,
                InvocationType='Event', # 'Event' for asynchronous invocation (fire-and-forget)
                Payload=json.dumps(payload)
            )
            print(f"Invoked SentimentAnalysisLambda for post {post_id}.")

        except Exception as e:
            print(f"Error processing {object_key} from {bucket_name}: {e}")
            # In a real system, consider a Dead-Letter Queue (DLQ) for failed messages
            # or push to an SQS queue for retry logic.

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed S3 events.')
    }
