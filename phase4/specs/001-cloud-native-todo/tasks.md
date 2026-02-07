# Tasks: Cloud Native Todo Chatbot – Phase IV

**Feature**: 001-cloud-native-todo
**Created**: 2026-02-05

## Task 1: Environment Verification

**Purpose**: Verify that all required tools (Docker, Minikube, Helm, kubectl) are installed and working properly.

**Commands**:
```bash
# Check Docker installation
docker --version
docker ps

# Check Minikube installation
minikube version

# Check Helm installation
helm version

# Check kubectl installation
kubectl version --client
```

**Expected Result**:
- All commands return version information without errors
- Docker daemon is running (you can see containers if any are running)
- All tools are installed and accessible from the command line

## Task 2: Start Minikube Cluster

**Purpose**: Initialize a local Kubernetes cluster using Minikube to host the Todo Chatbot application.

**Commands**:
```bash
# Start Minikube with adequate resources for our application
minikube start --cpus=2 --memory=4096

# Verify cluster is running
kubectl cluster-info

# Verify nodes are ready
kubectl get nodes
```

**Expected Result**:
- Minikube starts successfully with 2 CPUs and 4GB memory
- `kubectl cluster-info` shows the Kubernetes master address
- `kubectl get nodes` shows one node in "Ready" status

## Task 3: Examine Application Structure

**Purpose**: Identify the frontend and backend application files to understand what needs to be containerized.

**Commands**:
```bash
# Look for common frontend files
ls -la
find . -name "package.json" -o -name "index.html" -o -name "webpack.config.js" -o -name "vite.config.js" -o -name "angular.json" -o -name "app.js"

# Look for common backend files
find . -name "server.js" -o -name "main.py" -o -name "app.py" -o -name "requirements.txt" -o -name "Dockerfile" -o -name "*.yaml" -o -name "*.yml"
```

**Expected Result**:
- Identify frontend application files (likely a client-side app)
- Identify backend application files (likely a server-side app)
- Note any existing Dockerfiles or configuration files

## Task 4: Create Frontend Dockerfile

**Purpose**: Create a Dockerfile for the frontend application to containerize the user interface.

**Commands**:
```bash
# Create a Dockerfile for the frontend application
cat > frontend/Dockerfile << 'EOF'
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF

# Create a simple nginx configuration
cat > frontend/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen 80;
        root /usr/share/nginx/html;
        index index.html index.htm;

        # Serve all routes to index.html for SPA routing
        location / {
            try_files $uri $uri/ /index.html;
        }

        # API proxy to backend
        location /api {
            proxy_pass http://todo-backend:8080;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }
    }
}
EOF
```

**Expected Result**:
- Dockerfile created in the frontend directory
- nginx.conf created with proper configuration for the frontend app
- Dockerfile uses multi-stage build to optimize image size

## Task 5: Create Backend Dockerfile

**Purpose**: Create a Dockerfile for the backend application to containerize the API server.

**Commands**:
```bash
# Create a Dockerfile for the backend application
# This assumes a Node.js backend - modify based on actual technology
cat > backend/Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

# Change ownership
RUN chown -R nodejs:nodejs /app
USER nodejs

EXPOSE 8080

CMD ["node", "server.js"]
EOF
```

**Expected Result**:
- Dockerfile created in the backend directory
- Dockerfile follows security best practices (non-root user)
- Dockerfile uses production dependencies only

## Task 6: Build Docker Images

**Purpose**: Build the Docker images for both frontend and backend applications.

**Commands**:
```bash
# Build frontend image
docker build -t todo-frontend:v1.0 ./frontend

# Build backend image
docker build -t todo-backend:v1.0 ./backend

# Verify images were created
docker images | grep todo-
```

**Expected Result**:
- Two Docker images created: todo-frontend:v1.0 and todo-backend:v1.0
- Both images show in the `docker images` output
- Images build without errors

## Task 7: Test Docker Images Locally

**Purpose**: Test the Docker images locally before deploying to Kubernetes.

**Commands**:
```bash
# Run backend container (in the background)
docker run -d --name test-backend -p 8080:8080 todo-backend:v1.0

# Wait for backend to start
sleep 10

# Run frontend container (in the background)
docker run -d --name test-frontend -p 3000:80 todo-frontend:v1.0

# Wait for frontend to start
sleep 5

# Check running containers
docker ps

# Test the applications
curl http://localhost:8080/api/health || echo "Backend health check not available"
curl http://localhost:3000 || echo "Frontend not accessible"

# Stop and remove test containers
docker stop test-frontend test-backend
docker rm test-frontend test-backend
```

**Expected Result**:
- Both containers start without errors
- Applications are accessible on their respective ports
- Containers stop and remove cleanly

## Task 8: Create Helm Chart Structure

