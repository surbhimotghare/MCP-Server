from fastmcp import Client

async def main():
    # Connect via stdio to a local script
    async with Client("server.py") as client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        
        # Test web search
        print("\n--- Testing Web Search ---")
        result = await client.call_tool("web_search", {"query": "What is the capital of France?"})
        print(f"Web Search Result: {result}")
        
        # Test URL shortener
        print("\n--- Testing URL Shortener ---")
        url_result = await client.call_tool("shorten_url", {"url": "https://github.com/AI-Maker-Space/LLM-Dev-101"})
        print(f"URL Shortener Result: {url_result}")
        
        # Test dice roller
        print("\n--- Testing Dice Roller ---")
        dice_result = await client.call_tool("roll_dice", {"notation": "2d6", "num_rolls": 1})
        print(f"Dice Roll Result: {dice_result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())