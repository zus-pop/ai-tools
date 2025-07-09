FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create a non-root user
RUN groupadd --gid 1000 zus && \
    useradd --uid 1000 --gid zus --shell /bin/bash --create-home zus

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Create app directory and set ownership
RUN mkdir -p /app && chown -R zus:zus /app    

# Copy the application into the container
COPY --chown=zus:zus . /app

# Switch to non-root user
USER zus

# Instal the application dependencies
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1

RUN uv sync --frozen --no-cache --compile-bytecode

# Run the application
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
# CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]