**Purpose**: Set up the Helm chart directory structure for deploying the Todo Chatbot application.

**Commands**:
```bash
# Create Helm chart directory structure
mkdir -p todo-chatbot-chart/{templates,charts}

# Create Chart.yaml file
cat > todo-chatbot-chart/Chart.yaml << 'EOF'
apiVersion: v2
name: todo-chatbot
description: A Helm chart for deploying the Todo Chatbot application
type: application
version: 0.1.0
appVersion: "1.0.0"
EOF

# Create values.yaml with default configuration
cat > todo-chatbot-chart/values.yaml << 'EOF'
# Default values for todo-chatbot
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

replicaCount: 1

imagePullPolicy: IfNotPresent
# Overrides the image tag whose default is the chart appVersion.
imageTag: "v1.0"

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations: {}

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000

service:
  frontendPort: 80
  backendPort: 8080

resources:
  frontend:
    limits:
      cpu: 100m
      memory: 128Mi
    requests:
      cpu: 50m
      memory: 64Mi
  backend:
    limits:
      cpu: 200m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}
EOF
```

**Expected Result**:
- Helm chart directory structure created
- Chart.yaml file contains basic chart information
- values.yaml file contains configurable parameters

## Task 9: Create Frontend Kubernetes Manifests

**Purpose**: Create Kubernetes deployment and service manifests for the frontend application.

**Commands**:
```bash
# Create frontend deployment template
cat > todo-chatbot-chart/templates/frontend-deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend
  labels:
    app: todo-frontend
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: todo-frontend
  template:
    metadata:
      labels:
        app: todo-frontend
    spec:
      containers:
      - name: frontend
        image: "{{ .Values.image.repository }}/todo-frontend:{{ .Values.imageTag }}"
        imagePullPolicy: {{ .Values.imagePullPolicy }}
        ports:
        - containerPort: 80
        env:
        - name: BACKEND_SERVICE_URL
          value: "http://todo-backend:{{ .Values.service.backendPort }}"
        resources:
{{ toYaml .Values.resources.frontend | indent 10 }}
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend
  labels:
    app: todo-frontend
spec:
  type: {{ .Values.service.type }}
  ports:
  - port: {{ .Values.service.frontendPort }}
    targetPort: 80
    protocol: TCP
    name: http
  selector:
    app: todo-frontend
EOF
```

**Expected Result**:
- Frontend deployment manifest created
- Frontend service manifest created
- Template uses Helm values for configuration

## Task 10: Create Backend Kubernetes Manifests

**Purpose**: Create Kubernetes deployment and service manifests for the backend application.

**Commands**:
```bash
# Create backend deployment template
cat > todo-chatbot-chart/templates/backend-deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  labels:
    app: todo-backend
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
    spec:
      containers:
      - name: backend
        image: "{{ .Values.image.repository }}/todo-backend:{{ .Values.imageTag }}"
        imagePullPolicy: {{ .Values.imagePullPolicy }}
        ports:
        - containerPort: {{ .Values.service.backendPort }}
        env:
        - name: PORT
          value: "{{ .Values.service.backendPort }}"
        - name: NODE_ENV
          value: "production"
        resources:
{{ toYaml .Values.resources.backend | indent 10 }}
        livenessProbe:
          httpGet:
            path: /health
            port: {{ .Values.service.backendPort }}
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: {{ .Values.service.backendPort }}
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: todo-backend
  labels:
    app: todo-backend
spec:
  type: ClusterIP
  ports:
  - port: {{ .Values.service.backendPort }}
    targetPort: {{ .Values.service.backendPort }}
    protocol: TCP
    name: http
  selector:
    app: todo-backend
EOF
```

**Expected Result**:
- Backend deployment manifest created
- Backend service manifest created
- Template uses Helm values for configuration

## Task 11: Update Values for Local Deployment

**Purpose**: Update the Helm values to work with local Minikube deployment.

**Commands**:
```bash
# Update values.yaml with proper image repository and service type
cat > temp-values.yaml << 'EOF'
# Image configuration for local development
image:
  repository: ""
  pullPolicy: Never  # Since we're using local images in Minikube

# Service configuration
service:
  type: NodePort  # Use NodePort for local access
  frontendPort: 80
  backendPort: 8080

# Resource limits adjusted for local development
resources:
  frontend:
    limits:
      cpu: 100m
      memory: 128Mi
    requests:
      cpu: 50m
      memory: 64Mi
  backend:
    limits:
      cpu: 200m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi
EOF

# Append the temporary values to the existing values.yaml
cat temp-values.yaml >> todo-chatbot-chart/values.yaml
rm temp-values.yaml
```

**Expected Result**:
- Values updated to work with local Minikube
- Image pull policy set to Never for local images
- Service type set to NodePort for local access

## Task 12: Install Helm Chart

