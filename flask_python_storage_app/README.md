# Azure Blob Storage File Upload (Flask)

This is a simple Flask web application that allows users to upload files using Azure Blob Storage. It uses [Microsoft Entra Workload Identity](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview) via `DefaultAzureCredential` for secure access to the storage account.

## Features

- 📤 Upload files to Azure Blob Storage
- 🔐 Authentication via `DefaultAzureCredential`
- 🌐 Simple web interface with HTML forms

## Prerequisites

Before running the app, ensure you have:

- An [Azure Storage Account](https://portal.azure.com/)
- A container named `uploads` in your Blob Storage
- Proper access configured via Microsoft Entra ID and [DefaultAzureCredential](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python)
- Python 3.8+

## File Structure

```
.
├── app.py                  # Main Flask application
├── templates/
│   └── index.html          # Upload form
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## License

This project is licensed under the MIT License.