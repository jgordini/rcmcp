#!/usr/bin/env python3
"""
Simple test script for the UAB Research Computing Documentation MCP Server.

This script tests the basic functionality of the MCP server by calling its tools directly.
Run this to verify that the server is working correctly before connecting it to Claude Desktop.
"""

import asyncio
import sys
from uab_docs_server import (
    search_documentation,
    get_documentation_page,
    get_support_info,
    list_documentation_sections,
    get_cheaha_quick_start
)


async def test_all_tools():
    """Test all available MCP tools."""
    
    print("=" * 80)
    print("UAB Research Computing Documentation MCP Server - Test Suite")
    print("=" * 80)
    print()
    
    # Test 1: Search Documentation
    print("TEST 1: Searching documentation for 'slurm'")
    print("-" * 80)
    result = await search_documentation("slurm", max_results=3)
    print(result)
    print()
    
    # Test 2: Get Support Info
    print("TEST 2: Getting support information")
    print("-" * 80)
    result = await get_support_info()
    print(result)
    print()
    
    # Test 3: List Documentation Sections
    print("TEST 3: Listing documentation sections")
    print("-" * 80)
    result = await list_documentation_sections()
    print(result)
    print()
    
    # Test 4: Get Cheaha Quick Start
    print("TEST 4: Getting Cheaha quick start guide")
    print("-" * 80)
    result = await get_cheaha_quick_start()
    print(result)
    print()
    
    # Test 5: Get Documentation Page (example)
    print("TEST 5: Getting a documentation page (if available)")
    print("-" * 80)
    print("Note: This test may fail if the exact page doesn't exist.")
    result = await get_documentation_page("getting-started")
    print(result[:500] + "..." if len(result) > 500 else result)
    print()
    
    print("=" * 80)
    print("All tests completed!")
    print("=" * 80)
    print()
    print("If you see results above without errors, the server is working correctly.")
    print("You can now configure it in Claude Desktop using the instructions in README.md")


async def run_interactive_test():
    """Run an interactive test allowing the user to try different searches."""
    
    print("=" * 80)
    print("UAB Research Computing Documentation MCP Server - Interactive Test")
    print("=" * 80)
    print()
    print("This interactive test allows you to try different search queries.")
    print("Type 'quit' or 'exit' to stop.")
    print()
    
    while True:
        try:
            query = input("Enter a search query (or 'quit' to exit): ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Exiting interactive test.")
                break
            
            if not query:
                print("Please enter a search query.")
                continue
            
            print()
            print(f"Searching for: '{query}'")
            print("-" * 80)
            
            result = await search_documentation(query, max_results=5)
            print(result)
            print()
            
        except KeyboardInterrupt:
            print("\nExiting interactive test.")
            break
        except Exception as e:
            print(f"Error: {e}")
            print()


def print_usage():
    """Print usage information."""
    print("Usage: python test_server.py [mode]")
    print()
    print("Modes:")
    print("  all         - Run all automated tests (default)")
    print("  interactive - Run interactive test mode")
    print("  help        - Show this help message")
    print()
    print("Examples:")
    print("  python test_server.py")
    print("  python test_server.py all")
    print("  python test_server.py interactive")


async def main():
    """Main entry point for the test script."""
    
    mode = "all"
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    
    if mode == "help":
        print_usage()
        return
    
    if mode == "interactive":
        await run_interactive_test()
    else:
        await test_all_tools()


if __name__ == "__main__":
    asyncio.run(main())
