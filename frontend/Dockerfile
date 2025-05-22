# Use a lightweight Python base image
FROM python:3.9-slim AS builder

# Set the working directory inside the container
WORKDIR /app/frontend

# Copy only the requirements file to leverage Docker's caching mechanism
COPY requiremints.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requiremints.txt

# Copy only necessary frontend files to the container
COPY . .

# Use a lightweight runtime image to reduce final image size
FROM python:3.9-slim

# Set the working directory
WORKDIR /app/frontend

# Copy only installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app/frontend /app/frontend

# Expose the Streamlit port
EXPOSE 8501

# Run Streamlit on the specified port and bind address
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
