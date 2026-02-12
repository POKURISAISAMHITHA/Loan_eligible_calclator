# 🚀 Quick Deployment Guide

## Choose Your Deployment Path

### 🎯 Option 1: Quick Start (DigitalOcean - Easiest)

**Time:** 30 minutes | **Cost:** ~$100/month | **Best for:** Startups, MVPs

```bash
# 1. Create DigitalOcean account and install doctl
brew install doctl  # or apt-get install doctl

# 2. Authenticate
doctl auth init

# 3. Create Kubernetes cluster
doctl kubernetes cluster create loan-approval \
  --region nyc1 \
  --node-pool "name=workers;size=s-2vcpu-4gb;count=3"

# 4. Get kubeconfig
doctl kubernetes cluster kubeconfig save loan-approval

# 5. Deploy
./scripts/deploy-k8s.sh production
```

### 🏢 Option 2: AWS ECS (Production-Ready)

**Time:** 2 hours | **Cost:** ~$300/month | **Best for:** Enterprise, Scalability

```bash
# 1. Configure AWS CLI
aws configure

# 2. Create infrastructure
cd terraform/aws
terraform init
terraform plan
terraform apply

# 3. Build and push image
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ECR_URL
docker build -t loan-approval:latest .
docker tag loan-approval:latest ECR_URL/loan-approval:latest
docker push ECR_URL/loan-approval:latest

# 4. Deploy to ECS
aws ecs update-service --cluster loan-approval-cluster --service loan-approval-service --force-new-deployment
```

### ☁️ Option 3: Google Cloud Run (Serverless)

**Time:** 15 minutes | **Cost:** ~$20/month | **Best for:** Variable traffic, Pay-per-use

```bash
# 1. Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# 2. Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 3. Build and deploy in one command
gcloud run deploy loan-approval \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SERPER_API_KEY=$SERPER_KEY,GEMINI_API_KEY=$GEMINI_KEY

# 4. Done! Get URL
gcloud run services describe loan-approval --region us-central1 --format='value(status.url)'
```

### 🐳 Option 4: Existing Docker Environment

**Already have Docker/K8s infrastructure?**

```bash
# Simple deployment
docker compose -f docker-compose.prod.yml up -d

# Or Kubernetes
kubectl apply -f kubernetes/
```

---

## 📋 Pre-Deployment Checklist

### Required:
- [ ] API Keys configured (Serper, Gemini)
- [ ] Docker installed locally
- [ ] Git repository set up
- [ ] Domain name (for production)

