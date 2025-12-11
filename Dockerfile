# Frontend Dockerfile: builds Vite app and serves via Nginx with API proxy

# ---- Build stage ----
    FROM node:18-alpine AS build
    WORKDIR /app
    
    # Install deps
    COPY package.json package-lock.json* ./
    RUN npm ci --no-audit --no-fund || npm install
    
    # Copy sources and build
    COPY . .
    ARG VITE_API_URL=/api
    ENV VITE_API_URL=$VITE_API_URL
    RUN npm run build
    
    # ---- Runtime stage ----
    FROM nginx:alpine
    
    # Copy custom nginx config (proxies /api to backend service)
    
    # Copy built assets
    
    EXPOSE 80
    CMD ["nginx", "-g", "daemon off;"]