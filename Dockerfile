FROM python:3.11-slim

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY r.txt .
RUN pip install --no-cache-dir -r r.txt

# Copy project
COPY . .

# Make entrypoint executable
RUN chmod +x django_entrypoint.sh

EXPOSE 8000
