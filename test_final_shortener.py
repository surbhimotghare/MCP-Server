#!/usr/bin/env python3
"""
Final test for the improved URL shortener with custom alias support
"""

import time

def test_final_shortener():
    """Test the final URL shortener implementation"""
    
    # Import the function from our server
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from server import shorten_url
    
    print("🔗 Testing Final URL Shortener with Custom Alias Support")
    print("=" * 60)
    
    # Test 1: Basic URL shortening without alias
    print("\n1. Testing basic URL shortening:")
    result1 = shorten_url("google.com")
    print(f"Result: {result1}")
    
    # Test 2: URL shortening with custom alias (using timestamp to make it unique)
    print("\n2. Testing URL shortening with custom alias:")
    unique_alias = f"mysearch{int(time.time())}"
    result2 = shorten_url("google.com", unique_alias)
    print(f"Result: {result2}")
    
    # Test 3: Test with a different URL and unique alias
    print("\n3. Testing with github.com and unique alias:")
    unique_alias2 = f"myrepo{int(time.time())}"
    result3 = shorten_url("github.com", unique_alias2)
    print(f"Result: {result3}")
    
    # Test 4: Test with an existing alias (should fail gracefully)
    print("\n4. Testing with existing alias 'test' (should fail gracefully):")
    result4 = shorten_url("google.com", "test")
    print(f"Result: {result4}")

if __name__ == "__main__":
    test_final_shortener() 