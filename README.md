# Automated Backup System  
A cloud-based backup solution using AWS S3.  
This script automatically compresses, encrypts, and uploads backups to AWS S3.  
It also supports decryption and restoration of backups.  



## Features  
✅ Automatic folder backups  
✅ AES-256 encryption for security  
✅ Uploads to AWS S3  
✅ Scheduled automation (Cron/Task Scheduler)  
✅ Secure decryption & restore process  


## Installation  
### 1. Clone the Repository  
```bash
git clone https://github.com/SoCalledKrish/Backup_S3.git  
cd automated-backup-system


pip install -r requirements.txt  


aws configure  


## Usage  
### Run Backup  
```bash
python automated_backup.py


python restore_from_s3.py  




