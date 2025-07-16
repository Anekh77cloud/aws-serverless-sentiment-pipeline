# aws-serverless-sentiment-pipeline
Automated serverless data pipeline on AWS for social media sentiment analysis using Lambda, S3, DynamoDB,                 Amazon Comprehend.

* This project showcases a scalable, automated, and reliable serverless data pipeline on Amazon Web Services (AWS) that can ingest data similar to social media, use artificial intelligence to conduct sentiment analysis in real time, and deliver the enriched data for easy access by analysts.

* Issue Resolved: Companies frequently find it difficult to monitor brand health, quickly comprehend public opinion, or extract insights from massive volumes of unstructured social media data. The entire process is automated by this pipeline, which turns unprocessed text into useful sentiment data.

Important attributes:
--------------------

* Completely serverless: This ensures high scalability and cost-effectiveness by eliminating the need to provision or     manage servers.

* Event-Driven: As soon as fresh data enters the S3 landing area, it is automatically processed.

* Using AWS for AI/ML Integration Understand for effective sentiment analysis and key phrase extraction using natural language processing (NLP).

* Scalable Data Lake: Provides flexible and affordable long-term storage by storing both raw and processed data in Amazon S3.

* Analytics Ready: Constructs structured data that is instantly queryable in Amazon Athena using standard SQL.

* Cost-optimized: AWS Free Tier was taken into consideration during design to reduce running costs.


Key Features 
------------ 

* Amazon S3 (Simple Storage Service): Used for extremely durable and scalable object storage.

* A single bucket (raw-social-data-.) serves as the landing area for social media data being received.

* Another bucket (processed-social-data-.) is a data lake for the enriched, sentiment-analyzed data, partitioned by date to support optimized querying.

* AWS Lambda: Serverless compute service that executes code in reaction to events.

* SocialDataIngestLambda: S3 object creation triggers it, reads in raw data, stores data in DynamoDB, and calls the SentimentAnalysisLambda.

* SentimentAnalysisLambda: Does sentiment analysis and key phrase extraction with Amazon Comprehend, then writes enhanced data to the processed S3 bucket.

* Amazon DynamoDB: A high-performance, flexible NoSQL database service. Used to maintain the raw social media posts, giving a durable and rapidly accessible record of original data.

* Amazon Comprehend: An AWS Natural Language Processing (NLP) service. Built directly into the Lambda function to do advanced sentiment analysis (detecting positive, negative, neutral, or mixed sentiment) and extract key phrases from the text.

* Amazon Athena: A serverless query service that simplifies analyzing data directly in S3 with standard SQL. Utilized to query the processed social media data, taking advantage of partition projection to scan data efficiently



Technical Skills
----------------

* Serverless Architecture Design & Implementation: Building an entire data pipeline using Lambda, S3, DynamoDB, and Athena, eliminating server management.

* Python Development: Writing robust Lambda functions using Python and the boto3 AWS SDK to interact with various AWS services.

* Data Engineering: Designing and implementing an automated ETL (Extract, Transform, Load) pipeline for unstructured and semi-structured data.

* AI/ML Integration: Seamlessly incorporating Amazon Comprehend (an AWS AI service) into the data processing workflow for intelligent text analysis.

* Data Lake Concepts: Structuring data in S3 with effective partitioning for scalability, cost-efficiency, and analytics readiness.

* NoSQL Database Management: Interacting with DynamoDB for high-performance, flexible data storage.

* SQL Querying & Data Analytics: Using Amazon Athena to perform ad-hoc queries and derive insights from S3-based data.

* Cloud Cost Optimization: Demonstrating awareness and implementation of strategies to minimize cloud spending.

* Troubleshooting & Debugging: Effectively using CloudWatch Logs to identify and resolve issues within a complex distributed system.



WORK-FLOW
---------

* Data Ingestion: Social media data (simulated as JSON files for this project) is uploaded to the designated Raw Data Landing S3 Bucket.

* Lambda Trigger: An S3 event notification triggers the SocialDataIngestLambda (Python).

* Initial Processing & Storage: The SocialDataIngestLambda reads the incoming file, extracts relevant text and metadata, and stores the raw record in Amazon DynamoDB.

* Sentiment Analysis Invocation: Immediately after storing the raw data, the SocialDataIngestLambda asynchronously invokes the SentimentAnalysisLambda.

* AI-Powered Enrichment: The SentimentAnalysisLambda takes the text, calls Amazon Comprehend to detect sentiment (Positive, Negative, Neutral, Mixed) and extract key phrases.

* Processed Data Storage: The SentimentAnalysisLambda then constructs an enriched JSON object (including sentiment, scores, key phrases) and writes it to the Processed Data Lake S3 Bucket. Data is stored in a year=YYYY/month=MM/day=DD/ folder structure, optimizing it for analytical querying.

* Data Querying: Data analysts or business users can then use Amazon Athena to run standard SQL queries directly on the processed data in the S3 Data Lake, gaining insights without needing to load data into a separate database.



FUTURE ENHANCEMENTS
-------------------

* Robust Error Handling: Implement Dead-Letter Queues (DLQs) for Lambda functions to handle processing failures more gracefully.

* Real-time Data Ingestion: Integrate with Amazon Kinesis or Apache Kafka for true streaming data ingestion.

* Advanced Analytics: Incorporate more complex NLP tasks or machine learning models (e.g., topic modeling, named entity recognition) using AWS SageMaker.

* Dashboarding: Connect Athena to a Business Intelligence (BI) tool like Power BI or Tableau for interactive dashboards (while QuickSight is an option, it was not utilized in this project due to cost considerations during development).

* CI/CD Pipeline: Automate deployment of Lambda functions and infrastructure using AWS CodePipeline, CodeBuild, and CloudFormation/SAM.



COST MANAGEMENT
---------------

* This project was developed with a strong focus on cost optimization and designed to operate well within the generous AWS Free Tier for testing and demonstration purposes.

* Key strategies employed for cost management include:

* Serverless First: Utilizing services like AWS Lambda, S3, DynamoDB, and Athena which are inherently cost-effective as you only pay for what you use (compute duration, storage, data scanned/requests).

* AWS Free Tier Utilization: All core services used (S3, Lambda, DynamoDB, Comprehend, Athena) offer extensive Free Tier allowances, making initial development and testing virtually free.

* Amazon Comprehend: The project leverages the Comprehend Free Tier (50,000 units of text per month for 12 months) for sentiment analysis.

* S3 Data Partitioning: Storing processed data in S3 with a year/month/day partition structure significantly reduces data scanned by Athena, directly lowering query costs.

* Athena Query Optimization: Using SELECT * LIMIT X during testing and focusing on specific partitions in WHERE clauses for actual analysis helps control costs as Athena bills per data scanned.

* Mindful Service Selection: While a visualization tool like Amazon QuickSight could be a next step, it was intentionally not included in this project's implementation due to its potential cost beyond the free trial period. The project demonstrates the data's readiness for such tools through its queryability in Athena, proving the core value proposition of the pipeline.

* Resource Cleanup: A commitment to deleting all created AWS resources once the project's demonstration phase is complete to ensure no lingering charges.