# Dockerfile for React frontend
FROM node:22

# Set the working directory
WORKDIR /app

# Install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy the rest of the application code
COPY frontend .
