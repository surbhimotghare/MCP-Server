from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
import requests
import pyshorteners
from dice_roller import DiceRoller

load_dotenv()

mcp = FastMCP("mcp-server")
client = TavilyClient(os.getenv("TAVILY_API_KEY"))

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
def shorten_url(url: str, custom_alias: str = "") -> str:
    """Shorten a URL using multiple services. Supports custom aliases when available."""
    try:
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # If custom alias is requested, try v.gd first (it supports custom aliases)
        if custom_alias:
            try:
                # v.gd API endpoint for custom aliases
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
                            # Extract just the alias part from the full URL
                            shortened_url = f"https://v.gd/{custom_alias}"
                            result = f"✅ URL successfully shortened with custom alias!\n"
                            result += f"Service: V.gd\n"
                            result += f"Original: {url}\n"
                            result += f"Shortened: {shortened_url}\n"
                            result += f"Custom alias: {custom_alias}"
                            return result
                        elif 'errorcode' in data:
                            if data['errorcode'] == 2:  # Alias already exists
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
                    result = f"✅ URL successfully shortened!\n"
                    result += f"Service: {service_display}\n"
                    result += f"Original: {url}\n"
                    result += f"Shortened: {shortened_url}"
                    return result
                        
            except Exception as e:
                last_error = str(e)
                continue
        
        # If we get here, all services failed
        return f"❌ Unable to shorten URL. All services failed.\nLast error: {last_error}"
                
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")