import boto3
from botocore.exceptions import ClientError
import aws_config
import config

def connect_to_s3():
    s3_client = boto3.client('s3',
                        aws_access_key_id=aws_config.S3_ACCESS_KEY_ID,
                        aws_secret_access_key=aws_config.S3_SECRET_ACCESS_KEY
                    )
    return s3_client

def upload_file_to_s3(client, file_name: str, object_name: str, bucket_name: str=config.S3_BUCKET_NAME) -> bool:
    """Wrapper around the upload_file method of boto3

    Args:
        client (S3.client):
        file_name (str): the file to upload
        object_name (str): what the file should be called in the s3 bucket
        bucket_name (str): which bucket to upload to

    Returns:
        bool: whether or not the operation was a success
    """
    try:
        response = client.upload_file(
            Filename=file_name,
            Bucket=bucket_name,
            Key=object_name
        )
    except ClientError as e:
        print(f"Exception {e}")
        return False
    return True