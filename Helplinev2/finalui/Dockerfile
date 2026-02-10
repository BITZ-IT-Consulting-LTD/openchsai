# Build stage
FROM node:20-alpine as build-stage

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with retry logic
RUN npm ci --prefer-offline --no-audit || \
    npm ci --prefer-offline --no-audit || \
    npm ci --prefer-offline --no-audit

# Copy project files
COPY . .

# Build-time env vars (Vite inlines these at build time)
ARG VITE_DEFAULT_COUNTRY=KE_LOCAL
ARG VITE_SIP_PASS_PREFIX
ENV VITE_DEFAULT_COUNTRY=$VITE_DEFAULT_COUNTRY
ENV VITE_SIP_PASS_PREFIX=$VITE_SIP_PASS_PREFIX

# Generate nginx.conf from taxonomy contract for the selected environment
RUN node scripts/generate-nginx-conf.cjs

# Build the application
RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage

# Copy built assets from build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy generated nginx configuration
COPY --from=build-stage /app/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
