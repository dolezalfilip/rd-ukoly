# 🔐 Flask AKS Key Vault Viewer

This is a simple Python Flask application that runs on Azure Kubernetes Service (AKS) and securely retrieves a secret from **Azure Key Vault** using **Microsoft Entra Workload Identity** .

> The secret name and Key Vault name are passed in as environment variables.

---

## 🚀 Features

- Built with **Flask**
- Uses **DefaultAzureCredential** for automatic identity handling
- Accesses Azure Key Vault without storing credentials
- Includes a `/healthz` endpoint for Kubernetes probes

---

## 📦 Project Structure

```
.
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image definition
├── flask-app.yaml          # Kubernetes manifest (deployment + service)
└── README.md               # You're here!
```

---

## ⚙️ Configuration

Set the following environment variables in your deployment manifest:

| Variable         | Description                        |
|------------------|------------------------------------|
| `KEY_VAULT_NAME` | The name of your Azure Key Vault   |
| `SECRET_NAME`    | The name of the secret to retrieve |

---

## 🛠 Prerequisites

- Azure subscription with Key Vault and AKS set up
- [Microsoft Entra Workload Identity](https://learn.microsoft.com/azure/aks/workload-identity-overview) configured
- A federated **User Assigned Managed Identity** with `reader` access to secrets

---

## 🐳 Build & Push Docker Image

```bash
docker build -t <your_acr>.azurecr.io/flask-aks-keyvault:latest .
docker push <your_acr>.azurecr.io/flask-aks-keyvault:latest
```

---

## ☸️ Deploy to AKS

```bash
kubectl apply -f flask-app.yaml
```

Once deployed, find the external IP:

```bash
kubectl get service flask-service -n my-namespace
```

---

## 🌐 Access the App

Open the service in your browser or use curl:

```bash
curl http://<EXTERNAL-IP>/
```

You'll see a simple HTML page showing the secret value.

---

## ✅ Health Check

Use the `/healthz` endpoint for readiness/liveness probes:

```bash
curl http://<EXTERNAL-IP>/healthz
```

---

## 🧾 License

MIT License
