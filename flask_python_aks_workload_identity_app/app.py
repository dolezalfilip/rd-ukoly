import os
import logging
from flask import Flask, render_template_string
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import AzureError

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("flask-aks-app")

# Load config
KEY_VAULT_NAME = os.environ.get("KEY_VAULT_NAME")
SECRET_NAME = os.environ.get("SECRET_NAME")

if not KEY_VAULT_NAME or not SECRET_NAME:
    raise EnvironmentError("KEY_VAULT_NAME and SECRET_NAME environment variables must be set.")

# Azure Key Vault setup
VAULT_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net"
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=VAULT_URL, credential=credential)

# Flask app
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Secret Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f7f9fc; padding: 2rem; color: #333; }
        .container { max-width: 600px; margin: auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 2rem; }
        h1 { color: #0078D4; }
        .label { font-weight: bold; margin-top: 1rem; }
        .value { font-family: monospace; background: #eef; padding: 0.5rem; border-radius: 4px; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Azure Key Vault Secret Viewer</h1>
        {% if error %}
            <p class="error"><strong>Error:</strong> {{ error }}</p>
        {% else %}
            <p><span class="label">Key Vault:</span> {{ vault }}</p>
            <p><span class="label">Secret Name:</span> {{ name }}</p>
            <p><span class="label">Secret Value:</span> <span class="value">{{ value }}</span></p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    """
    Main route - displays the secret in a styled HTML page
    """
    try:
        logger.info(f"Fetching secret '{SECRET_NAME}' from Key Vault '{KEY_VAULT_NAME}'...")
        secret = secret_client.get_secret(SECRET_NAME)
        logger.info("Secret retrieved successfully.")
        return render_template_string(
            HTML_TEMPLATE,
            vault=KEY_VAULT_NAME,
            name=SECRET_NAME,
            value=secret.value,
            error=None
        )
    except AzureError as e:
        logger.error(f"Failed to retrieve secret: {str(e)}")
        return render_template_string(
            HTML_TEMPLATE,
            vault=KEY_VAULT_NAME,
            name=SECRET_NAME,
            value=None,
            error=str(e)
        ), 500

@app.route("/healthz", methods=["GET"])
def health_check():
    """
    Simple health check endpoint
    """
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)