# Multi-stage build for frontend
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy frontend files
COPY . .

# No build needed for this simple static site
# If using a build system (React, Vue, etc.), add build commands here
# RUN npm install
# RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built application from builder stage
COPY --from=builder /app /usr/share/nginx/html

# Copy custom nginx configuration to handle SPA routing
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]