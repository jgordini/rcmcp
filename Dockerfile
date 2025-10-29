# Dockerfile for UAB RC Docs MCP Server (Smithery)
# Optimized for Smithery deployment with streamable HTTP support

# Use Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Install the project into /app
WORKDIR /app

# Enable bytecode compilation for better performance
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Copy dependency files first for better layer caching
COPY pyproject.toml ./

# Install dependencies using uv - including smithery SDK
RUN uv pip install --system mcp httpx smithery pydantic

# Copy the server file
COPY uab_docs_server_smithery.py ./

# Smithery sets PORT environment variable to 8081
ENV PORT=8081

# Python unbuffered output for better logging
ENV PYTHONUNBUFFERED=1

# Expose the port (Smithery uses 8081)
EXPOSE 8081

# Run the Smithery-compatible server
CMD ["python", "uab_docs_server_smithery.py"]