**Purpose**: Deploy the Todo Chatbot application to Minikube using the Helm chart.

**Commands**:
```bash
# Load Docker images into Minikube
eval $(minikube docker-env)
docker build -t todo-frontend:v1.0 ./frontend
docker build -t todo-backend:v1.0 ./backend

# Verify images are in Minikube
docker images | grep todo-

# Install the Helm chart
helm install todo-chatbot ./todo-chatbot-chart

# Wait for deployments to be ready
kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=300s
kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=300s

# Check all resources
kubectl get all
```

**Expected Result**:
- Docker images loaded into Minikube's Docker environment
- Helm chart installed successfully
- Frontend and backend pods are in "Running" and "Ready" status
- All services and deployments show correctly in kubectl get all

## Task 13: Access the Application

**Purpose**: Verify the application is accessible and functioning properly.

**Commands**:
```bash
# Get the service URLs
minikube service todo-frontend --url

# Alternative: Get the NodePort to access via minikube IP
kubectl get svc todo-frontend

# Get minikube IP
minikube ip

# Access the application
FRONTEND_PORT=$(kubectl get svc todo-frontend -o jsonpath='{.spec.ports[0].nodePort}')
MINIKUBE_IP=$(minikube ip)
echo "Access the Todo Chatbot at: http://$MINIKUBE_IP:$FRONTEND_PORT"
```

**Expected Result**:
- URL to access the frontend application is displayed
- Application loads in the browser
- Both frontend and backend communicate properly

## Task 14: Using kubectl-ai for Analysis

**Purpose**: Use kubectl-ai to analyze the running application and get insights.

**Commands**:
```bash
# Check if kubectl-ai is installed
kubectl ai --help

# Analyze the current state of deployments
kubectl ai explain deployments

# Get insights about resource usage
kubectl ai resource-usage

# Analyze pod status
kubectl ai pods-status

# Get scaling recommendations
kubectl ai recommend autoscale
```

**Expected Result**:
- kubectl-ai commands execute without errors
- Insights about the application state are provided
- Recommendations for optimization are given

## Task 15: Using kagent for Cluster Analysis

**Purpose**: Use kagent to analyze the Kubernetes cluster state and performance.

**Commands**:
```bash
# Check if kagent is installed
kagent --help

# Run a cluster analysis
kagent analyze

# Get cluster health status
kagent health

# Get recommendations for improving cluster performance
kagent recommend
```

**Expected Result**:
- kagent commands execute without errors
- Cluster analysis report is generated
- Recommendations for cluster optimization are provided

## Task 16: Test Application Functionality

**Purpose**: Verify that the Todo Chatbot application works as expected in the Kubernetes environment.

**Commands**:
```bash
# Get pod names for checking logs
kubectl get pods

# Check frontend logs
kubectl logs -l app=todo-frontend

# Check backend logs
kubectl logs -l app=todo-backend

# Forward a local port to the backend to test API directly
kubectl port-forward svc/todo-backend 8081:8080 &
PORT_FORWARD_PID=$!

# Test backend API
sleep 5
curl -v http://localhost:8081/health

# Clean up port forward
kill $PORT_FORWARD_PID

# Scale the frontend to 2 replicas
kubectl scale deployment todo-frontend --replicas=2

# Wait for scaling to complete
kubectl get pods
kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=300s
```

**Expected Result**:
- Logs show normal application startup
- Backend API responds to health check
- Frontend deployment scales to 2 replicas successfully
- New pods reach "Ready" status

## Task 17: Troubleshooting Common Issues

**Purpose**: Learn how to troubleshoot common problems with the Kubernetes deployment.

**Commands**:
```bash
# Check for any failed pods
kubectl get pods --field-selector=status.phase!=Running

# Check for any failed events
kubectl get events --sort-by='.lastTimestamp'

# Get detailed pod information
kubectl describe pod -l app=todo-frontend
kubectl describe pod -l app=todo-backend

# Get detailed service information
kubectl describe service todo-frontend
kubectl describe service todo-backend

# Exec into a pod to check configuration
kubectl exec -it deployment/todo-frontend -- env
kubectl exec -it deployment/todo-backend -- env
```

**Expected Result**:
- Any potential issues are identified through event logs
- Detailed information about pods and services is displayed
- Environment variables inside containers can be inspected

## Task 18: Cleanup

**Purpose**: Clean up resources when finished testing or when starting over.

**Commands**:
```bash
# Uninstall the Helm release
helm uninstall todo-chatbot

# Verify resources are deleted
kubectl get all

# Stop Minikube
minikube stop

# Optionally, delete the Minikube VM to free up resources
# minikube delete
```

**Expected Result**:
- Helm release is uninstalled
- All application resources are deleted from Kubernetes
- Minikube cluster is stopped