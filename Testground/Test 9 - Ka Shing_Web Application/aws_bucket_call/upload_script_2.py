import boto3
from keys import ACCESS_KEY, SECRET_KEY, BUCKET

PREFIX = 'files/'

s3 = boto3.resource(
    's3', 
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

# Creating an empty file called "_DONE" and putting it in the S3 bucket
obj = s3.Object(BUCKET, PREFIX + 'test.csv').put(Body='Testing, testing, 1, 2, 3')

# s3.Object(BUCKET, PREFIX + 'test.csv').put(Body="testing, testing, 1, 2, 3")
