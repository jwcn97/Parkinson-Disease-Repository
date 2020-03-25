# === Imports ===
import boto3

# === S3 Class ===
class S3():
    """
    Class to handle S3 connections to AWS
    """
    def __init___(self, access, secret):
        """
        Constructor class.
        Instantiates the connection to the S3 bucket.

        Parameters
        ----------
        access (str)
            Access key
        secret (str)
            Secret access key
        """
        self.s3 = boto3.resource(
            's3',
            aws_access_key_id=access,
            aws_secret_access_key=secret
        )
