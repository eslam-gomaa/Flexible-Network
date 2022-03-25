import boto3
import botocore
import urllib3
import socket
import os

class S3_APIs:

    def __init__(self):
        # Read from the configuration file
        self.access_key = ''
        self.secret_key = ''
        self.region = ''
        self.endpoint = ''
        self.s3_client = None


    def authenticate(self):
        self.s3_client = boto3.client(
            service_name='s3',
            aws_access_key_id = self.access_key,
            aws_secret_access_key = self.secret_key,
            endpoint_url = self.endpoint,
            region_name = self.region,
            # The next option is only required because my provider only offers "version 2"
            # authentication protocol. Otherwise this would be 's3v4' (the default, version 4).
            # config=botocore.client.Config(signature_version='s3'),
            )

        # Trying to list buckest to Validate credentials
        try:
            self.list_buckets()
        except (botocore.exceptions.HTTPClientError,
                urllib3.exceptions.URLSchemeUnknown,
                ValueError,
                socket.gaierror,
                botocore.exceptions.EndpointConnectionError,
                urllib3.exceptions.NewConnectionError,
                botocore.exceptions.ClientError) as e:
                print(f"ERROR -- Failed to validate S3 authentication\n> {e}")
                exit(1)
                
        

    def list_buckets(self):
        if self.s3_client is None:
            self.authenticate()
        return self.s3_client.list_buckets()

    def create_bucket(self, bucket_name, region=None):
        """
        Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: {"success": True, "fail_reason": ''} if bucket created, else {"success": False, "fail_reason": '...'}
        """
        if self.s3_client is None:
            self.authenticate()
        try:
            if region is None:
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': region}
                self.s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
            return {"success": True, "fail_reason": ''}
        except (botocore.exceptions.ClientError) as e:
            return {"success": False, "fail_reason": e}

    def delete_bucket(self, bucket_name):
        """
        Delete a bucket
        INPUT: 
            1. bucket_name
        """
        if self.s3_client is None:
            self.authenticate()
        try:
            self.s3_client.delete_bucket(Bucket=bucket_name)
        except (botocore.exceptions.ClientError) as e:
            return {"success": False, "fail_reason": e}
        return {"success": True, "fail_reason": ''}

    def create_object_from_data(self, bucket, object_name, content):
        pass


    def upload_file(self, file_path, bucket, object_name=None, directory=None):
        """
        Upload a file to an S3 bucket
        :param file_path: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: {"success": True, "fail_reason": ''} if bucket created, else {"success": False, "fail_reason": '...'}
        """
        if self.s3_client is None:
            self.authenticate()
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_path)
        if directory is not None:
            object_name = directory + '/' + object_name
        # Upload the file
        try:
            response = self.s3_client.upload_file(file_path, bucket, object_name)
        except (botocore.exceptions.ClientError) as e:
            return {"success": True, "fail_reason": e}
        return {"success": True, "fail_reason": ''}

    def list_objects(self, bucket):
        """
        List objects in a bucket
        INPUT
            1. bucket
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects
        """
        if self.s3_client is None:
            self.authenticate()
        try:
            buckets = self.s3_client.list_objects(Bucket=bucket)
        except (self.s3_client.exceptions.NoSuchBucket, botocore.exceptions.ClientError) as e:
             return {"success": False, "fail_reason": e, "output": ''}
        return {"success": True, "fail_reason": '', "output": buckets.get('Contents')}


    def get_object(self, bucket, file_name):
        """
        Get an object from a bucket
        INPUT
            1. bucket
            2. file_name
        """
        
        if self.s3_client is None:
            self.authenticate()
        try:
            obj = self.s3_client.get_object(Bucket=bucket, Key=file_name)
        except (self.s3_client.Client.exceptions.NoSuchKey, 
                self.s3_client.Client.exceptions.InvalidObjectState) as e:
                return {"success": True, "fail_reason": e, 'output': ''}
        return {"success": True, "fail_reason": '', 'output': obj.get('Body').read().decode('utf-8')}






s3 = S3_APIs()
# print(s3.list_buckets())
# print(s3.delete_bucket('love-you'))
# print(s3.upload_file('/tmp/90.84.41.239-8D30EC0137.txt', 'love-you-2', directory='sub-dir3'))
# print(s3.list_objects('love-you-2')['output'])
# print(s3.get_object('love-you-2', '90.84.41.239-8D30EC0137.txt')['output'])


