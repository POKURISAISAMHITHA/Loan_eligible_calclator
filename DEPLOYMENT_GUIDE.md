# 🚀 Production Deployment Guide
## Cloud-Native Deployment with CI/CD, Security, and Scalability

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Cloud Platforms](#cloud-platforms)
3. [Infrastructure Setup](#infrastructure-setup)
4. [CI/CD Pipeline](#cicd-pipeline)
5. [Security & Privacy](#security--privacy)
6. [Monitoring & Debugging](#monitoring--debugging)
7. [Scalability & Performance](#scalability--performance)
8. [Step-by-Step Deployment](#step-by-step-deployment)

---

## 🏗️ Architecture Overview

### Recommended Architecture: Microservices with Container Orchestration

```
┌─────────────────────────────────────────────────────────────┐
│                     Load Balancer (ALB/NLB)                 │
│                    with SSL/TLS Termination                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Container Orchestration (Kubernetes/ECS)        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   FastAPI    │  │   FastAPI    │  │   FastAPI    │     │
│  │  Container 1 │  │  Container 2 │  │  Container N │     │
│  │ (Auto-Scale) │  │ (Auto-Scale) │  │ (Auto-Scale) │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
            ┌─────────────┐     ┌─────────────┐
            │   Database  │     │    Cache    │
            │  (RDS/Cloud │     │   (Redis/   │
            │     SQL)    │     │  ElastiCache│
            └─────────────┘     └─────────────┘
```

### Key Components:
- **Load Balancer**: Distributes traffic across multiple containers
- **Container Orchestration**: Manages scaling, health checks, rolling updates
- **Database**: Managed PostgreSQL/MySQL for production
- **Cache**: Redis for session management and performance
- **Object Storage**: S3/Cloud Storage for logs and backups
- **Secrets Manager**: Secure API key storage
- **Monitoring**: CloudWatch/Stackdriver/Datadog
- **CI/CD**: GitHub Actions/GitLab CI/Jenkins

---

## ☁️ Cloud Platforms

### Option 1: AWS (Recommended for Enterprise)

**Pros:**
- Most mature cloud platform
- Extensive managed services
- Best security compliance (SOC2, HIPAA, PCI-DSS)
- Advanced monitoring with CloudWatch

**Services:**
- **Compute**: ECS (Fargate) or EKS (Kubernetes)
- **Database**: RDS PostgreSQL
- **Cache**: ElastiCache (Redis)
- **Load Balancer**: Application Load Balancer (ALB)
- **Storage**: S3
- **Secrets**: AWS Secrets Manager
- **CI/CD**: CodePipeline + CodeBuild
- **Monitoring**: CloudWatch + X-Ray
- **Cost**: ~$200-500/month (scalable)

### Option 2: Google Cloud Platform (GCP)

**Pros:**
- Great Kubernetes support (GKE)
- Excellent AI/ML integration
- Competitive pricing
- Easy to use

**Services:**
- **Compute**: Cloud Run or GKE
- **Database**: Cloud SQL
- **Cache**: Memorystore (Redis)
- **Load Balancer**: Cloud Load Balancing
- **Storage**: Cloud Storage
- **Secrets**: Secret Manager
- **CI/CD**: Cloud Build
- **Monitoring**: Cloud Operations (Stackdriver)
- **Cost**: ~$150-400/month

### Option 3: Azure

**Pros:**
- Great for Microsoft ecosystems
- Strong enterprise support
- Good compliance options

**Services:**
- **Compute**: AKS or Container Instances
- **Database**: Azure Database for PostgreSQL
- **Cache**: Azure Cache for Redis
- **Load Balancer**: Application Gateway
- **Storage**: Blob Storage
- **Secrets**: Key Vault
- **CI/CD**: Azure DevOps
- **Monitoring**: Azure Monitor
- **Cost**: ~$200-450/month

### Option 4: DigitalOcean (Budget-Friendly)

**Pros:**
- Simple and developer-friendly
- Predictable pricing
- Good for startups/SMBs
- Easy to get started

**Services:**
- **Compute**: Kubernetes (DOKS) or App Platform
- **Database**: Managed PostgreSQL
- **Cache**: Managed Redis
- **Load Balancer**: DigitalOcean Load Balancer
- **Storage**: Spaces
- **CI/CD**: GitHub Actions
- **Monitoring**: Built-in + Datadog
- **Cost**: ~$50-150/month

---

## 🛠️ Infrastructure Setup

### 1. Kubernetes Deployment (Recommended)

#### `kubernetes/deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loan-approval-api
  labels:
    app: loan-approval
spec:
  replicas: 3  # Scale to 3 instances
  selector:
    matchLabels:
      app: loan-approval
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: loan-approval
    spec:
      containers:
      - name: loan-approval
        image: ghcr.io/pokurisaisamhitha/loan-approval:latest
        ports:
        - containerPort: 8000
        env:
        - name: SERPER_API_KEY
          valueFrom:
            secretKeyRef:
              name: loan-approval-secrets
              key: serper-api-key
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: loan-approval-secrets
              key: gemini-api-key
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: loan-approval-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: loan-approval-service
spec:
  type: LoadBalancer
  selector:
    app: loan-approval
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: loan-approval-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: loan-approval-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

#### `kubernetes/secrets.yaml`
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: loan-approval-secrets
type: Opaque
stringData:
  serper-api-key: "your-serper-key-here"
  gemini-api-key: "your-gemini-key-here"
  database-url: "postgresql://user:pass@host:5432/loandb"
```

#### `kubernetes/ingress.yaml`
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: loan-approval-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - api.yourdomain.com
    secretName: loan-approval-tls
  rules:
  - host: api.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: loan-approval-service
            port:
              number: 80
```

### 2. AWS ECS Deployment (Alternative)

#### `ecs/task-definition.json`
```json
{
  "family": "loan-approval-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "loan-approval",
      "image": "ghcr.io/pokurisaisamhitha/loan-approval:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "secrets": [
        {
          "name": "SERPER_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:serper-key"
        },
        {
          "name": "GEMINI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:gemini-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/loan-approval",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ]
}
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions (Recommended)

#### `.github/workflows/deploy.yml`
```yaml
name: Build, Test, and Deploy

on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest tests/ --cov=. --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    permissions:
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/staging'
    environment:
      name: staging
      url: https://staging-api.yourdomain.com
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}
      
      - name: Deploy to Staging
        run: |
          kubectl set image deployment/loan-approval-api \
            loan-approval=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:staging-${{ github.sha }} \
            -n staging
          kubectl rollout status deployment/loan-approval-api -n staging

  deploy-production:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://api.yourdomain.com
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}
      
      - name: Deploy to Production
        run: |
          kubectl set image deployment/loan-approval-api \
            loan-approval=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest \
            -n production
          kubectl rollout status deployment/loan-approval-api -n production
      
      - name: Run smoke tests
        run: |
          sleep 30
          curl -f https://api.yourdomain.com/health || exit 1
      
      - name: Notify Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### GitLab CI/CD Alternative

#### `.gitlab-ci.yml`
```yaml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

test:
  stage: test
  image: python:3.10
  script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
    - pytest tests/ --cov=.
  coverage: '/TOTAL.*\s+(\d+%)$/'

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - main
    - staging

deploy_staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context staging
    - kubectl set image deployment/loan-approval loan-approval=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA -n staging
    - kubectl rollout status deployment/loan-approval -n staging
  environment:
    name: staging
    url: https://staging.yourdomain.com
  only:
    - staging

deploy_production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context production
    - kubectl set image deployment/loan-approval loan-approval=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA -n production
    - kubectl rollout status deployment/loan-approval -n production
  environment:
    name: production
    url: https://api.yourdomain.com
  only:
    - main
  when: manual
```

---

## 🔒 Security & Privacy

### 1. Data Encryption

#### Update `database.py` for encryption
```python
from cryptography.fernet import Fernet
import os
import base64

class SecureDatabase(Database):
    def __init__(self, db_path: str = "loan_approval.db"):
        super().__init__(db_path)
        # Load encryption key from environment
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            raise ValueError("ENCRYPTION_KEY environment variable required")
        self.cipher = Fernet(key.encode())
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
    
    def create_application(self, application: dict) -> str:
        """Create application with encrypted PII"""
        # Encrypt sensitive fields
        if 'applicant_name' in application:
            application['applicant_name'] = self.encrypt_data(application['applicant_name'])
        if 'email' in application:
            application['email'] = self.encrypt_data(application['email'])
        
        return super().create_application(application)
```

### 2. API Authentication

#### Add JWT authentication to `main.py`
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

@app.post("/loan/apply", dependencies=[Depends(verify_token)])
async def apply_for_loan(application: LoanApplicationRequest):
    # Protected endpoint
    pass
```

### 3. Security Headers

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Add security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*.yourdomain.com"])
app.add_middleware(HTTPSRedirectMiddleware)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

### 4. Secrets Management

#### Terraform for AWS Secrets Manager
```hcl
resource "aws_secretsmanager_secret" "api_keys" {
  name = "loan-approval/api-keys"
  
  tags = {
    Application = "loan-approval"
    Environment = "production"
  }
}

resource "aws_secretsmanager_secret_version" "api_keys" {
  secret_id = aws_secretsmanager_secret.api_keys.id
  secret_string = jsonencode({
    SERPER_API_KEY = var.serper_api_key
    GEMINI_API_KEY = var.gemini_api_key
    JWT_SECRET_KEY = var.jwt_secret_key
    ENCRYPTION_KEY = var.encryption_key
  })
}
```

### 5. Compliance Checklist

```yaml
# compliance/security-checklist.yml
security_requirements:
  data_protection:
    - ✅ Data encryption at rest (database)
    - ✅ Data encryption in transit (TLS/SSL)
    - ✅ PII data encryption (application-level)
    - ✅ Secure key management (Secrets Manager)
  
  access_control:
    - ✅ API authentication (JWT)
    - ✅ Role-based access control (RBAC)
    - ✅ Rate limiting
    - ✅ IP whitelisting (optional)
  
  audit_logging:
    - ✅ All API requests logged
    - ✅ Loan decisions logged
    - ✅ Access logs retained (90 days)
    - ✅ Sensitive data masked in logs
  
  compliance:
    - ✅ GDPR compliance (data retention, right to be forgotten)
    - ✅ SOC 2 Type II (access controls, monitoring)
    - ✅ PCI DSS (if handling payments)
    - ✅ Regular security audits
```

---

## 📊 Monitoring & Debugging

### 1. Prometheus & Grafana Setup

#### `monitoring/prometheus-config.yml`
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'loan-approval-api'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: loan-approval
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
```

### 2. Application Metrics

#### Add to `main.py`
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_fastapi_instrumentator import Instrumentator

# Metrics
loan_applications_total = Counter(
    'loan_applications_total',
    'Total number of loan applications',
    ['status', 'decision']
)

loan_processing_duration = Histogram(
    'loan_processing_duration_seconds',
    'Time spent processing loan applications',
    ['stage']
)

active_requests = Gauge(
    'active_requests',
    'Number of active requests'
)

# Initialize Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

@app.post("/loan/apply")
async def apply_for_loan(application: LoanApplicationRequest):
    start_time = time.time()
    
    try:
        # Process application
        result = await orchestrator.process_application(application)
        
        # Record metrics
        loan_applications_total.labels(
            status='success',
            decision=result.decision
        ).inc()
        
        duration = time.time() - start_time
        loan_processing_duration.labels(stage='total').observe(duration)
        
        return result
    except Exception as e:
        loan_applications_total.labels(status='error', decision='none').inc()
        raise
```

### 3. Logging Strategy

#### `logging_config.py`
```python
import logging
import json
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['service'] = 'loan-approval-api'
        log_record['environment'] = os.getenv('ENVIRONMENT', 'development')

def setup_logging():
    logHandler = logging.StreamHandler()
    formatter = CustomJsonFormatter()
    logHandler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    
    return logger
```

### 4. Distributed Tracing

#### Add OpenTelemetry
```python
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Setup tracing
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)
```

### 5. Grafana Dashboards

#### `monitoring/grafana-dashboard.json`
```json
{
  "dashboard": {
    "title": "Loan Approval System",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])"
          }
        ]
      },
      {
        "title": "Response Time (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      },
      {
        "title": "Approval Rate",
        "targets": [
          {
            "expr": "rate(loan_applications_total{decision=\"approved\"}[1h]) / rate(loan_applications_total[1h])"
          }
        ]
      }
    ]
  }
}
```

### 6. Alerting Rules

#### `monitoring/alerts.yml`
```yaml
groups:
  - name: loan_approval_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} req/sec"
      
      - alert: SlowResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Slow API response time"
          description: "95th percentile is {{ $value }}s"
      
      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Pod is crash looping"
      
      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Container memory usage > 90%"
