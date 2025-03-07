#Code for file uploadto s3 bucket!!!!

import boto3
import os

AWS_REGION = "ap-south-1" 
BUCKET_NAME = "abhibucket142003"  

def upload_to_s3(file_path, bucket_name):
    """Uploads a file to S3."""
    s3 = boto3.client("s3")
    file_name = os.path.basename(file_path)

    try:
        s3.upload_file(file_path, bucket_name, file_name)
        print(f" {file_name} successfully uploaded to {bucket_name}!")
    except Exception as e:
        print(f" Error uploading {file_name}: {str(e)}")

if __name__ == "__main__":
    file_path = input("Enter the full path of the file to back up: ")
    
    if os.path.exists(file_path):
        upload_to_s3(file_path, BUCKET_NAME)
    else:
        print(" File does not exist. Please enter a valid file path.")


