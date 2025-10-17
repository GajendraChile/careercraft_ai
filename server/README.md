🚀 Getting Started

Clone the repository.
Populate the .env file in the root directory with the required values.
Install dependencies and start the server.

Description of the variable in the .env file:

1. MODEL_CLAUDE_SONNET : Identifier for the Claude Sonnet 4 model version hosted on Amazon Bedrock.

2. AWS_ACCESS_KEY_ID : AWS access key for authenticating API requests.

3. AWS_SECRET_ACCESS_KEY : AWS secret key for secure access to AWS services.

4. AWS_REGION_NAME : AWS region where the Bedrock service is hosted.

5. PROFILE_SEARCH_AGENT_URL = deployed url of the profile searcher agent hosted locally or on aws

6. BUCKET_NAME = AWS bucket name to be used to store uploaded files
PROFILE_MATCHER_AGENT_URL = deployed url of the profile matcher agent hosted locally or on aws
COURSE_RECOMMENDER_AGENT_URL = deployed url of the course recommender agent hosted locally or on aws
BUCKET_INITIALS = the bucket initials of the cloud bucket. For example, if the file is store in S3 bucket the value should be "s3://"