```

---

## 📈 Scalability & Performance

### 1. Database Optimization

#### Switch to PostgreSQL
```python
# requirements.txt - add
psycopg2-binary==2.9.9
asyncpg==0.29.0
sqlalchemy==2.0.23

# database.py - PostgreSQL version
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/loandb")

engine = create_async_engine(DATABASE_URL, echo=False, pool_size=20, max_overflow=40)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session
```

### 2. Caching Layer

```python
import redis.asyncio as redis
from functools import wraps

# Redis connection
redis_client = redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379"),
    encoding="utf-8",
    decode_responses=True
)

def cache_result(expire: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Call function
            result = await func(*args, **kwargs)
            
            # Store in cache
            await redis_client.setex(
                cache_key,
                expire,
                json.dumps(result)
            )
            
            return result
        return wrapper
    return decorator

@cache_result(expire=600)
async def get_company_verification(company: str):
    # Expensive operation - cache for 10 minutes
    return await verify_company(company)
```

### 3. Load Testing

#### `locust/locustfile.py`
```python
from locust import HttpUser, task, between

class LoanApplicationUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def submit_loan_application(self):
        self.client.post("/loan/apply", json={
            "applicant_name": "Test User",
            "loan_amount": 250000,
            "monthly_income": 10000,
            "employment_years": 7,
            "credit_history": {
                "existing_loans": 2,
                "repayment_score": 0.92
            },
            "collateral_value": 350000,
            "company": "Microsoft"
        })
    
    @task(1)
    def check_health(self):
        self.client.get("/health")

# Run: locust -f locustfile.py --host=http://localhost:8000
```

### 4. Auto-Scaling Configuration

```yaml
# Auto-scaling based on metrics
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: loan-approval-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: loan-approval-api
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 2
        periodSeconds: 30
```

---

## 🚀 Step-by-Step Deployment

### Phase 1: Local Development (Week 1)
- [x] Application dockerized
- [x] Local testing complete
- [ ] Unit tests written
- [ ] Integration tests written

### Phase 2: Infrastructure Setup (Week 2)

#### AWS Setup Script
```bash
#!/bin/bash
# setup-aws-infrastructure.sh

# Variables
CLUSTER_NAME="loan-approval-cluster"
REGION="us-east-1"
DB_INSTANCE="loan-approval-db"

echo "🚀 Setting up AWS infrastructure..."

# 1. Create VPC and networking
aws cloudformation create-stack \
  --stack-name loan-approval-network \
  --template-body file://cloudformation/network.yml \
  --region $REGION

# 2. Create RDS PostgreSQL
aws rds create-db-instance \
  --db-instance-identifier $DB_INSTANCE \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password ${DB_PASSWORD} \
  --allocated-storage 20 \
  --storage-encrypted \
  --region $REGION

# 3. Create ElastiCache Redis
aws elasticache create-cache-cluster \
  --cache-cluster-id loan-approval-cache \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1 \
  --region $REGION

# 4. Create ECS Cluster
aws ecs create-cluster \
  --cluster-name $CLUSTER_NAME \
  --region $REGION

# 5. Create Secrets
aws secretsmanager create-secret \
  --name loan-approval/api-keys \
  --secret-string file://secrets.json \
  --region $REGION

echo "✅ Infrastructure setup complete!"
```

### Phase 3: CI/CD Setup (Week 3)

1. **GitHub Secrets Configuration**
```bash
# Add secrets to GitHub
gh secret set KUBE_CONFIG_PROD < ~/.kube/config
gh secret set AWS_ACCESS_KEY_ID
gh secret set AWS_SECRET_ACCESS_KEY
gh secret set SERPER_API_KEY
gh secret set GEMINI_API_KEY
gh secret set SLACK_WEBHOOK
```

2. **Test CI/CD Pipeline**
```bash
# Push to trigger pipeline
git checkout -b staging
git push origin staging

# Monitor deployment
kubectl get pods -n staging -w
```

### Phase 4: Security Hardening (Week 4)

1. **Enable encryption**
2. **Configure JWT authentication**
3. **Set up WAF rules**
4. **Enable audit logging**
5. **Penetration testing**

### Phase 5: Monitoring Setup (Week 5)

```bash
# Install monitoring stack
kubectl apply -f monitoring/prometheus.yml
kubectl apply -f monitoring/grafana.yml
kubectl apply -f monitoring/alerts.yml

# Access Grafana
kubectl port-forward svc/grafana 3000:3000 -n monitoring
```

### Phase 6: Load Testing (Week 6)

```bash
# Run load tests
locust -f locust/locustfile.py \
  --host=https://staging-api.yourdomain.com \
  --users 1000 \
  --spawn-rate 50 \
  --run-time 10m \
  --headless

# Analyze results
python scripts/analyze_load_test.py
```

### Phase 7: Production Deployment (Week 7)

```bash
# Final production deployment
git checkout main
git merge staging
git push origin main

# Monitor rollout
kubectl rollout status deployment/loan-approval-api -n production

# Run smoke tests
./scripts/smoke-tests.sh production
```

---

## 🛠️ Recommended Tools

### Development
- **Docker**: Containerization
- **Docker Compose**: Local multi-container orchestration
- **pytest**: Testing framework
- **locust**: Load testing

### CI/CD
- **GitHub Actions** (Recommended): Free for public repos, great integration
- **GitLab CI**: Good alternative with built-in container registry
- **CircleCI**: Great for complex pipelines
- **Jenkins**: Self-hosted option

### Infrastructure
- **Terraform**: Infrastructure as Code
- **Kubernetes**: Container orchestration
- **Helm**: Kubernetes package manager
- **ArgoCD**: GitOps continuous delivery

### Monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Jaeger/Zipkin**: Distributed tracing
- **ELK Stack**: Log aggregation (Elasticsearch, Logstash, Kibana)
- **Datadog/New Relic**: All-in-one (paid)

### Security
- **Vault**: Secrets management
- **Trivy**: Container scanning
- **OWASP ZAP**: Security testing
- **SonarQube**: Code quality and security

---

## 💰 Cost Estimation

### AWS Deployment (Production)
```
Component                    Monthly Cost
─────────────────────────────────────────
ECS Fargate (3 containers)   $150
RDS PostgreSQL (db.t3.small) $50
ElastiCache Redis            $30
ALB                          $25
S3 Storage                   $10
CloudWatch Logs              $10
Secrets Manager              $5
Data Transfer                $20
─────────────────────────────────────────
Total:                       ~$300/month
```

### DigitalOcean (Budget Option)
```
Component                    Monthly Cost
─────────────────────────────────────────
Kubernetes (3 nodes)         $60
Managed PostgreSQL           $15
Managed Redis                $15
Load Balancer                $12
Spaces Storage               $5
Monitoring                   $0 (included)
─────────────────────────────────────────
Total:                       ~$107/month
```

---

## 📚 Additional Resources

### Documentation
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [12-Factor App](https://12factor.net/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### Next Steps
1. Choose your cloud platform
2. Set up infrastructure using provided templates
3. Configure CI/CD pipeline
4. Deploy to staging environment
5. Run load tests and optimize
6. Deploy to production
7. Set up monitoring and alerts
8. Document runbooks for common issues

---

**Ready to deploy?** Start with the infrastructure setup scripts in the next section!
