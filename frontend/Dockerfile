# frontend/Dockerfile

# --- Stage 1: Build the application ---
# UPDATED: Use a newer version of Node.js that is compatible with Vite
FROM node:20-alpine AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json for dependency installation
COPY package*.json ./

# Install all project dependencies
RUN npm install

# Copy the rest of your application's source code
COPY . .

# Build the application for production. Vite builds to a 'dist' folder.
RUN npm run build


# --- Stage 2: Serve the application using Nginx ---
# Use a tiny, official Nginx image for the final production image
FROM nginx:stable-alpine

# Copy the static build files from the 'builder' stage to Nginx's web root
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx listens on port 80 by default, so we expose it
EXPOSE 80