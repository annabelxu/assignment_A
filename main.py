import os, datetime
from flask import Flask, request
from google.cloud import storage
from google.cloud import datastore

app = Flask(__name__)
CLOUD_STORAGE_BUCKET = "photo-timeline-shared123" 


@app.route("/")
def homepage():
    return "Hello Photo Timeline!"

@app.route("/upload", methods=['POST'])

def upload():
    photo = request.files['file']
    print(photo.filename)

    storage_client = storage.Client.from_service_account_json('photo-timeline-shared-347519-a62ca851fc20.json')
    bucket_name = CLOUD_STORAGE_BUCKET
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(photo.filename)
    blob.upload_from_string(photo.read(), content_type=photo.content_type)

    datastore_client = datastore.Client.from_service_account_json('photo-timeline-shared-347519-a62ca851fc20.json')
    kind = 'Photos'
    name = blob.name
    key = datastore_client.key(kind, name)

    entity = datastore.Entity(key)
    entity['blob_name'] = blob.name
    entity['image_public_url'] = blob.public_url
    entity['timestamp'] = datetime.datetime.now()
    entity['star_rating'] = 0
  

    datastore_client.put(entity)



    return ":)"

if __name__ == '__main__':
  app.run(debug=True)