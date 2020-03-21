import boto3

from keys import ACCESS_KEY, SECRET_KEY, BUCKET

s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        # aws_session_token=SESSION_TOKEN
    )
s3.download_file(BUCKET, 'files/files/test.txt', 'files/tester.txt')
