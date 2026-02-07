#!/bin/bash

# Cloud Native Todo Chatbot - Phase IV Deployment Script
# This script deploys the Todo Chatbot application to Minikube

set -e  # Exit on any error

echo "🚀 Starting Cloud Native Todo Chatbot Deployment..."

# Function to check if a command exists
command_exists() {
    command -v "$@" > /dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."
if ! command_exists minikube; then
    echo "❌ Minikube is not installed. Please install Minikube first."
    exit 1
fi

if ! command_exists helm; then
    echo "❌ Helm is not installed. Please install Helm first."
    exit 1
fi

if ! command_exists kubectl; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

if ! command_exists docker; then
    echo "❌ Docker is not installed or not running. Please start Docker first."
    exit 1
fi

# Start Minikube if not running
echo "🔄 Checking Minikube status..."
MINIKUBE_STATUS=$(minikube status --format='{{.Host}}')
if [ "$MINIKUBE_STATUS" != "Running" ]; then
    echo "🔧 Starting Minikube cluster..."
    minikube start --cpus=2 --memory=4096
else
    echo "✅ Minikube is already running"
fi

# Set Docker environment to Minikube
echo "🐳 Setting Docker environment to Minikube..."
eval $(minikube docker-env)

# Build Docker images
echo "📦 Building Docker images..."
echo "Building frontend image..."
docker build -t todo-frontend:latest ./frontend

echo "Building backend image..."
docker build -t todo-backend:latest ./backend

# Verify images were built
if ! docker images | grep -q "todo-frontend"; then
    echo "❌ Frontend image was not built successfully"
    exit 1
fi

if ! docker images | grep -q "todo-backend"; then
    echo "❌ Backend image was not built successfully"
    exit 1
fi

echo "✅ Docker images built successfully"

# Install Helm charts
echo " Charts..."
helm uninstall todo-frontend 2>/dev/null || true
helm uninstall todo-backend 2>/dev/null || true

echo "Installing backend chart..."
helm install todo-backend ./helm/backend-chart

echo "Installing frontend chart..."
helm install todo-frontend ./helm/frontend-chart

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=backend-chart --timeout=300s
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=frontend-chart --timeout=300s

# Verify services are running
echo "✅ Verifying services..."
kubectl get services
kubectl get pods

# Show access URL
echo "🌐 Application is now available!"
echo "Backend API: $(minikube service todo-backend-backend-chart --url)"
echo "Frontend UI: $(minikube service todo-frontend-frontend-chart --url)"

echo "💡 To access the application, visit the frontend UI URL in your browser."

# Check for kubectl-ai and kagent
if command_exists kubectl-ai; then
    echo "🤖 kubectl-ai is available. You can use it for analysis:"
    echo "   kubectl ai explain deployments"
    echo "   kubectl ai pods-status"
    echo "   kubectl ai recommend autoscale"
fi

if command_exists kagent; then
    echo "🤖 kagent is available. You can use it for cluster analysis:"
    echo "   kagent analyze"
    echo "   kagent health"
    echo "   kagent recommend"
fi

echo "🎉 Deployment completed successfully!"
echo "To verify everything is working:"
echo "1. Visit the frontend URL in your browser"
echo "2. Test the chatbot functionality"
echo "3. Check pod status: kubectl get pods"
echo "4. Check service status: kubectl get services"

# Option to open dashboard
read -p "Do you want to open the Minikube dashboard? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    minikube dashboard
fi