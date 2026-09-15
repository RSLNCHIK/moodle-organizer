# React build
# This Dockerfile is used to build a React application and serve it using Nginx. It consists of two stages: the build stage and the production stage.
# FROM node:22-alpine AS build is the first stage of the Dockerfile, which uses the official Node.js 22 Alpine image as the base image. This stage is responsible for building the React application.
# we use it to install the dependencies and build the application. AS build is used to name this stage "build" so that we can reference it later in the production stage.
FROM node:22-alpine AS build

# WORKDIR /app sets the working directory inside the container to /app. All subsequent commands will be run from this directory.
WORKDIR /app

# COPY package*.json ./ copies the package.json and package-lock.json files from the host machine to the working directory inside the container. These files contain the list of dependencies required for the React application.
COPY package*.json ./

# ARG VITE_API_URL is used to define a build-time variable that can be passed to the Docker build command. This variable is used to set the API URL for the React application.
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}

# RUN npm ci is used to install the dependecies listed in the package-lock.json file. The npm ci command is preferred for CI/CD pipelines because it installs dependiencies faster and ensures a clean installation by removing the node_modules folder before installing.
RUN npm ci

# COPY . . copies the rest of the application code from the host machine to the working directory inside the container.
COPY . .

# ARG VITE_API_URL is used to define a build-time variable that can be passed to the Docker build command. This variable is used to set the API URL for the React application.
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build

# FROM nginx:alpine is the second stage of the Dockerfile, which uses the official Nginx Alpine image as the base image. This stage is responsible for serving the built React application.
FROM nginx:alpine

# COPY nginx.conf /etc/nginx/conf.d/default.conf copies the custom Nginx configuration file from the host machine to the default Nginx configuration directory inside the container. This configuration file is used to set up the Nginx server to serve the React application.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# COPY --from=build /app/dist /usr/share/nginx/html copies the built React application from the build stage to the Nginx HTML directory inside the container. This allows Nginx to serve the React application when the container is run.
COPY --from=build /app/dist /usr/share/nginx/html

# EXPOSE 80 informs Docker that the container will listen on port 80 at runtime. This is the default port for HTTP traffic, and it allows external clients to access the React application served by Nginx.
EXPOSE 80

