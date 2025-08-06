#!/usr/bin/env python3
'''
test_headers.py - Test script for the Headers class in darkdump

This script demonstrates all the functionality of the enhanced Headers class,
including getting random user agents, filtering by browser type or OS, and
accessing modern user agents.

Usage:
    python test_headers.py

Author: Josh Schiavone (Enhanced by Factory AI)
License: MIT
'''

import sys
import random
from headers.agents import Headers

def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_example(description, value):
    """Print an example with description and value."""
    print(f"\n{description}:")
    print(f"  {value}")

def test_random_agents():
    """Demonstrate getting random user agents."""
    print_header("RANDOM USER AGENTS")
    
    # Get a single random user agent
    print_example("Random user agent", Headers.get_random_agent())
    
    # Get multiple random user agents
    print("\nMultiple random user agents:")
    for i in range(3):
        print(f"  {i+1}. {Headers.get_random_agent()}")

def test_browser_specific_agents():
    """Demonstrate getting browser-specific user agents."""
    print_header("BROWSER-SPECIFIC USER AGENTS")
    
    browsers = ['chrome', 'firefox', 'ie', 'edge', 'opera', 'safari', 'mobile']
    
    for browser in browsers:
        print_example(f"Random {browser.upper()} user agent", Headers.get_random_by_browser(browser))
    
    # Demonstrate error handling with an invalid browser type
    print("\nError handling with invalid browser type:")
    try:
        Headers.get_random_by_browser('invalid_browser')
    except ValueError as e:
        print(f"  Error: {e}")

def test_os_specific_agents():
    """Demonstrate getting OS-specific user agents."""
    print_header("OS-SPECIFIC USER AGENTS")
    
    os_types = ['windows', 'mac', 'linux', 'android', 'ios']
    
    for os_type in os_types:
        print_example(f"Random {os_type.upper()} user agent", Headers.get_random_by_os(os_type))
    
    # Demonstrate error handling with an invalid OS type
    print("\nError handling with invalid OS type:")
    try:
        Headers.get_random_by_os('invalid_os')
    except ValueError as e:
        print(f"  Error: {e}")

def test_modern_agents():
    """Demonstrate getting modern user agents."""
    print_header("MODERN USER AGENTS")
    
    print_example("Random modern user agent", Headers.get_modern_agent())
    
    print("\nMultiple modern user agents:")
    for i in range(3):
        print(f"  {i+1}. {Headers.get_modern_agent()}")

def test_direct_access():
    """Demonstrate direct access to user agent lists."""
    print_header("DIRECT ACCESS TO USER AGENT LISTS")
    
    # Show total counts of user agents by category
    print("\nTotal user agents by category:")
    print(f"  All user agents: {len(Headers.user_agents)}")
    print(f"  Chrome agents: {len(Headers.chrome_agents)}")
    print(f"  Firefox agents: {len(Headers.firefox_agents)}")
    print(f"  IE/Edge agents: {len(Headers.ie_edge_agents)}")
    print(f"  Opera agents: {len(Headers.opera_agents)}")
    print(f"  Safari agents: {len(Headers.safari_agents)}")
    print(f"  Mobile agents: {len(Headers.mobile_agents)}")
    
    # Show a random example from each category
    print("\nRandom examples from each category:")
    print(f"  Chrome: {random.choice(Headers.chrome_agents)}")
    print(f"  Firefox: {random.choice(Headers.firefox_agents)}")
    print(f"  IE/Edge: {random.choice(Headers.ie_edge_agents)}")
    print(f"  Opera: {random.choice(Headers.opera_agents)}")
    print(f"  Safari: {random.choice(Headers.safari_agents)}")
    print(f"  Mobile: {random.choice(Headers.mobile_agents)}")

def test_practical_usage():
    """Demonstrate practical usage in HTTP requests."""
    print_header("PRACTICAL USAGE IN HTTP REQUESTS")
    
    print("""
# Example of using Headers with the requests library:

import requests
from headers.agents import Headers

# Get a random Chrome user agent
headers = {'User-Agent': Headers.get_random_by_browser('chrome')}

# Make a request with the Chrome user agent
response = requests.get('https://example.com', headers=headers)

# For scraping that requires modern browsers
headers = {'User-Agent': Headers.get_modern_agent()}
response = requests.get('https://example.com', headers=headers)

# For mobile-specific content
headers = {'User-Agent': Headers.get_random_by_browser('mobile')}
response = requests.get('https://example.com', headers=headers)
""")

def main():
    """Run all test functions."""
    print("\nTesting the Headers class functionality from darkdump\n")
    
    test_random_agents()
    test_browser_specific_agents()
    test_os_specific_agents()
    test_modern_agents()
    test_direct_access()
    test_practical_usage()
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    main()
