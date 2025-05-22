# Stage 1 - Build Vite React app
FROM node:20.10 AS frontend

WORKDIR /app

# Copy package.json and package-lock.json (if present)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all the frontend code
COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}
# Build the React app
RUN npm run build

# Stage 2 - Serve the build using NGINX
FROM nginx:alpine

# Copy the build output from the 'frontend' stage to the NGINX server's public directory
COPY --from=frontend /app/dist /usr/share/nginx/html

# Expose the port that NGINX will listen on (default is 80)
EXPOSE 80

# Start the NGINX server
CMD ["nginx", "-g", "daemon off;"]

