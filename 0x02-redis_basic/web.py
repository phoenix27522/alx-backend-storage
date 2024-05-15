#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
from functools import lru_cache
from threading import Timer

# Dictionary to track URL access counts
url_access_count = {}


def clear_cache(url):
    """Clear cache for the specified URL."""
    global url_access_count
    del url_access_count[url]


def reset_access_count(url):
    """Reset access count for the specified URL."""
    global url_access_count
    url_access_count[url] = 0


@lru_cache(maxsize=None, typed=False)
def get_page(url):
    """Fetch HTML content of the specified URL."""
    global url_access_count

    # Increment access count for this URL
    url_access_count[url] = url_access_count.get(url, 0) + 1

    # Schedule cache clearance after 10 seconds
    Timer(10, clear_cache, args=[url]).start()

    # Fetch HTML content
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Test the get_page function
    url = "http://slowwly.robertomurray.co.uk/delay/10000/url/http://www.example.com"
    html_content = get_page(url)
    print(html_content)

    # Wait for 12 seconds to see if cache is cleared
    import time
    time.sleep(12)

    # Access the same URL again
    html_content_cached = get_page(url)
    print(html_content_cached)

    # Reset access count for testing
    reset_access_count(url)
