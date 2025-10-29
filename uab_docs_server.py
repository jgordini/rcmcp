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
import os
import re
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr (required for STDIO servers)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("uab-research-computing-docs")


# Define prompts to help users interact with the server
@mcp.prompt()
def search_cheaha_help(topic: str = "getting started") -> str:
    """
    Search UAB Research Computing documentation for help with a specific topic.
    
    Useful for finding information about Cheaha HPC, SLURM jobs, software,
    storage, and other research computing topics.
    
    Args:
        topic: The topic to search for (default: "getting started")
    
    Returns:
        A prompt to search the documentation
    """
    return f"""Please search the UAB Research Computing documentation for information about '{topic}'. 
Use the search_documentation tool to find relevant pages, then retrieve the full content 
of the most relevant page using get_documentation_page."""


@mcp.prompt()
def how_to_submit_slurm_job() -> str:
    """
    Get help with submitting SLURM jobs on Cheaha HPC cluster.
    
    Provides guidance on creating job scripts, resource requests,
    and best practices for job submission.
    
    Returns:
        A prompt to guide job submission assistance
    """
    return """Please help me understand how to submit a SLURM job on the Cheaha HPC cluster. 
Search the documentation for 'SLURM tutorial' or 'job submission', then provide 
step-by-step guidance including how to create a job script, request resources, 
and submit the job."""


@mcp.prompt()
def find_available_software(software_name: str = "Python") -> str:
    """
    Find information about available software on Cheaha HPC.
    
    Helps users locate and use specific software packages,
    including how to load modules and check versions.
    
    Args:
        software_name: The name of the software to find
    
    Returns:
        A prompt to search for software information
    """
    return f"""Please help me find information about {software_name} on the Cheaha HPC cluster. 
Search the documentation for '{software_name}' and provide information about:
- How to load the module
- Available versions
- Usage examples
- Any special configuration needed"""


@mcp.prompt()
def get_help_and_support() -> str:
    """
    Get information about UAB Research Computing support options.
    
    Provides office hours, contact information, and support channels.
    
    Returns:
        A prompt to retrieve support information
    """
    return """Please provide information about how to get help and support from 
UAB Research Computing, including office hours, contact methods, and the support portal. 
Use the get_support_info tool."""


@mcp.prompt()
def cheaha_getting_started() -> str:
    """
    Get started with Cheaha HPC cluster.
    
    Provides essential information for new users including access,
    basic usage, and key resources.
    
    Returns:
        A prompt to get quick start information
    """
    return """Please provide a quick start guide for using the Cheaha HPC cluster at UAB. 
Include information about access, basic usage, and key topics a new user should learn. 
Use the get_cheaha_quick_start tool."""

# Constants
DOCS_BASE_URL = "https://docs.rc.uab.edu"
RC_BASE_URL = "https://rc.uab.edu"
GITHUB_API_BASE = "https://api.github.com"
GITHUB_REPO = "uabrc/uabrc.github.io"
USER_AGENT = "UAB-RC-MCP-Server/1.0"
GITHUB_TOKEN = os.environ.get(
    "GITHUB_TOKEN"
)  # Optional GitHub token for higher rate limits


def clean_docs_url(url: str) -> str:
    """
    Remove /docs/ path segment from documentation URLs.
    The /docs/ path is part of the GitHub repository structure but not the actual docs site.

    Args:
        url: URL that may contain /docs/ segment

    Returns:
        Cleaned URL with /docs/ removed from the path
    """
    # Remove /docs/ that appears after the domain in the URL path
    # Pattern: https://docs.rc.uab.edu/docs/... -> https://docs.rc.uab.edu/...
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


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
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
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

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
        # Step 1: Remove .md extension
        clean_path = file_path.replace(".md", "")

        # Step 2: Remove README
        clean_path = clean_path.replace("README", "")

        # Step 3: Remove leading 'docs/' if present
        if clean_path.startswith("docs/"):
            clean_path = clean_path[5:]

        # Step 4: Remove trailing slashes
        clean_path = clean_path.rstrip("/")

        # Step 5: Build the URL
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


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
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
        # Extract the file path from GitHub URL if provided
        # Example: https://github.com/uabrc/uabrc.github.io/blob/main/docs/cheaha/slurm/slurm_tutorial.md
        if "github.com" in page_path:
            parts = page_path.split("/blob/")
            if len(parts) > 1:
                # Get everything after /blob/{branch}/
                path_parts = parts[1].split("/", 1)
                if len(path_parts) > 1:
                    page_path = path_parts[1]
                else:
                    return f"Error: Could not extract file path from GitHub URL: {page_path}"
        else:
            return f"Error: URL provided is not a GitHub URL: {page_path}"

    # Clean up the path
    page_path = page_path.lstrip("/")

    # If the path doesn't start with 'docs/', add it
    if not page_path.startswith("docs/"):
        page_path = f"docs/{page_path}"

    # If the path doesn't end with .md, add it
    if not page_path.endswith(".md"):
        page_path = f"{page_path}.md"

    # Construct the raw GitHub content URL
    # Use the default branch (usually 'main' or 'master')
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

    # Generate the docs site URL for reference (without /docs/ in the path)
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


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
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


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
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


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
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
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
