#!/usr/bin/env python3
"""
UAB Research Computing Documentation MCP Server (Streamable HTTP)
This version uses FastMCP's native streamable_http_app() for Smithery compatibility.
"""

import logging
import httpx
import os
import re
import uvicorn
from typing import Any
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Constants
DOCS_BASE_URL = "https://docs.rc.uab.edu"
RC_BASE_URL = "https://rc.uab.edu"
GITHUB_API_BASE = "https://api.github.com"
GITHUB_REPO = "uabrc/uabrc.github.io"
USER_AGENT = "UAB-RC-MCP-Server/1.0"

# Initialize FastMCP server
mcp = FastMCP("uab-research-computing-docs")


def get_github_token() -> str:
    """Get GitHub token from environment."""
    return os.environ.get("GITHUB_TOKEN", "")


def clean_docs_url(url: str) -> str:
    """
    Remove /docs/ path segment from documentation URLs.
    The /docs/ path is part of the GitHub repository structure but not the actual docs site.

    Args:
        url: URL that may contain /docs/ segment

    Returns:
        Cleaned URL with /docs/ removed from the path
    """
    return re.sub(r"(https://docs\.rc\.uab\.edu)/docs/", r"\1/", url)


async def make_http_request(
    url: str, headers: dict[str, str] | None = None
) -> dict[str, Any] | str | None:
    """Make an HTTP request with proper error handling."""
    default_headers = {"User-Agent": USER_AGENT}
    if headers:
        default_headers.update(headers)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url, headers=default_headers, timeout=30.0, follow_redirects=True
            )
            response.raise_for_status()

            # Try to parse as JSON, otherwise return text
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                return response.json()
            else:
                return response.text
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            logger.error(f"Error making request to {url}: {e}")
            return None


@mcp.tool()
async def search_documentation(query: str, max_results: int = 5) -> str:
    """
    Search the UAB Research Computing documentation for relevant content.

    This tool searches through the documentation repository to find pages
    that match the search query. Useful for finding information about:
    - How to use Cheaha HPC cluster
    - Research computing policies and procedures
    - Getting support and office hours
    - Software and tools available
    - Storage and data management

    Args:
        query: The search term or phrase to look for in the documentation
        max_results: Maximum number of results to return (default: 5, max: 10)

    Returns:
        Formatted search results with titles, URLs, and excerpts
    """
    max_results = min(max_results, 10)  # Cap at 10 results

    # Use GitHub API to search the repository
    search_url = f"{GITHUB_API_BASE}/search/code"
    params = {"q": f"{query} repo:{GITHUB_REPO}", "per_page": max_results}

    headers = {"Accept": "application/vnd.github.v3+json"}
    
    # Get token from environment
    github_token = get_github_token()
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                search_url,
                params=params,
                headers={**headers, "User-Agent": USER_AGENT},
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error searching documentation: {e.response.status_code} - {e.response.text}"
            )
            if e.response.status_code == 401:
                return "Error: GitHub API authentication failed. Set GITHUB_TOKEN environment variable for authenticated access."
            elif e.response.status_code == 403:
                return "Error: GitHub API rate limit exceeded. Set GITHUB_TOKEN environment variable for higher rate limits."
            return f"Error searching documentation: HTTP {e.response.status_code}"
        except Exception as e:
            logger.error(f"Error searching documentation: {e}")
            return f"Error searching documentation: {str(e)}"

    if not data.get("items"):
        return f"No results found for '{query}' in the UAB Research Computing documentation."

    results = []
    results.append(f"Found {data.get('total_count', 0)} results for '{query}':\n")

    for i, item in enumerate(data["items"][:max_results], 1):
        file_name = item.get("name", "Unknown")
        file_path = item.get("path", "")
        html_url = item.get("html_url", "")

        # Convert GitHub file path to docs URL
        clean_path = file_path.replace(".md", "").replace("README", "")
        if clean_path.startswith("docs/"):
            clean_path = clean_path[5:]
        clean_path = clean_path.rstrip("/")
        doc_url = f"{DOCS_BASE_URL}/{clean_path}"

        result_entry = f"""
{i}. **{file_name}**
   URL: {doc_url}
   Repository: {html_url}
   Path: {file_path}
"""
        results.append(result_entry)

    results.append(
        f"\n💡 Tip: Use the 'get_documentation_page' tool to retrieve the full content of a specific page."
    )

    return "\n".join(results)


