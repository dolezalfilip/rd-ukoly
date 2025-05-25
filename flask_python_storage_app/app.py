import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

app = Flask(__name__)

# Azure Blob Storage Service
class BlobStorageService:
    def __init__(self):
        account_url = "XXX"
        credential = DefaultAzureCredential()
        self.blob_service_client = BlobServiceClient(account_url, credential=credential)
        self.container_name = 'uploads'

    def upload_blob(self, blob_name, data):
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
        blob_client.upload_blob(data, overwrite=True)

    def download_blob(self, blob_name):
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
        blob_data = blob_client.download_blob()
        return blob_data.readall()

# Initialize the Blob Storage Service
blob_service = BlobStorageService()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        
        if file.filename == '':
            return "No selected file"
        
        if file:
            blob_service.upload_blob(file.filename, file)
            return f"File {file.filename} uploaded successfully"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        file_stream = blob_service.download_blob(filename)
        return send_file(BytesIO(file_stream), attachment_filename=filename, as_attachment=True)
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
   app.run(debug=True)
