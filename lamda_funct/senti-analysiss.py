import json
import boto3
import os
from datetime import datetime

# Initialize AWS clients outside the handler
comprehend_client = boto3.client('comprehend')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    print(f"Received payload from Ingest Lambda: {json.dumps(event)}")

    # Extract data from the payload received from Ingest Lambda
    post_id = event.get('post_id')
    text_to_analyze = event.get('text_to_analyze')
    original_s3_bucket = event.get('original_s3_bucket')
    original_s3_key = event.get('original_s3_key')
    author = event.get('author')
    source_platform = event.get('source_platform')
    ingestion_timestamp_ms = event.get('ingestion_timestamp_ms')

    if not text_to_analyze or not text_to_analyze.strip():
        print(f"No valid text to analyze for post_id: {post_id}. Skipping sentiment analysis.")
        return {
            'statusCode': 400,
            'body': json.dumps('No text_to_analyze provided or text is empty.')
        }

    try:
        # 1. Perform Sentiment Analysis using Amazon Comprehend
        # Note: For very long texts, Comprehend has limits 
        # For this project, assuming typical social media post length.
        sentiment_response = comprehend_client.detect_sentiment(
            Text=text_to_analyze,
            LanguageCode='en' # Assuming English. Adjust if your data is multi-language.
        )
        sentiment = sentiment_response['Sentiment']
        sentiment_scores = sentiment_response['SentimentScore'] # Provides scores for Positive, Negative, Neutral, Mixed

        # 2. Extract Key Phrases (Optional but enhances data)
        key_phrases_response = comprehend_client.detect_key_phrases(
            Text=text_to_analyze,
            LanguageCode='en'
        )
        key_phrases = [kp['Text'] for kp in key_phrases_response['KeyPhrases']]

        # 3. Prepare enriched data for storage
        processed_data = {
            'post_id': post_id,
            'original_text': text_to_analyze,
            'sentiment': sentiment,
            'sentiment_scores_positive': sentiment_scores.get('Positive', 0.0), # Flatten sentiment scores
            'sentiment_scores_negative': sentiment_scores.get('Negative', 0.0),
            'sentiment_scores_neutral': sentiment_scores.get('Neutral', 0.0),
            'sentiment_scores_mixed': sentiment_scores.get('Mixed', 0.0),
            'key_phrases': key_phrases,
            'author': author,
            'source_platform': source_platform,
            'ingestion_timestamp_ms': ingestion_timestamp_ms,
            'processing_timestamp_ms': int(datetime.now().timestamp() * 1000),
            'original_s3_key': original_s3_key # For traceability back to the raw file
        }

        # 4. Write processed data to Processed S3 Bucket
        # Use timestamp from ingestion for partitioning to ensure consistency
        dt_object = datetime.fromtimestamp(ingestion_timestamp_ms / 1000) # Convert ms to seconds
        year = dt_object.strftime('%Y')
        month = dt_object.strftime('%m')
        day = dt_object.strftime('%d')

        # Define output S3 key with year/month/day partitions
        output_s3_key = f"year={year}/month={month}/day={day}/{post_id}.json"

        s3_client.put_object(
            Bucket=os.environ['PROCESSED_S3_BUCKET_NAME'],
            Key=output_s3_key,
            Body=json.dumps(processed_data, indent=2) # Store as pretty JSON
        )
        print(f"Stored processed data for post {post_id} at s3://{os.environ['PROCESSED_S3_BUCKET_NAME']}/{output_s3_key}")

    except Exception as e:
        print(f"Error during sentiment analysis for post {post_id}: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error during sentiment analysis: {str(e)}")
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Sentiment analysis completed and data stored.')
    }
