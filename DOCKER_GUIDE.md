# 🐳 Docker Deployment Guide

## Quick Start with Docker

### Prerequisites
- Docker installed and running
- Docker Compose (optional, but recommended)

### 🚀 Option 1: Using Docker Compose (Recommended)

#### 1. Build and Start
```bash
cd /home/labuser/loan_approval
docker-compose up -d --build
```

#### 2. View Logs
```bash
docker-compose logs -f
```

#### 3. Stop the Application
```bash
docker-compose down
```

#### 4. Stop and Remove All Data
```bash
docker-compose down -v
```

### 🐳 Option 2: Using Docker Commands

#### 1. Build the Image
```bash
docker build -t loan-approval-system:latest .
```

#### 2. Run the Container
```bash
docker run -d \
  --name loan_approval \
  -p 8000:8000 \
  -e SERPER_API_KEY=db9ed35c9262af6e3e4bada7fbfb1102d5565564 \
  -e GEMINI_API_KEY=your_gemini_key_here \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/loan_approval.db:/app/loan_approval.db \
  --restart unless-stopped \
  loan-approval-system:latest
```

#### 3. View Logs
```bash
docker logs -f loan_approval
```

#### 4. Stop the Container
```bash
docker stop loan_approval
docker rm loan_approval
```

### 📊 Access the Application

Once running, access:
- **UI**: http://localhost:8000/
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 🔧 Useful Docker Commands

#### Check Container Status
```bash
docker ps
```

#### View Container Logs
```bash
docker logs loan_approval
docker logs -f loan_approval  # Follow logs
```

#### Execute Commands in Container
```bash
docker exec -it loan_approval bash
```

#### Restart Container
```bash
docker restart loan_approval
```

#### Check Health Status
```bash
docker inspect --format='{{json .State.Health}}' loan_approval | python -m json.tool
```

#### Remove Image
```bash
docker rmi loan-approval-system:latest
```

#### Clean Up Everything
```bash
docker system prune -a --volumes
```

### 🌐 Deploy to Cloud

#### Docker Hub
```bash
# Tag image
docker tag loan-approval-system:latest your-username/loan-approval-system:latest

# Push to Docker Hub
docker push your-username/loan-approval-system:latest

# Pull and run on any server
docker pull your-username/loan-approval-system:latest
docker run -d -p 8000:8000 your-username/loan-approval-system:latest
```

#### AWS EC2 / Azure VM / GCP Compute Engine
1. Install Docker on the VM
2. Clone your repository or pull Docker image
3. Run using docker-compose or docker run commands above
4. Configure security groups to allow port 8000

### 📦 What's Included

The Docker setup includes:
- ✅ Python 3.10 slim base image
- ✅ All dependencies from requirements.txt
- ✅ FastAPI application with all agents
- ✅ SQLite database persistence
- ✅ Health check endpoint monitoring
- ✅ Automatic restart on failure
- ✅ Volume mounting for data persistence

### 🔒 Environment Variables

Create a `.env` file or pass environment variables:
```env
SERPER_API_KEY=your_serper_key
GEMINI_API_KEY=your_gemini_key
```

### 🐛 Troubleshooting

#### Container won't start
```bash
docker logs loan_approval
```

#### Permission issues with volumes
```bash
sudo chown -R $USER:$USER data/
sudo chown -R $USER:$USER *.db
```

#### Port already in use
```bash
# Use different port
docker run -p 8080:8000 ...
```

#### Database issues
```bash
# Remove database and restart fresh
rm loan_approval.db
docker-compose up -d
```

### 🎯 Production Deployment Tips

1. **Use environment variables** for sensitive data
2. **Set up SSL/TLS** with reverse proxy (nginx)
3. **Enable logging** to external service
4. **Monitor health checks** with orchestration tools
5. **Scale horizontally** using Docker Swarm or Kubernetes
6. **Backup database** regularly from volume mounts

### 📈 Scaling with Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml loan-approval

# Scale service
docker service scale loan-approval_loan-approval-api=3

# View services
docker service ls
```

### ☸️ Kubernetes Deployment

Convert docker-compose to Kubernetes manifests:
```bash
kompose convert -f docker-compose.yml
kubectl apply -f .
```

---

For more information, see the main [README.md](README.md)
