#!/usr/bin/env python3
"""
Direct test for custom alias functionality
"""

import requests
import time

def test_custom_alias_direct():
    """Test custom alias functionality directly with different services"""
    
    print("🔗 Testing Custom Alias Support Directly")
    print("=" * 50)
    
    # Test 1: Try v.gd service with unique alias
    print("\n1. Testing v.gd service with unique custom alias:")
    try:
        # v.gd API endpoint
        url = "https://google.com"
        # Use timestamp to make alias unique
        unique_alias = f"mysearch{int(time.time())}"
        
        # v.gd uses a different format
        api_url = "https://v.gd/create.php"
        params = {
            'url': url,
            'shorturl': unique_alias,
            'format': 'json'
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if 'shorturl' in data:
                    print(f"✅ Success! Shortened URL: https://v.gd/{data['shorturl']}")
                    print(f"Custom alias used: {unique_alias}")
                else:
                    print(f"❌ Error: {data}")
            except:
                print(f"Response: {response.text}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Try is.gd service with unique alias
    print("\n2. Testing is.gd service with unique custom alias:")
    try:
        url = "https://google.com"
        unique_alias = f"mysearch{int(time.time())}"
        
        api_url = "https://is.gd/create.php"
        params = {
            'url': url,
            'shorturl': unique_alias,
            'format': 'json'
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if 'shorturl' in data:
                    print(f"✅ Success! Shortened URL: https://is.gd/{data['shorturl']}")
                    print(f"Custom alias used: {unique_alias}")
                else:
                    print(f"❌ Error: {data}")
            except:
                print(f"Response: {response.text}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_custom_alias_direct() 