@mcp.tool()
async def get_documentation_page(page_path: str) -> str:
    """
    Retrieve the full content of a specific documentation page.

    This tool fetches the complete markdown content of a documentation page from the
    UAB Research Computing GitHub repository. Use this after finding a relevant
    page with the search tool.

    Args:
        page_path: The path to the documentation page (e.g., "docs/cheaha/slurm/slurm_tutorial.md" or "cheaha/slurm/slurm_tutorial")
                  Can be a relative path from the repository root or a GitHub URL

    Returns:
        The full markdown content of the documentation page
    """
    # Handle GitHub URLs
    if page_path.startswith("http"):
        if "github.com" in page_path:
            parts = page_path.split("/blob/")
            if len(parts) > 1:
                path_parts = parts[1].split("/", 1)
                if len(path_parts) > 1:
                    page_path = path_parts[1]
                else:
                    return f"Error: Could not extract file path from GitHub URL: {page_path}"
        else:
            return f"Error: URL provided is not a GitHub URL: {page_path}"

    # Clean up the path
    page_path = page_path.lstrip("/")
    if not page_path.startswith("docs/"):
        page_path = f"docs/{page_path}"
    if not page_path.endswith(".md"):
        page_path = f"{page_path}.md"

    # Construct the raw GitHub content URL
    raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{page_path}"
    logger.info(f"Fetching documentation from: {raw_url}")

    # Try to fetch the page content
    content = await make_http_request(raw_url)

    if content is None:
        # Try with 'master' branch if 'main' fails
        raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/{page_path}"
        logger.info(f"Retrying with master branch: {raw_url}")
        content = await make_http_request(raw_url)

        if content is None:
            return f"Error: Unable to fetch content from GitHub. The file may not exist at path: {page_path}"

    if isinstance(content, dict):
        return f"Error: Received JSON instead of markdown content. This shouldn't happen with raw.githubusercontent.com"

    # Generate the docs site URL for reference
    display_path = page_path.replace("docs/", "", 1).replace(".md", "").rstrip("/")
    docs_site_url = f"{DOCS_BASE_URL}/{display_path}"

    # Return the content with metadata
    result = f"""# Documentation Page: {page_path}
**URL:** {docs_site_url}

---

{content}

---

**Source:** UAB Research Computing Documentation
**Base URL:** {DOCS_BASE_URL}
"""

    return result


@mcp.tool()
async def get_support_info() -> str:
    """
    Get information about how to get support from UAB Research Computing.

    This tool provides contact information, office hours, and support channels
    for UAB Research Computing services.

    Returns:
        Comprehensive support information including office hours, contact methods,
        and links to support resources
    """
    support_info = f"""
# UAB Research Computing Support Information

## Primary Documentation Site
{DOCS_BASE_URL}

## Cheaha Access Portal
{RC_BASE_URL}

## Getting Support

The UAB Research Computing team provides support through multiple channels:

### Office Hours
Visit the documentation site for current office hours information:
{DOCS_BASE_URL}/help/office_hours

### Support Portal
For technical support, questions, and issues:
{DOCS_BASE_URL}/help/support

### Contributing to Documentation
If you'd like to contribute to improving the documentation:
{DOCS_BASE_URL}/contributing/contributor_guide/

## Quick Links

- **Main Documentation:** {DOCS_BASE_URL}
- **Cheaha Login:** {RC_BASE_URL}
- **Getting Started Guides:** {DOCS_BASE_URL}/getting-started/
- **Software Documentation:** {DOCS_BASE_URL}/software/
- **Storage & Data:** {DOCS_BASE_URL}/storage/

## About UAB Research Computing

UAB Research Computing is part of UAB IT, with a mission to serve and support
the UAB Research Community with all of their research computing and data needs.

Services include:
- High-Performance Computing (Cheaha cluster)
- Data storage and management
- Research software support
- Consultation and training
- Cloud computing integration

For the most up-to-date information, always refer to the official documentation
at {DOCS_BASE_URL}
"""

    return support_info


