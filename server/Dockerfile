# Use Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY uv.lock .
COPY src/ ./src/
COPY settings.toml .

# Install dependencies using uv
RUN uv sync --frozen

# Expose port
EXPOSE 8002

# Run the application
CMD ["uv", "run", "uvicorn", "src.app.api:app", "--host", "0.0.0.0", "--port", "8002"]
