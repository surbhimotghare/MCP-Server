import asyncio
from url_manager_graph import run_smart_url_manager

async def test_complete_workflow():
    """Test a complete end-to-end workflow"""
    
    user_request = """
    I'm researching AI and Machine Learning. Please analyze these educational resources:
    
    https://www.python.org
    https://pytorch.org/tutorials/
    
    Collection: ai_learning_resources
    Tags: education, ai, machine-learning, tutorials
    """
    
    print("🧪 Testing Complete Workflow: Content Curation")
    print("=" * 60)
    print("📝 User Request:")
    print(user_request)
    print("\n🤖 Smart URL Manager Processing...")
    print("-" * 40)
    
    result = await run_smart_url_manager(user_request)
    print(result)
    
    print("\n" + "="*60)
    print("🎉 Complete workflow test finished!")

if __name__ == "__main__":
    asyncio.run(test_complete_workflow()) 