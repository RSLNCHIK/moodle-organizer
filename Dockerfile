# FROM python:3.12-slim is used to specify the base image for the Docker container.
# The base image is a lightweight version of Python 3.12, which is suitable for running Python applications in a containerized environment.
FROM python:3.12-slim

# Set the working directory inside the container to /app.
# This is where the application code and dependencies will be placed.
WORKDIR /app

# COPY the requirements file to the working directory
# This is necessary to install the dependencies listed in the requirements.txt file
COPY requirements.txt .

# Install the dependencies from the requirements.txt file
# The --no-cache-dir option is used to prevent pip from caching the packages, which can save space in the Docker image
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# CMD specifies the command to run when the container starts. 
# In this case, it runs the uvicorn server to serve the FastAPI application defined in app/api.py.
# The --host option is set to "0.0.0.0" and the --port option is set to "8000" to make the application accessible from outside the container.
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]

