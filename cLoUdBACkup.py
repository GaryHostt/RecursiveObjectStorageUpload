import os
import sys
import time
import threading
from google.oauth2 import service_account
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/folder/folder/credentials.json'
# Imports the Google Cloud client library
from google.cloud import storage

#Specify source folder on line 13
#Specify GCP bucket on line 15
#In the case below, folders are created empty until /test, then the subdir. of test
#will be uploaded with its contents as well
path = '/Users/desktop/test2'
bucket_name = 'my-bucket'

print('Preparing to backup to cloud')
time.sleep(2)

def get_files2(path):
    for directory, _, filenames in os.walk(path):
        for filename in filenames:
            yield os.path.join(directory, filename)
            print(str(filename) + ' has been sent to the Cloud')

print('Getting coordinates....')
time.sleep(3)

storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
time.sleep(3)
print('Sending files to ' + str(bucket))
time.sleep(3)

def upload_serial(bucket, filename):
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)

def upload_parallel(bucket, path):
    threads = []
    for filename in get_files2(path):
        # consider using thread pool
        thread = threading.Thread(target=upload_serial, args=(bucket, filename))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

upload_parallel(bucket, path)
print('Launch complete')

if __name__ == "__main__":




