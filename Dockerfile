# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder

# Install build-time dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install only Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final image
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN useradd --system --no-create-home exporter

WORKDIR /app

# Copy installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy your application code
COPY exporter.py .
COPY openvpn_collector.py .

# Drop privileges
USER exporter

# Run the exporter
ENTRYPOINT ["python", "exporter.py"]
