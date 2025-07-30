CREATE EXTERNAL TABLE IF NOT EXISTS social_analytics_db_anekh.social_posts1 (
  `post_id` string,
  `original_text` string,
  `sentiment` string,
  `sentiment_scores` struct<positive:double, negative:double, neutral:double, mixed:double>,
  `key_phrases` array<string>,
  `author` string,
  `source_platform` string,
  `location` string,
  `product` string,
  `ingestion_timestamp` bigint,
  `processing_timestamp` bigint,
  `original_s3_key` string
)
PARTITIONED BY (
  `year` string,
  `month` string,
  `day` string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://processed-social-data-anekh-project/'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'projection.enabled' = 'true',
  'projection.year.type' = 'integer',
  'projection.year.range' = '2023,2026',
  'projection.month.type' = 'integer',
  'projection.month.range' = '1,12',
  'projection.month.digits' = '2',
  'projection.day.type' = 'integer',
  'projection.day.range' = '1,31',
  'projection.day.digits' = '2',
  'storage.location.template' = 's3://processed-social-data-anekh-project/year=${year}/month=${month}/day=${day}/'
);
