FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container
COPY . /app

# Instal the application dependencies
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN uv sync --frozen --no-cache --compile-bytecode

# Run the application
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]