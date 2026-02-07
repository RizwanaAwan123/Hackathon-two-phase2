# Multi-stage build for backend
FROM node:18-alpine AS deps

# Install dependencies
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --only=production

FROM node:18-alpine AS builder
WORKDIR /app
COPY . .
# No build needed for this simple server

FROM node:18-alpine AS runtime

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules

# Copy application code from builder stage
COPY --from=builder --chown=nodejs:nodejs /app . .

# Switch to non-root user
USER nodejs

# Expose port 8000
EXPOSE 8000

# Start the application
CMD ["node", "server.js"]