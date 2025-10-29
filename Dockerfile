# Dockerfile for UAB RC Docs MCP Server (HTTP/SSE)
# Optimized for Smithery deployment

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

# Install dependencies using uv
RUN uv pip install --system mcp httpx fastmcp

# Copy the server file
COPY uab_docs_server_http.py ./

# Smithery sets PORT environment variable to 8081
# Default to 8081 if PORT is not set
ENV PORT=8081
ENV MCP_SERVER_HOST=0.0.0.0

# Python unbuffered output for better logging
ENV PYTHONUNBUFFERED=1

# Expose the port (Smithery uses 8081)
EXPOSE 8081

# Run the HTTP server
CMD ["python", "uab_docs_server_http.py"]
