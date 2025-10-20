🚀 Getting Started

Clone the repository.
Populate the .env file in the root directory with the required values.
Install dependencies and start the server.


variable description in .env file

1. FILE_BASEPATH : base URI of the bucket. For example if the file is in S3 bucket then the it should be s3://<bucket-name>

2. EMBEDDING_MODEL = name of the embedding model from aws.

3. AWS_ACCESS_KEY_ID : AWS access key for authenticating API requests.

4. AWS_SECRET_ACCESS_KEY : AWS secret key for secure access to AWS services.

5. AWS_REGION_NAME : AWS region where the Bedrock service is hosted.