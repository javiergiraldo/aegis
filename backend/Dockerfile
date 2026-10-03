FROM python:3.12-slim

WORKDIR /app

# Install system dependencies if required (e.g., for psycopg2)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Run ASGI server with socket.io support
CMD ["uvicorn", "src.main:socket_app", "--host", "0.0.0.0", "--port", "8000"]
