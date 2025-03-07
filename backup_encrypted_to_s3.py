import boto3
import os
import shutil
from cryptography.fernet import Fernet

# AWS S3 Configuration
AWS_REGION = "ap-south-1"  # Change to your AWS region
BUCKET_NAME = "abhibucket142003"  # Change this
ENCRYPTION_KEY_FILE = "encryption.key"  # Stores encryption key

def generate_key():
    """Generates and saves an encryption key."""
    key = Fernet.generate_key()
    with open(ENCRYPTION_KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print(f"🔑 Encryption key saved to {ENCRYPTION_KEY_FILE}")

def load_key():
    """Loads the encryption key from file."""
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        generate_key()
    with open(ENCRYPTION_KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_file(file_path, key):
    """Encrypts a file using AES-256 encryption."""
    cipher = Fernet(key)
    encrypted_file = file_path + ".enc"

    with open(file_path, "rb") as f:
        encrypted_data = cipher.encrypt(f.read())

    with open(encrypted_file, "wb") as f:
        f.write(encrypted_data)

    print(f"🔒 Encrypted: {encrypted_file}")
    return encrypted_file

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
        key = load_key()  # Load encryption key
        encrypted_file = encrypt_file(zip_file, key)  # Encrypt the zip file
        upload_to_s3(encrypted_file, BUCKET_NAME)  # Upload encrypted file
        os.remove(zip_file)  # Remove unencrypted zip
        os.remove(encrypted_file)  # Remove encrypted file after upload
        print("🗑️ Local files removed after upload.")
