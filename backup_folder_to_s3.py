import boto3
import os

# AWS S3 Configuration
AWS_REGION = "ap-south-1"  # Change to your AWS region
BUCKET_NAME = "abhibucket142003"  # Change this

def upload_file_to_s3(file_path, bucket_name, s3_folder=""):
    """Uploads a file to S3, keeping the folder structure."""
    s3 = boto3.client("s3")
    
    # Preserve folder structure in S3
    file_name = os.path.basename(file_path)
    s3_key = f"{s3_folder}/{file_name}" if s3_folder else file_name

    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"✅ Uploaded: {file_name} -> s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"❌ Error uploading {file_name}: {str(e)}")

def upload_folder_to_s3(folder_path, bucket_name):
    """Uploads all files in a folder to S3."""
    if not os.path.exists(folder_path):
        print("❌ Folder does not exist. Please enter a valid folder path.")
        return
    
    s3_folder = os.path.basename(folder_path)  # Keep folder structure in S3
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            upload_file_to_s3(file_path, bucket_name, s3_folder)

if __name__ == "__main__":
    folder_path = input("Enter the full path of the folder to back up: ")

    upload_folder_to_s3(folder_path, BUCKET_NAME)
