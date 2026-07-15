# Azure Deployment Guide

## Prerequisites

1. **Azure Subscription** - Active Azure account
2. **Azure CLI** - Install from [azure.microsoft.com/cli](https://azure.microsoft.com/en-us/products/azure-cli)
3. **Docker** - For building container images
4. **Git** - For version control

## Deployment Steps

### 1. Login to Azure

```bash
az login
```

### 2. Create Resource Group

```bash
az group create \
  --name portfolio-agent-rg \
  --location eastus
```

### 3. Create Container Registry

```bash
az acr create \
  --resource-group portfolio-agent-rg \
  --name portfolioagistry \
  --sku Basic
```

### 4. Build and Push Docker Image

```bash
# Build image
docker build -t portfolio-agent:latest .

# Tag for registry
docker tag portfolio-agent:latest portfolioagistry.azurecr.io/portfolio-agent:latest

# Login to registry
az acr login --name portfolioagistry

# Push image
docker push portfolioagistry.azurecr.io/portfolio-agent:latest
```

### 5. Deploy Container Instance

#### Option A: Using Azure CLI

```bash
az container create \
  --resource-group portfolio-agent-rg \
  --name portfolio-agent \
  --image portfolioagistry.azurecr.io/portfolio-agent:latest \
  --cpu 2 \
  --memory 4 \
  --registry-login-server portfolioagistry.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --ports 5000 \
  --environment-variables AZURE_ENV=production \
  --dns-name-label portfolio-agent
```

#### Option B: Using ARM Template

```bash
az deployment group create \
  --resource-group portfolio-agent-rg \
  --template-file azure-deploy.json \
  --parameters \
    appName=portfolio-agent \
    containerImage=portfolioagistry.azurecr.io/portfolio-agent:latest
```

### 6. Get Application URL

```bash
az container show \
  --resource-group portfolio-agent-rg \
  --name portfolio-agent \
  --query ipAddress.fqdn
```

Output will be: `portfolio-agent.<region>.azurecontainers.io:5000`

## Access the Application

Navigate to: `http://portfolio-agent.<region>.azurecontainers.io:5000`

## Alternative: Azure App Service Deployment

### 1. Create App Service Plan

```bash
az appservice plan create \
  --name portfolio-agent-plan \
  --resource-group portfolio-agent-rg \
  --sku B2 \
  --is-linux
```

### 2. Create Web App

```bash
az webapp create \
  --resource-group portfolio-agent-rg \
  --plan portfolio-agent-plan \
  --name portfolio-agent-app \
  --deployment-container-image-name-user portfolioagistry.azurecr.io/portfolio-agent:latest
```

### 3. Configure Container

```bash
az webapp config container set \
  --resource-group portfolio-agent-rg \
  --name portfolio-agent-app \
  --docker-custom-image-name portfolioagistry.azurecr.io/portfolio-agent:latest \
  --docker-registry-server-url https://portfolioagistry.azurecr.io \
  --docker-registry-server-user <username> \
  --docker-registry-server-password <password>
```

## Monitoring & Troubleshooting

### View Logs

```bash
# Container logs
az container logs \
  --resource-group portfolio-agent-rg \
  --name portfolio-agent
```

### Check Container Status

```bash
az container show \
  --resource-group portfolio-agent-rg \
  --name portfolio-agent \
  --query "containers[0].instanceView.currentState"
```

### Restart Container

```bash
az container restart \
  --resource-group portfolio-agent-rg \
  --name portfolio-agent
```

## Cost Optimization

- **Container Instances**: Auto-scales, pay per second
- **App Service**: Reserved instances for 30%+ savings
- **Consider**: Use `Standard` tier for production workloads

## Security Best Practices

1. Use Azure Managed Identity for authentication
2. Store secrets in Azure Key Vault
3. Enable Network Security Groups
4. Use Azure Container Registry with private endpoints
5. Implement WAF (Web Application Firewall) for App Service

## Cleanup

```bash
# Delete resource group (deletes all resources)
az group delete --name portfolio-agent-rg
```

## Support & Documentation

- [Azure Container Instances Docs](https://docs.microsoft.com/azure/container-instances/)
- [Azure App Service Docs](https://docs.microsoft.com/azure/app-service/)
- [Azure CLI Reference](https://docs.microsoft.com/cli/azure/)
