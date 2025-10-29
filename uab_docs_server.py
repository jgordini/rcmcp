#!/usr/bin/env python3
"""
UAB Research Computing Documentation MCP Server

This MCP server provides access to the University of Alabama at Birmingham's
Research Computing documentation, allowing AI assistants to search and retrieve
relevant information about UAB's research computing resources, including:
- Cheaha HPC cluster documentation
- Getting support and office hours
- Contributing to documentation
- Research computing services

Homepage: https://docs.rc.uab.edu
"""

from typing import Any
import logging
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr (required for STDIO servers)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("uab-research-computing-docs")

# Constants
DOCS_BASE_URL = "https://docs.rc.uab.edu"
RC_BASE_URL = "https://rc.uab.edu"
GITHUB_API_BASE = "https://api.github.com"
GITHUB_REPO = "uabrc/uabrc.github.io"
USER_AGENT = "UAB-RC-MCP-Server/1.0"


async def make_http_request(url: str, headers: dict[str, str] | None = None) -> dict[str, Any] | str | None:
    """Make an HTTP request with proper error handling."""
    default_headers = {"User-Agent": USER_AGENT}
    if headers:
        default_headers.update(headers)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=default_headers, timeout=30.0, follow_redirects=True)
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
    params = {
        "q": f"{query} repo:{GITHUB_REPO}",
        "per_page": max_results
    }
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                search_url,
                params=params,
                headers={**headers, "User-Agent": USER_AGENT},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
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
        # The repo structure typically has docs in specific folders
        doc_url = f"{DOCS_BASE_URL}/{file_path.replace('.md', '').replace('README', '')}"
        
        result_entry = f"""
{i}. **{file_name}**
   URL: {doc_url}
   Repository: {html_url}
   Path: {file_path}
"""
        results.append(result_entry)
    
    results.append(f"\n💡 Tip: Use the 'get_documentation_page' tool to retrieve the full content of a specific page.")
    
    return "\n".join(results)


@mcp.tool()
async def get_documentation_page(page_path: str) -> str:
    """
    Retrieve the full content of a specific documentation page.
    
    This tool fetches the complete content of a documentation page from the
    UAB Research Computing documentation site. Use this after finding a relevant
    page with the search tool.
    
    Args:
        page_path: The path to the documentation page (e.g., "getting-started/intro" or "storage/data-management")
                  Can be a relative path from docs.rc.uab.edu or a full URL
    
    Returns:
        The full content of the documentation page in markdown format
    """
    # Handle both full URLs and relative paths
    if page_path.startswith("http"):
        url = page_path
    else:
        # Remove leading slash if present
        page_path = page_path.lstrip("/")
        url = f"{DOCS_BASE_URL}/{page_path}"
    
    # Try to fetch the page content
    content = await make_http_request(url)
    
    if content is None:
        return f"Error: Unable to fetch content from {url}. The page may not exist or there may be a network issue."
    
    if isinstance(content, dict):
        return f"Error: Received JSON instead of page content. URL may be incorrect: {url}"
    
    # Return the content with metadata
    result = f"""
# Documentation Page: {page_path}
**URL:** {url}

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

## Accessing Cheaha

### Web Portal
The easiest way to access Cheaha is through the web portal:
**{RC_BASE_URL}**

### SSH Access
For command-line access:
```bash
ssh YOUR_BLAZERID@cheaha.rc.uab.edu
```

## Key Resources

### Documentation Home
{DOCS_BASE_URL}

### Getting Support
- Office Hours: {DOCS_BASE_URL}/help/office_hours
- Support Portal: {DOCS_BASE_URL}/help/support

### Essential Topics to Explore

1. **Account Setup**
   - Learn about access requirements and account creation
   - Search documentation for: "account setup"

2. **Job Submission with SLURM**
   - Understand how to submit computational jobs
   - Search documentation for: "SLURM tutorial" or "job submission"

3. **Software Modules**
   - Learn how to load software with the module system
   - Search documentation for: "modules" or "software"

4. **Storage Systems**
   - Understand available storage options and quotas
   - Search documentation for: "storage" or "data management"

5. **Best Practices**
   - Learn how to use resources efficiently
   - Search documentation for: "best practices"

## Next Steps

Use the MCP tools to explore specific topics:
- `search_documentation("slurm tutorial")` - Learn about job submission
- `search_documentation("python")` - Find Python-related resources
- `search_documentation("gpu")` - Information about GPU computing
- `list_documentation_sections()` - See all available topics

## Need Help?

The UAB Research Computing team is here to support you:
- Check office hours for live assistance
- Submit a support ticket for technical issues
- Review the documentation for guides and tutorials

For the most current information, always refer to {DOCS_BASE_URL}
"""
    
    return quick_start


def main():
    """Initialize and run the MCP server."""
    logger.info("Starting UAB Research Computing Documentation MCP Server")
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
