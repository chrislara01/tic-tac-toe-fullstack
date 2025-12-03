# syntax=docker/dockerfile:1

# Build stage
FROM node:20-alpine AS build
WORKDIR /app

# Enable corepack (pnpm)
RUN corepack enable

# Copy lockfiles and manifest first for better caching
COPY package.json pnpm-lock.yaml ./

# Install deps
RUN pnpm install --frozen-lockfile

# Copy source
COPY . .

# Build with Vite; allow overriding API base via build arg
ARG VITE_API_BASE_URL=/api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN pnpm run build

# Runtime stage: Nginx to serve the static app and proxy /api to backend
FROM nginx:alpine AS runtime

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
