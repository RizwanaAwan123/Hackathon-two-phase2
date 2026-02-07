# Quickstart Guide: Cloud Native Todo Chatbot – Phase IV

**Feature**: 001-cloud-native-todo
**Date**: 2026-02-05

## Overview
This guide will help you quickly deploy the Todo Chatbot application to your local Kubernetes cluster using Minikube and Helm.

## Prerequisites
- Docker Desktop running
- Minikube installed and configured
- Helm installed
- kubectl installed and configured
- kubectl-ai and kagent (optional, for advanced operations)

## Steps to Deploy

### 1. Start Minikube
```bash
minikube start
```

### 2. Navigate to Helm Chart Directory
```bash
cd path/to/todo-chatbot-chart
```

### 3. Install the Helm Chart
```bash
helm install todo-chatbot .
```

### 4. Verify the Installation
```bash
kubectl get pods
kubectl get services
```

### 5. Access the Application
```bash
minikube service todo-chatbot-frontend --url
```

## Using AI-Assisted Tools

### With kubectl-ai
```bash
# Analyze pod status
kubectl ai explain pods

# Get scaling recommendations
kubectl ai recommend autoscale
```

### With kagent
```bash
# Analyze cluster state
kagent analyze
```

## Troubleshooting
- If services aren't starting, check: `kubectl get events`
- To view logs: `kubectl logs deployment/todo-chatbot-backend`
- To debug networking: `kubectl port-forward service/todo-chatbot-frontend 8080:80`