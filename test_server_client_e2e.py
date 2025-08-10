import asyncio
from url_manager_graph_client import run_smart_url_manager

async def test_server_client_e2e_workflow():
    """Test a complete end-to-end workflow between LangGraph client and MCP server"""
    
    user_request = """
    I'm researching AI and Machine Learning. Please analyze these educational resources:
    
    https://www.python.org
    https://pytorch.org/tutorials/
    
    Collection: ai_learning_resources
    Tags: education, ai, machine-learning, tutorials
    """
    
    print("🧪 Testing Server-Client E2E Workflow: Content Curation")
    print("=" * 60)
    print("📝 User Request:")
    print(user_request)
    print("\n🤖 Smart URL Manager Processing...")
    print("-" * 40)
    
    result = await run_smart_url_manager(user_request)
    print(result)
    
    print("\n" + "="*60)
    print("🎉 Server-Client E2E workflow test finished!")

if __name__ == "__main__":
    asyncio.run(test_server_client_e2e_workflow()) 