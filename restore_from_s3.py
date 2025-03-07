import boto3
import os
import shutil
from cryptography.fernet import Fernet

# AWS S3 Configuration
AWS_REGION = "ap-south-1"  # Change to your AWS region
BUCKET_NAME = "abhibucket142003"  # Change this
ENCRYPTION_KEY_FILE = "encryption.key"  # Key used for decryption
RESTORE_FOLDER = "restored_backups"  # Where files will be restored

def load_key():
    """Loads the encryption key from file."""
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        print("❌ Encryption key not found! Cannot decrypt files.")
        exit(1)
    
    with open(ENCRYPTION_KEY_FILE, "rb") as key_file:
        return key_file.read()

def decrypt_file(encrypted_file, key):
    """Decrypts an encrypted file."""
    cipher = Fernet(key)
    decrypted_file = encrypted_file.replace(".enc", "")

    with open(encrypted_file, "rb") as f:
        decrypted_data = cipher.decrypt(f.read())

    with open(decrypted_file, "wb") as f:
        f.write(decrypted_data)

    print(f"🔓 Decrypted: {decrypted_file}")
    return decrypted_file

def download_from_s3(file_name, bucket_name):
    """Downloads a file from S3."""
    s3 = boto3.client("s3")
    download_path = os.path.join(os.getcwd(), file_name)

    try:
        s3.download_file(bucket_name, file_name, download_path)
        print(f"📥 Downloaded: {file_name} from S3")
        return download_path
    except Exception as e:
        print(f"❌ Error downloading {file_name}: {str(e)}")
        return None

def extract_zip(zip_path):
    """Extracts a ZIP file."""
    extract_to = os.path.join(os.getcwd(), RESTORE_FOLDER)
    os.makedirs(extract_to, exist_ok=True)

    shutil.unpack_archive(zip_path, extract_to)
    print(f"📂 Extracted files to: {extract_to}")

if __name__ == "__main__":
    s3_file_name = input("Enter the name of the backup file to restore (e.g., backup.zip.enc): ")

    # Step 1: Download the encrypted backup
    encrypted_file = download_from_s3(s3_file_name, BUCKET_NAME)
    
    if encrypted_file:
        key = load_key()  # Step 2: Load encryption key
        decrypted_file = decrypt_file(encrypted_file, key)  # Step 3: Decrypt the file
        extract_zip(decrypted_file)  # Step 4: Extract the zip file

        # Clean up
        os.remove(encrypted_file)
        os.remove(decrypted_file)
        print("🗑️ Temporary files removed after restore.")
