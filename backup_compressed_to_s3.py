import boto3
import os
import shutil

# AWS S3 Configuration
AWS_REGION = "ap-south-1"  # Change to your AWS region
BUCKET_NAME = "abhibucket142003"  # Change this

def compress_folder(folder_path):
    """Compresses a folder into a .zip file."""
    if not os.path.exists(folder_path):
        print("❌ Folder does not exist. Please enter a valid folder path.")
        return None
    
    zip_name = os.path.basename(folder_path) + ".zip"
    zip_path = os.path.join(os.path.dirname(folder_path), zip_name)
    
    shutil.make_archive(zip_path.replace(".zip", ""), 'zip', folder_path)
    print(f"📦 Folder compressed: {zip_path}")
    return zip_path

def upload_to_s3(file_path, bucket_name):
    """Uploads a file to S3."""
    s3 = boto3.client("s3")
    file_name = os.path.basename(file_path)

    try:
        s3.upload_file(file_path, bucket_name, file_name)
        print(f"✅ Uploaded: {file_name} -> s3://{bucket_name}/{file_name}")
    except Exception as e:
        print(f"❌ Error uploading {file_name}: {str(e)}")

if __name__ == "__main__":
    folder_path = input("Enter the full path of the folder to back up: ")
    
    zip_file = compress_folder(folder_path)
    
    if zip_file:
        upload_to_s3(zip_file, BUCKET_NAME)
        os.remove(zip_file)  # Optional: Delete zip after upload
        print("🗑️ Local zip file removed after upload.")
