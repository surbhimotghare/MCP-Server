from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
import requests
import pyshorteners
from dice_roller import DiceRoller
from enhanced_url_tools import EnhancedURLTools
from url_storage import URLStorage
import json
from typing import List

load_dotenv()

mcp = FastMCP("mcp-server")
client = TavilyClient(os.getenv("TAVILY_API_KEY"))

# Initialize enhanced URL tools
url_tools = EnhancedURLTools()
url_storage = URLStorage()

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    search_results = client.get_search_context(query=query)
    return search_results

@mcp.tool()
def roll_dice(notation: str, num_rolls: int = 1) -> str:
    """Roll the dice with the given notation"""
    roller = DiceRoller(notation, num_rolls)
    return str(roller)

@mcp.tool()
def shorten_url(url: str, custom_alias: str = "", collection_name: str = "", tags: str = "") -> str:
    """Shorten a URL using multiple services. Supports custom aliases and collections."""
    try:
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Get metadata for the URL
        metadata = url_tools.get_url_metadata(url)
        
        # Check URL safety
        safety_check = url_tools.check_url_safety(url)
        
        # If custom alias is requested, try v.gd first
        service_used = "Unknown"
        shortened_url = ""
        
        if custom_alias:
            try:
                api_url = "https://v.gd/create.php"
                params = {
                    'url': url,
                    'shorturl': custom_alias,
                    'format': 'json'
                }
                
                response = requests.get(api_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'shorturl' in data:
                            shortened_url = f"https://v.gd/{custom_alias}"
                            service_used = "V.gd"
                        elif 'errorcode' in data:
                            if data['errorcode'] == 2:
                                return f"❌ Custom alias '{custom_alias}' already exists. Please choose a different alias."
                            else:
                                return f"❌ V.gd service error: {data.get('errormessage', 'Unknown error')}"
                    except:
                        return f"❌ Invalid response from V.gd service: {response.text}"
                else:
                    return f"❌ HTTP Error {response.status_code} from V.gd service"
                    
            except Exception as e:
                return f"❌ Error with V.gd service: {str(e)}"
        
        # For basic shortening (no custom alias), use multiple services as fallback
        if not shortened_url:
            shortener = pyshorteners.Shortener()
            services_to_try = [
                ('tinyurl', 'TinyURL'),
                ('chilpit', 'Chilp.it'),
                ('vgd', 'V.gd')
            ]
            
            last_error = None
            
            for service_name, service_display in services_to_try:
                try:
                    if service_name == 'tinyurl':
                        shortened_url = shortener.tinyurl.short(url)
                    elif service_name == 'chilpit':
                        shortened_url = shortener.chilpit.short(url)
                    elif service_name == 'vgd':
                        shortened_url = shortener.vgd.short(url)
                    else:
                        continue
                    
                    if shortened_url:
                        service_used = service_display
                        break
                            
                except Exception as e:
                    last_error = str(e)
                    continue
            
            if not shortened_url:
                return f"❌ Unable to shorten URL. All services failed.\nLast error: {last_error}"
        
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
        
        # Save to database
        url_id = url_storage.save_url(
            original=url,
            shortened=shortened_url,
            custom_alias=custom_alias,
            title=metadata.get('title', ''),
            description=metadata.get('description', ''),
            tags=tag_list,
            collection_name=collection_name,
            service_used=service_used,
            is_safe=safety_check.get('is_safe', True),
            metadata=metadata
        )
        
        # Format response
        result = f"✅ URL successfully shortened!\n"
        result += f"Service: {service_used}\n"
        result += f"Original: {url}\n"
        result += f"Shortened: {shortened_url}\n"
        
        if custom_alias:
            result += f"Custom alias: {custom_alias}\n"
        
        if metadata.get('title'):
            result += f"Title: {metadata['title']}\n"
        
        if collection_name:
            result += f"Collection: {collection_name}\n"
        
        if tag_list:
            result += f"Tags: {', '.join(tag_list)}\n"
        
        if not safety_check.get('is_safe', True):
            result += f"⚠️ Safety warnings: {', '.join(safety_check.get('warnings', []))}\n"
        
        result += f"Saved to database with ID: {url_id}"
        
        return result
                
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

@mcp.tool()
def shorten_url_batch(urls: str, collection_name: str = "", tags: str = "") -> str:
    """Shorten multiple URLs at once. Separate URLs with newlines or commas."""
    try:
        # Parse URLs - support both newline and comma separation
        url_list = []
        if '\n' in urls:
            url_list = [url.strip() for url in urls.split('\n') if url.strip()]
        else:
            url_list = [url.strip() for url in urls.split(',') if url.strip()]
        
        if not url_list:
            return "❌ No valid URLs provided"
        
        if len(url_list) > 20:
            return "❌ Too many URLs. Maximum 20 URLs per batch."
        
        results = []
        success_count = 0
        
        for i, url in enumerate(url_list, 1):
            try:
                result = shorten_url(url, collection_name=collection_name, tags=tags)
                if "✅" in result:
                    success_count += 1
                    # Extract just the shortened URL from the result
                    lines = result.split('\n')
                    shortened = next((line.split(': ', 1)[1] for line in lines if line.startswith('Shortened:')), 'N/A')
                    results.append(f"{i}. {url} → {shortened}")
                else:
                    results.append(f"{i}. {url} → ERROR: {result}")
            except Exception as e:
                results.append(f"{i}. {url} → ERROR: {str(e)}")
        
        summary = f"📊 Batch URL Shortening Complete!\n"
        summary += f"✅ Successfully shortened: {success_count}/{len(url_list)} URLs\n"
        if collection_name:
            summary += f"📁 Collection: {collection_name}\n"
        if tags:
            summary += f"🏷️ Tags: {tags}\n"
        summary += "\n📋 Results:\n" + '\n'.join(results)
        
        return summary
        
    except Exception as e:
        return f"❌ Batch processing error: {str(e)}"

@mcp.tool()
def validate_url(url: str) -> str:
    """Validate if a URL is properly formatted and reachable"""
    try:
        result = url_tools.validate_url(url)
        
        if result.get('is_valid'):
            status = "✅ URL is valid"
            if result.get('is_reachable'):
                status += " and reachable"
            else:
                status += " but not reachable"
            
            response = f"{status}\n"
            response += f"Original URL: {result.get('original_url')}\n"
            response += f"Final URL: {result.get('final_url')}\n"
            response += f"Status Code: {result.get('status_code')}\n"
            
            if result.get('redirected'):
                response += "🔄 URL redirects to a different location\n"
            
            return response
        else:
            return f"❌ URL validation failed: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"❌ Validation error: {str(e)}"

@mcp.tool()
def get_url_metadata(url: str) -> str:
    """Extract metadata from a URL including title, description, and other information"""
    try:
        metadata = url_tools.get_url_metadata(url)
        
        if 'error' in metadata:
            return f"❌ Failed to extract metadata: {metadata['error']}"
        
        result = f"📄 URL Metadata\n"
        result += f"URL: {metadata.get('url', 'N/A')}\n"
        result += f"Title: {metadata.get('title', 'No title found')}\n"
        result += f"Description: {metadata.get('description', 'No description found')}\n"
        result += f"Domain: {metadata.get('domain', 'N/A')}\n"
        result += f"Secure (HTTPS): {'Yes' if metadata.get('is_secure') else 'No'}\n"
        result += f"Content Type: {metadata.get('content_type', 'N/A')}\n"
        result += f"Content Length: {metadata.get('content_length', 0)} bytes\n"
        
        if metadata.get('favicon_url'):
            result += f"Favicon: {metadata['favicon_url']}\n"
        
        if metadata.get('image_url'):
            result += f"Preview Image: {metadata['image_url']}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Metadata extraction error: {str(e)}"

@mcp.tool()
def check_url_safety(url: str) -> str:
    """Check if a URL is safe and identify potential security risks"""
    try:
        safety_result = url_tools.check_url_safety(url)
        
        if 'error' in safety_result:
            return f"❌ Safety check failed: {safety_result['error']}"
        
        result = f"🔒 URL Safety Report\n"
        result += f"URL: {safety_result.get('url', 'N/A')}\n"
        result += f"Domain: {safety_result.get('domain', 'N/A')}\n"
        result += f"Risk Level: {safety_result.get('risk_level', 'unknown').upper()}\n"
        
        if safety_result.get('is_safe'):
            result += "✅ URL appears to be safe\n"
        else:
            result += "⚠️ URL has potential safety concerns\n"
        
        warnings = safety_result.get('warnings', [])
        if warnings:
            result += "\n🚨 Warnings:\n"
            for warning in warnings:
                result += f"• {warning}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Safety check error: {str(e)}"

@mcp.tool()
def generate_qr_code(url: str, size: int = 10) -> str:
    """Generate a QR code for a URL and return it as base64 encoded image"""
    try:
        qr_result = url_tools.generate_qr_code(url, size)
        
        if 'error' in qr_result:
            return f"❌ QR code generation failed: {qr_result['error']}"
        
        result = f"📱 QR Code Generated\n"
        result += f"URL: {qr_result.get('url', 'N/A')}\n"
        result += f"Format: {qr_result.get('format', 'N/A')}\n"
        result += f"Size: {qr_result.get('size', 'N/A')}\n"
        result += f"\n🖼️ QR Code (Base64):\n"
        result += f"data:image/png;base64,{qr_result.get('qr_code_base64', '')}"
        
        return result
        
    except Exception as e:
        return f"❌ QR code generation error: {str(e)}"

@mcp.tool()
def expand_url(shortened_url: str) -> str:
    """Expand a shortened URL to see its final destination"""
    try:
        expand_result = url_tools.expand_url(shortened_url)
        
        if 'error' in expand_result:
            return f"❌ URL expansion failed: {expand_result['error']}"
        
        result = f"🔗 URL Expansion\n"
        result += f"Original: {expand_result.get('original_shortened', 'N/A')}\n"
        result += f"Final URL: {expand_result.get('final_url', 'N/A')}\n"
        result += f"Redirects: {expand_result.get('redirect_count', 0)}\n"
        result += f"Status Code: {expand_result.get('status_code', 'N/A')}\n"
        
        if expand_result.get('redirect_chain'):
            result += "\n🔄 Redirect Chain:\n"
            for i, redirect_url in enumerate(expand_result['redirect_chain'], 1):
                result += f"{i}. {redirect_url}\n"
        
        return result
        
    except Exception as e:
        return f"❌ URL expansion error: {str(e)}"

@mcp.tool()
def create_url_collection(name: str, description: str = "") -> str:
    """Create a new URL collection for organizing shortened URLs"""
    try:
        success = url_storage.create_collection(name, description)
        
        if success:
            result = f"✅ Collection created successfully!\n"
            result += f"Name: {name}\n"
            if description:
                result += f"Description: {description}\n"
            return result
        else:
            return f"❌ Collection '{name}' already exists"
            
    except Exception as e:
        return f"❌ Collection creation error: {str(e)}"

@mcp.tool()
def list_my_urls(collection: str = "", tags: str = "", limit: int = 20) -> str:
    """List saved URLs with optional filtering by collection or tags"""
    try:
        # Parse tags if provided
        tag_list = [tag.strip() for tag in tags.split(",")] if tags else None
        
        urls = url_storage.get_urls(
            collection=collection if collection else None,
            tags=tag_list,
            limit=limit
        )
        
        if not urls:
            return "📝 No URLs found matching your criteria"
        
        result = f"📋 Your Saved URLs ({len(urls)} found)\n"
        
        if collection:
            result += f"🗂️ Collection: {collection}\n"
        if tags:
            result += f"🏷️ Tags: {tags}\n"
        
        result += "\n"
        
        for i, url_data in enumerate(urls, 1):
            result += f"{i}. {url_data.get('title', 'No title')}\n"
            result += f"   🔗 {url_data.get('shortened_url', 'N/A')}\n"
            result += f"   📍 Original: {url_data.get('original_url', 'N/A')}\n"
            
            if url_data.get('collection_name'):
                result += f"   🗂️ Collection: {url_data['collection_name']}\n"
            
            if url_data.get('tags'):
                try:
                    tag_data = json.loads(url_data['tags']) if isinstance(url_data['tags'], str) else url_data['tags']
                    if tag_data:
                        result += f"   🏷️ Tags: {', '.join(tag_data)}\n"
                except:
                    pass
            
            result += f"   📅 Created: {url_data.get('created_at', 'N/A')}\n"
            result += "\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error retrieving URLs: {str(e)}"

@mcp.tool()
def search_urls(search_term: str, limit: int = 20) -> str:
    """Search through saved URLs by title, description, or original URL"""
    try:
        urls = url_storage.search_urls(search_term, limit)
        
        if not urls:
            return f"🔍 No URLs found matching '{search_term}'"
        
        result = f"🔍 Search Results for '{search_term}' ({len(urls)} found)\n\n"
        
        for i, url_data in enumerate(urls, 1):
            result += f"{i}. {url_data.get('title', 'No title')}\n"
            result += f"   🔗 {url_data.get('shortened_url', 'N/A')}\n"
            result += f"   📍 Original: {url_data.get('original_url', 'N/A')}\n"
            
            if url_data.get('description'):
                result += f"   📝 {url_data['description'][:100]}...\n"
            
            result += f"   📅 Created: {url_data.get('created_at', 'N/A')}\n"
            result += "\n"
        
        return result
        
    except Exception as e:
        return f"❌ Search error: {str(e)}"

@mcp.tool()
def list_collections() -> str:
    """List all URL collections"""
    try:
        collections = url_storage.get_collections()
        
        if not collections:
            return "📁 No collections found"
        
        result = f"📁 Your Collections ({len(collections)} found)\n\n"
        
        for i, collection in enumerate(collections, 1):
            result += f"{i}. {collection.get('name', 'Unnamed')}\n"
            if collection.get('description'):
                result += f"   📝 {collection['description']}\n"
            result += f"   📅 Created: {collection.get('created_at', 'N/A')}\n"
            result += "\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error retrieving collections: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")