### Recommended:
- [ ] SSL certificate (Let's Encrypt)
- [ ] Monitoring tools (Prometheus/Grafana)
- [ ] Backup strategy
- [ ] CI/CD pipeline configured

---

## 🔑 Secrets Configuration

### 1. Generate Required Secrets

```bash
# JWT Secret
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"

# Encryption Key (for PII data)
python3 -c "from cryptography.fernet import Fernet; print('ENCRYPTION_KEY=' + Fernet.generate_key().decode())"
```

### 2. Create Kubernetes Secret

```bash
# Copy template
cp kubernetes/secrets-template.yaml kubernetes/secrets.yaml

# Edit with your values
nano kubernetes/secrets.yaml

# Apply
kubectl apply -f kubernetes/secrets.yaml -n production
```

### 3. For AWS Secrets Manager

```bash
aws secretsmanager create-secret \
  --name loan-approval/api-keys \
  --secret-string '{
    "SERPER_API_KEY":"your-key",
    "GEMINI_API_KEY":"your-key",
    "JWT_SECRET_KEY":"your-key",
    "ENCRYPTION_KEY":"your-key"
  }'
```

---

## 🌐 Domain & SSL Setup

### Option A: Let's Encrypt (Free)

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# SSL will be automatically provisioned!
```

### Option B: CloudFlare (Recommended)

1. Add your domain to CloudFlare
2. Point DNS to your load balancer
3. Enable "Full (strict)" SSL mode
4. CloudFlare handles certificates automatically

---

## 📊 Verify Deployment

### Health Checks

```bash
# Quick health check
curl https://api.yourdomain.com/health

# Expected response:
# {
#   "status": "healthy",
#   "database": "connected",
#   "agents": { ... }
# }
```

### Load Test

```bash
# Install locust
pip install locust

# Run load test
locust -f tests/load/locustfile.py \
  --host https://api.yourdomain.com \
  --users 100 \
  --spawn-rate 10 \
  --run-time 2m \
  --headless
```

### Monitor Logs

```bash
# Kubernetes logs
kubectl logs -f deployment/loan-approval-api -n production

# Or use the script
./view-logs.sh
```

---

## 🔒 Security Post-Deployment

### 1. Enable Rate Limiting

```yaml
# Add to kubernetes/deployment.yaml annotations
nginx.ingress.kubernetes.io/limit-rps: "100"
nginx.ingress.kubernetes.io/limit-connections: "50"
```

### 2. Enable WAF (Web Application Firewall)

**CloudFlare:**
- Enable "I'm Under Attack" mode
- Configure rate limiting rules
- Enable bot protection

**AWS WAF:**
```bash
aws wafv2 create-web-acl \
  --name loan-approval-waf \
  --scope REGIONAL \
  --default-action Allow={} \
  --rules file://waf-rules.json
```

### 3. Network Policies

```yaml
# kubernetes/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: loan-approval-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: loan-approval
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443  # HTTPS
    - protocol: TCP
      port: 5432  # PostgreSQL
```

---

## 📈 Monitoring Setup (5 minutes)

### Quick Monitoring with Grafana Cloud (Free tier)

```bash
# 1. Sign up at grafana.com

# 2. Get agent key from Grafana Cloud

# 3. Install Grafana Agent
kubectl apply -f https://raw.githubusercontent.com/grafana/agent/main/production/kubernetes/agent-bare.yaml

# 4. Configure agent with your key

# 5. Done! View metrics in Grafana Cloud
```

### Self-Hosted Monitoring

```bash
# Install Prometheus & Grafana
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace

# Access Grafana
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
# Username: admin, Password: prom-operator
```

---

## 🔄 CI/CD Setup

### GitHub Actions (Automated)

```bash
# 1. Add secrets to GitHub repository
gh secret set KUBE_CONFIG_PROD < ~/.kube/config
gh secret set SERPER_API_KEY
gh secret set GEMINI_API_KEY
gh secret set SLACK_WEBHOOK  # Optional

# 2. Push to trigger deployment
git push origin main

# 3. Monitor in GitHub Actions tab
```

### Manual Deployment

```bash
# Build new version
docker build -t ghcr.io/yourusername/loan_approval:v1.2.0 .

# Push to registry
docker push ghcr.io/yourusername/loan_approval:v1.2.0

# Update Kubernetes
kubectl set image deployment/loan-approval-api \
  loan-approval=ghcr.io/yourusername/loan_approval:v1.2.0 \
  -n production

# Monitor rollout
kubectl rollout status deployment/loan-approval-api -n production
```

---

## 🎯 Performance Optimization

### 1. Database Connection Pooling

```python
# Already configured in database.py
# For PostgreSQL, use SQLAlchemy with pool settings:
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

### 2. Enable Redis Caching

```bash
# Deploy Redis
helm install redis bitnami/redis -n production

# Get password
export REDIS_PASSWORD=$(kubectl get secret redis -o jsonpath="{.data.redis-password}" | base64 -d)

# Update secrets with Redis URL
kubectl patch secret loan-approval-secrets -n production \
  --type merge \
  -p '{"stringData":{"redis-url":"redis://:'"$REDIS_PASSWORD"'@redis-master:6379/0"}}'
```

### 3. CDN for Static Assets

- Use CloudFlare for free CDN
- Or AWS CloudFront
- Configure in ingress annotations

---

## 🚨 Troubleshooting

### Pods not starting?

```bash
# Check pod status
kubectl get pods -n production

# Describe pod for events
kubectl describe pod POD_NAME -n production

# Check logs
kubectl logs POD_NAME -n production
```

### Database connection issues?

```bash
# Test database connectivity
kubectl run psql-test --rm -i --restart=Never \
  --image=postgres:15 -n production -- \
  psql $DATABASE_URL -c "SELECT 1"
```

### High memory usage?

```bash
# Check resource usage
kubectl top pods -n production

# Increase limits in deployment.yaml
resources:
  limits:
    memory: "1Gi"  # Increase from 512Mi
```

---

## 📞 Support & Resources

### Documentation
- Full deployment guide: `DEPLOYMENT_GUIDE.md`
- Docker guide: `DOCKER_GUIDE.md`
- Main README: `README.md`

### Scripts
- `./scripts/deploy-k8s.sh` - Kubernetes deployment
- `./view-logs.sh` - View production logs
- `./docker-status.sh` - Docker container status

### Community
- GitHub Issues: [Create issue](https://github.com/POKURISAISAMHITHA/Loan_eligible_calclator/issues)
- Discussions: [GitHub Discussions](https://github.com/POKURISAISAMHITHA/Loan_eligible_calclator/discussions)

---

## ✅ Post-Deployment Checklist

- [ ] Application is accessible via domain
- [ ] SSL certificate is valid
- [ ] Health endpoint returns 200 OK
- [ ] All 7 agents are initialized
- [ ] Database is connected
- [ ] Logs are being collected
- [ ] Monitoring dashboards are working
- [ ] Alerts are configured
- [ ] Backup strategy is in place
- [ ] CI/CD pipeline is working
- [ ] Load testing completed
- [ ] Security scan passed
- [ ] Documentation is updated

---

**Congratulations! Your Loan Approval System is now in production! 🎉**

Questions? Check the [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed information.
