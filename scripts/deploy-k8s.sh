#!/bin/bash
# Quick deployment script for Kubernetes

set -e

echo "🚀 Deploying Loan Approval System to Kubernetes"
echo "================================================"
echo ""

# Variables
NAMESPACE="${1:-production}"
ENVIRONMENT="${2:-production}"

echo "📋 Configuration:"
echo "  Namespace: $NAMESPACE"
echo "  Environment: $ENVIRONMENT"
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

# Check cluster connection
echo "🔍 Checking cluster connection..."
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster"
    echo "   Please configure your kubeconfig file"
    exit 1
fi
echo "✅ Connected to cluster"
echo ""

# Create namespace if it doesn't exist
echo "📦 Creating namespace: $NAMESPACE"
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
echo ""

# Apply secrets (you should create this from the template first)
echo "🔐 Applying secrets..."
if [ -f "kubernetes/secrets.yaml" ]; then
    kubectl apply -f kubernetes/secrets.yaml -n $NAMESPACE
    echo "✅ Secrets applied"
else
    echo "⚠️  Warning: kubernetes/secrets.yaml not found"
    echo "   Please create it from kubernetes/secrets-template.yaml"
    echo "   and add your actual secrets"
fi
echo ""

# Apply deployment
echo "🚢 Deploying application..."
kubectl apply -f kubernetes/deployment.yaml -n $NAMESPACE
echo "✅ Deployment applied"
echo ""

# Wait for rollout to complete
echo "⏳ Waiting for rollout to complete..."
kubectl rollout status deployment/loan-approval-api -n $NAMESPACE --timeout=5m
echo "✅ Rollout complete"
echo ""

# Show deployment status
echo "📊 Deployment Status:"
kubectl get deployments -n $NAMESPACE -l app=loan-approval
echo ""

echo "🔍 Pods:"
kubectl get pods -n $NAMESPACE -l app=loan-approval
echo ""

echo "🌐 Services:"
kubectl get svc -n $NAMESPACE -l app=loan-approval
echo ""

# Get the service URL
echo "📍 Access Information:"
SERVICE_TYPE=$(kubectl get svc loan-approval-service -n $NAMESPACE -o jsonpath='{.spec.type}')

if [ "$SERVICE_TYPE" == "LoadBalancer" ]; then
    echo "   Service Type: LoadBalancer"
    echo "   Fetching external IP..."
    
    # Wait for external IP (max 2 minutes)
    for i in {1..24}; do
        EXTERNAL_IP=$(kubectl get svc loan-approval-service -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
        if [ -n "$EXTERNAL_IP" ] && [ "$EXTERNAL_IP" != "null" ]; then
            echo "   ✅ External IP: http://$EXTERNAL_IP"
            break
        fi
        echo "   Waiting for external IP... ($i/24)"
        sleep 5
    done
    
    if [ -z "$EXTERNAL_IP" ] || [ "$EXTERNAL_IP" == "null" ]; then
        echo "   ⚠️  External IP not yet assigned. Check with:"
        echo "      kubectl get svc loan-approval-service -n $NAMESPACE"
    fi
elif [ "$SERVICE_TYPE" == "ClusterIP" ]; then
    echo "   Service Type: ClusterIP (internal only)"
    echo "   To access locally, run:"
    echo "      kubectl port-forward svc/loan-approval-service 8000:80 -n $NAMESPACE"
    echo "   Then visit: http://localhost:8000"
fi
echo ""

# Check ingress if exists
if kubectl get ingress loan-approval-ingress -n $NAMESPACE &> /dev/null; then
    echo "🌐 Ingress:"
    kubectl get ingress loan-approval-ingress -n $NAMESPACE
    echo ""
fi

# Test health endpoint
echo "🏥 Testing health endpoint..."
if [ "$SERVICE_TYPE" == "ClusterIP" ]; then
    kubectl run curl-test --image=curlimages/curl:latest --rm -i --restart=Never -n $NAMESPACE -- \
        curl -s http://loan-approval-service/health && echo "✅ Health check passed" || echo "❌ Health check failed"
fi
echo ""

echo "✅ Deployment Complete!"
echo ""
echo "📚 Next Steps:"
echo "   1. Check logs: kubectl logs -f deployment/loan-approval-api -n $NAMESPACE"
echo "   2. View metrics: kubectl top pods -n $NAMESPACE -l app=loan-approval"
echo "   3. Scale deployment: kubectl scale deployment/loan-approval-api --replicas=5 -n $NAMESPACE"
echo "   4. Update image: kubectl set image deployment/loan-approval-api loan-approval=IMAGE:TAG -n $NAMESPACE"
echo ""
echo "🔧 Troubleshooting:"
echo "   - View events: kubectl get events -n $NAMESPACE --sort-by='.lastTimestamp'"
echo "   - Describe pod: kubectl describe pod POD_NAME -n $NAMESPACE"
echo "   - Shell into pod: kubectl exec -it POD_NAME -n $NAMESPACE -- /bin/bash"
echo ""
