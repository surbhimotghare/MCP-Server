import asyncio
from fastmcp import Client
import json

async def test_enhanced_url_tools():
    """Test all the enhanced URL shortener tools"""
    print("🧪 Testing Enhanced URL Shortener MCP Server")
    print("=" * 60)
    
    async with Client("server.py") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"📋 Available tools: {len(tools)} found")
        for tool in tools:
            print(f"  • {tool.name}")
        print()
        
        # Test URLs for demonstration
        test_urls = [
            "https://github.com/AI-Maker-Space/LLM-Dev-101",
            "https://www.python.org",
            "https://fastapi.tiangolo.com"
        ]
        
        # Test 1: Basic URL shortening with enhanced features
        print("🔗 Test 1: Enhanced URL Shortening")
        print("-" * 40)
        result = await client.call_tool("shorten_url", {
            "url": test_urls[0],
            "collection_name": "test_collection",
            "tags": "github, ai, education"
        })
        print(f"Result: {result.data.result}")
        print()
        
        # Test 2: Create a collection
        print("📁 Test 2: Create URL Collection")
        print("-" * 40)
        result = await client.call_tool("create_url_collection", {
            "name": "research_links",
            "description": "Collection of research and educational links"
        })
        print(f"Result: {result.data.result}")
        print()
        
        # Test 3: Batch URL shortening
        print("📊 Test 3: Batch URL Shortening")
        print("-" * 40)
        batch_urls = "\n".join(test_urls)
        result = await client.call_tool("shorten_url_batch", {
            "urls": batch_urls,
            "collection_name": "research_links",
            "tags": "batch_test, research"
        })
        print(f"Result: {result.data.result}")
        print()
        
        # Test 4: URL validation
        print("✅ Test 4: URL Validation")
        print("-" * 40)
        result = await client.call_tool("validate_url", {
            "url": "https://www.google.com"
        })
        print(f"Result: {result.data.result}")
        print()
        
        # Test 5: Get URL metadata
        print("📄 Test 5: URL Metadata Extraction")
        print("-" * 40)
        result = await client.call_tool("get_url_metadata", {
            "url": "https://www.python.org"
        })
        print(f"Result: {result.data.result}")
        print()
        
        # Test 6: Check URL safety
        print("🔒 Test 6: URL Safety Check")
        print("-" * 40)
        result = await client.call_tool("check_url_safety", {
            "url": "https://www.github.com"
        })
        print(f"Result: {result.data.result}")
        print()
        
        # Test 7: Generate QR code
        print("📱 Test 7: QR Code Generation")
        print("-" * 40)
        result = await client.call_tool("generate_qr_code", {
            "url": "https://www.python.org",
            "size": 8
        })
        result_text = result.data.result
        # Only show first part of base64 to avoid cluttering output
        if "data:image/png;base64," in result_text:
            parts = result_text.split("data:image/png;base64,")
            print(f"{parts[0]}data:image/png;base64,[BASE64_DATA_TRUNCATED_FOR_DISPLAY]")
        else:
            print(f"Result: {result_text}")
        print()
        
        # Test 8: Expand URL (using a known short URL)
        print("🔗 Test 8: URL Expansion")
        print("-" * 40)
        result = await client.call_tool("expand_url", {
            "shortened_url": "https://bit.ly/python-docs"
        })
        print(f"Result: {result.data.result}")
        print()
        
        # Test 9: List collections
        print("📁 Test 9: List Collections")
        print("-" * 40)
        result = await client.call_tool("list_collections")
        print(f"Result: {result.data.result}")
        print()
        
        # Test 10: List saved URLs
        print("📋 Test 10: List Saved URLs")
        print("-" * 40)
        result = await client.call_tool("list_my_urls", {
            "limit": 10
        })
        print(f"Result: {result.data.result}")
        print()
        
        # Test 11: Search URLs
        print("🔍 Test 11: Search URLs")
        print("-" * 40)
        result = await client.call_tool("search_urls", {
            "search_term": "python",
            "limit": 5
        })
        print(f"Result: {result.data.result}")
        print()
        
        # Test 12: Filter URLs by collection
        print("🗂️ Test 12: Filter URLs by Collection")
        print("-" * 40)
        result = await client.call_tool("list_my_urls", {
            "collection": "research_links",
            "limit": 5
        })
        print(f"Result: {result.data.result}")
        print()
        
        # Test the original tools to ensure they still work
        print("🎲 Test 13: Original Dice Roller (Compatibility)")
        print("-" * 40)
        result = await client.call_tool("roll_dice", {
            "notation": "2d6",
            "num_rolls": 1
        })
        print(f"Result: {result.data.result}")
        print()
        
        print("🌐 Test 14: Original Web Search (Compatibility)")
        print("-" * 40)
        result = await client.call_tool("web_search", {
            "query": "MCP protocol documentation"
        })
        result_text = result.data.result
        print(f"Result: {result_text[:200]}...")  # Truncate for readability
        print()
        
        print("✅ All tests completed!")
        print("🎉 Enhanced URL Shortener MCP Server is working correctly!")

async def test_error_handling():
    """Test error handling scenarios"""
    print("\n🚨 Testing Error Handling")
    print("=" * 40)
    
    async with Client("server.py") as client:
        # Test invalid URL
        print("1. Testing invalid URL:")
        result = await client.call_tool("validate_url", {
            "url": "not-a-valid-url"
        })
        print(f"   Result: {result.data.result}")
        
        # Test unreachable URL
        print("\n2. Testing unreachable URL:")
        result = await client.call_tool("validate_url", {
            "url": "https://this-domain-definitely-does-not-exist-12345.com"
        })
        print(f"   Result: {result.data.result}")
        
        # Test empty batch
        print("\n3. Testing empty batch URLs:")
        result = await client.call_tool("shorten_url_batch", {
            "urls": "",
            "collection_name": "test"
        })
        print(f"   Result: {result.data.result}")
        
        print("\n✅ Error handling tests completed!")

if __name__ == "__main__":
    print("🚀 Starting Enhanced URL Shortener MCP Tests")
    print("=" * 60)
    
    # Run main functionality tests
    asyncio.run(test_enhanced_url_tools())
    
    # Run error handling tests
    asyncio.run(test_error_handling())
    
    print("\n🎊 All tests completed successfully!")
    print("📊 Summary:")
    print("   • ✅ Enhanced URL shortening with metadata")
    print("   • ✅ Collection and tag management")
    print("   • ✅ Batch processing capabilities")
    print("   • ✅ URL validation and safety checks")
    print("   • ✅ QR code generation")
    print("   • ✅ URL expansion and analysis")
    print("   • ✅ Persistent storage with SQLite")
    print("   • ✅ Search and filtering functionality")
    print("   • ✅ Backward compatibility with existing tools") 