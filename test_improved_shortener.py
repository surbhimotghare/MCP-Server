#!/usr/bin/env python3
"""
Test script for improved URL shortener with custom alias support
"""

import pyshorteners

def test_improved_shortener():
    """Test the improved URL shortener functionality"""
    
    def shorten_url(url: str, custom_alias: str = "") -> str:
        """Shorten a URL using multiple services. Supports custom aliases when available."""
        try:
            # Validate URL format
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Initialize shortener
            shortener = pyshorteners.Shortener()
            
            # Try multiple services in order of preference
            services_to_try = []
            
            if custom_alias:
                # For custom aliases, try services that support them
                services_to_try = [
                    ('isgd', 'Is.gd (with custom alias)'),
                    ('tinyurl', 'TinyURL (fallback)'),
                    ('chilpit', 'Chilp.it (fallback)')
                ]
            else:
                # For basic shortening, use faster services
                services_to_try = [
                    ('tinyurl', 'TinyURL'),
                    ('isgd', 'Is.gd'),
                    ('chilpit', 'Chilp.it')
                ]
            
            last_error = None
            
            for service_name, service_display in services_to_try:
                try:
                    if service_name == 'isgd' and custom_alias:
                        # Is.gd supports custom aliases
                        shortened_url = shortener.isgd.short(url, custom_alias)
                        if shortened_url:
                            result = f"✅ URL successfully shortened with custom alias!\n"
                            result += f"Service: {service_display}\n"
                            result += f"Original: {url}\n"
                            result += f"Shortened: {shortened_url}\n"
                            result += f"Custom alias: {custom_alias}"
                            return result
                    
                    elif service_name == 'tinyurl':
                        # TinyURL basic shortening
                        shortened_url = shortener.tinyurl.short(url)
                        if shortened_url:
                            result = f"✅ URL successfully shortened!\n"
                            result += f"Service: {service_display}\n"
                            result += f"Original: {url}\n"
                            result += f"Shortened: {shortened_url}"
                            if custom_alias:
                                result += f"\nNote: Custom alias '{custom_alias}' not supported by this service"
                            return result
                    
                    elif service_name == 'chilpit':
                        # Chilp.it basic shortening
                        shortened_url = shortener.chilpit.short(url)
                        if shortened_url:
                            result = f"✅ URL successfully shortened!\n"
                            result += f"Service: {service_display}\n"
                            result += f"Original: {url}\n"
                            result += f"Shortened: {shortened_url}"
                            if custom_alias:
                                result += f"\nNote: Custom alias '{custom_alias}' not supported by this service"
                            return result
                            
                except Exception as e:
                    last_error = str(e)
                    continue
            
            # If we get here, all services failed
            if custom_alias:
                return f"❌ Unable to shorten URL with custom alias '{custom_alias}'. All services failed.\nLast error: {last_error}"
            else:
                return f"❌ Unable to shorten URL. All services failed.\nLast error: {last_error}"
                
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
    
    print("🔗 Testing Improved URL Shortener with Custom Alias Support")
    print("=" * 60)
    
    # Test 1: Basic URL shortening without alias
    print("\n1. Testing basic URL shortening:")
    result1 = shorten_url("google.com")
    print(f"Result: {result1}")
    
    # Test 2: URL shortening with custom alias 'mysearch'
    print("\n2. Testing URL shortening with custom alias 'mysearch':")
    result2 = shorten_url("google.com", "mysearch")
    print(f"Result: {result2}")
    
    # Test 3: Test with a different URL and alias
    print("\n3. Testing with github.com and alias 'myrepo':")
    result3 = shorten_url("github.com", "myrepo")
    print(f"Result: {result3}")

if __name__ == "__main__":
    test_improved_shortener() 