@mcp.tool()
async def list_documentation_sections() -> str:
    """
    List the main sections and categories available in the UAB Research Computing documentation.

    This tool provides an overview of the documentation structure to help users
    understand what information is available.

    Returns:
        A structured list of main documentation sections and their purposes
    """
    sections = f"""
# UAB Research Computing Documentation Structure

The documentation is organized into the following main sections:

## 1. Getting Started
Learn the basics of using UAB Research Computing resources
- Introduction to Cheaha
- Account setup and access
- First steps tutorials
- Basic HPC concepts

## 2. Help & Support
Get assistance with your research computing needs
- Office hours schedule
- Support portal and ticketing
- Contact information
- FAQ and troubleshooting

## 3. Software & Applications
Information about available software and tools
- Installed software catalog
- Module system (Lmod)
- Custom software installation
- Containers (Singularity/Apptainer)
- Licensed software access

## 4. Storage & Data Management
Managing your research data
- Storage systems overview
- Quota and allocations
- Data transfer methods
- Backup and archival
- Data security and compliance

## 5. Job Scheduling (SLURM)
Running computational jobs on Cheaha
- SLURM basics and commands
- Job submission scripts
- Resource requests
- Queue policies
- Job arrays and dependencies

## 6. Best Practices
Guidelines for effective use of research computing resources
- Workflow optimization
- Resource efficiency
- Reproducible research
- Collaboration and sharing

## 7. Contributing
How to contribute to the documentation
- Contributor guide
- Documentation standards
- Submitting changes

## Quick Access

- **Main Site:** {DOCS_BASE_URL}
- **Cheaha Portal:** {RC_BASE_URL}
- **GitHub Repository:** https://github.com/{GITHUB_REPO}

Use the 'search_documentation' tool to find specific topics within these sections,
or 'get_documentation_page' to retrieve full content from a specific page.
"""

    return sections


@mcp.tool()
async def get_cheaha_quick_start() -> str:
    """
    Get quick start information for accessing and using the Cheaha HPC cluster.

    This tool provides essential information for new users getting started with
    the Cheaha high-performance computing cluster at UAB.

    Returns:
        Quick start guide with essential information for Cheaha access and basic usage
    """
    quick_start = f"""
# Cheaha HPC Quick Start Guide

## What is Cheaha?

Cheaha is the University of Alabama at Birmingham's high-performance computing (HPC)
cluster, providing powerful computational resources for research.

## Getting Started

### 1. Account Creation
- Visit the account creation page to set up your Cheaha account
- All researchers receive 5 TB of individual storage

### 2. Access Methods

**Primary Access - Web Portal (Recommended)**
The easiest way to access Cheaha is through the Open OnDemand web portal:
**{RC_BASE_URL}**

Requirements:
- UAB credentials 
- Duo 2-Factor Authentication

**Alternative - SSH Access**
For command-line access:
```bash
ssh YOUR_BLAZERID@cheaha.rc.uab.edu
```
(Connect to port 22)

### 3. Interactive Applications Available
Once logged in through the web portal, you can access:
- **File Browser** - Manage your files
- **Remote Desktop** - Full desktop environment
- **Jupyter Notebook/Lab** - Interactive computing
- **RStudio** - R development environment
- **MATLAB** - Mathematical computing

## Important Usage Guidelines

⚠️ **Critical Rule**: Do not run compute-intensive tasks on login nodes
- Always use SLURM job scheduler for computational work
- Choose appropriate partition based on your needs

## Compute Partitions

### GPU Processing
- **pascalnodes** - Pascal GPU nodes
- **amperenodes** - Ampere GPU nodes

### General Purpose
- **amd-hdr100** - General computing

### Time-based Partitions
- **express** - Short jobs
- **short** - Short-term computing
- **medium** - Medium-term jobs  
- **long** - Long-running jobs

### Specialized
- **largemem** - High memory requirements

## Software Access

- Software available through the **module system**
- **Anaconda recommended** for package management
- Need help with software? Submit a support ticket

## Getting Support

### Documentation Home
{DOCS_BASE_URL}

### Support Channels
- Office Hours: {DOCS_BASE_URL}/help/office_hours
- Support Portal: {DOCS_BASE_URL}/help/support

## Next Steps

Use the MCP tools to explore specific topics:
- `search_documentation("slurm tutorial")` - Learn job submission
- `search_documentation("modules")` - Software module system
- `search_documentation("partitions")` - Compute node details
- `search_documentation("storage")` - Data management

**Quick Tip**: Always submit computational jobs through SLURM to utilize compute nodes effectively.

For the most current information, always refer to {DOCS_BASE_URL}
"""

    return quick_start


def main():
    """Initialize and run the MCP server with streamable HTTP transport."""
    logger.info("Starting UAB Research Computing Documentation MCP Server")
    logger.info("Using FastMCP native streamable HTTP")
    
    # Create streamable HTTP app
    app = mcp.streamable_http_app()
    
    # Add CORS middleware for browser-based clients
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["mcp-session-id", "mcp-protocol-version"],
        max_age=86400,
    )
    
    # Get port from environment (Smithery sets PORT=8081)
    port = int(os.environ.get("PORT", "8081"))
    
    logger.info(f"Server will listen on http://0.0.0.0:{port}")
    logger.info("MCP endpoint will be available at http://0.0.0.0:{port}/mcp")
    
    # Run with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


if __name__ == "__main__":
    main()
