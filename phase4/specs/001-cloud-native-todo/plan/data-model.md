# Data Model: Cloud Native Todo Chatbot – Phase IV

**Feature**: 001-cloud-native-todo
**Date**: 2026-02-05

## Entity 1: Todo Chatbot Application

### Description
The complete application consisting of frontend UI and backend API components that work together to provide todo management functionality with chatbot interface.

### Attributes
- Name: "Todo Chatbot"
- Version: Application version identifier
- Components: List of constituent services (frontend, backend)

### Relationships
- Contains -> Frontend Service
- Contains -> Backend Service
- Depends on -> Database (if applicable)

## Entity 2: Frontend Service

### Description
Containerized web interface that allows users to interact with the Todo Chatbot through a graphical user interface.

### Attributes
- Type: Web application
- Technology: HTML/CSS/JavaScript framework (e.g., React, Vue, Angular)
- Port: HTTP port number for web access
- Environment Variables:
  - BACKEND_API_URL: URL of the backend API service
  - NODE_ENV: Environment mode (development/production)

### Relationships
- Communicates with -> Backend Service
- Serves -> End Users

## Entity 3: Backend Service

### Description
Containerized API that manages todo data and chatbot functionality, providing REST endpoints for the frontend.

### Attributes
- Type: REST API service
- Technology: Server-side framework (e.g., Node.js/Express, Python/FastAPI, Java/Spring Boot)
- Port: HTTP port number for API access
- Environment Variables:
  - DATABASE_URL: Connection string for data persistence
  - PORT: Internal port for service access
  - JWT_SECRET: Secret for authentication tokens

### Relationships
- Serves -> Frontend Service
- Stores/reads -> Todo Data
- Authenticates -> Users (if applicable)

## Entity 4: Helm Chart

### Description
Packaged Kubernetes application manifest that enables easy deployment and management of the Todo Chatbot application.

### Attributes
- Chart Name: Identifier for the Helm chart
- Version: Semantic version of the chart
- AppVersion: Version of the application being deployed
- Values: Configurable parameters for customization
- Templates: Kubernetes manifest templates

### Relationships
- Deploys -> Todo Chatbot Application
- Manages -> Kubernetes Resources

## Entity 5: Minikube Cluster

### Description
Local Kubernetes environment for development and testing of the Todo Chatbot application.

### Attributes
- Provider: Local Kubernetes distribution
- Resources: CPU, Memory, Storage capacity
- Addons: Enabled Kubernetes addons (dashboard, ingress, etc.)

### Relationships
- Hosts -> Todo Chatbot Application
- Managed by -> kubectl