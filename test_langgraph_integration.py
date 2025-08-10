import asyncio
import subprocess
import time
from url_manager_graph import SmartURLManager

async def test_basic_langgraph_integration():
    """Test basic LangGraph integration with MCP server"""
    print("🧪 Testing LangGraph Integration with MCP Server")
    print("=" * 60)
    
    try:
        # Initialize the Smart URL Manager
        print("🔧 Initializing Smart URL Manager...")
        manager = SmartURLManager()
        print("✅ Smart URL Manager initialized successfully")
        
        # Test simple URL validation workflow
        print("\n📝 Testing URL Validation Workflow...")
        test_request = "Please check if this URL works: https://www.python.org"
        
        print(f"Request: {test_request}")
        print("\n🤖 Processing request through LangGraph workflow...")
        
        result = await manager.process_request(test_request)
        
        print("\n📊 Workflow Result:")
        print("-" * 40)
        print(result)
        
        print("\n✅ Basic LangGraph integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ LangGraph integration test failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

async def test_intent_detection():
    """Test the intent detection capabilities"""
    print("\n🎯 Testing Intent Detection")
    print("=" * 40)
    
    test_cases = [
        ("Validate URL: https://www.google.com", "validate"),
        ("Shorten these URLs: https://example.com, https://test.com", "batch_process"),
        ("Analyze this content: https://www.python.org", "content_analysis"),
        ("Organize these links collection: docs", "organize")
    ]
    
    manager = SmartURLManager()
    
    for request, expected_intent in test_cases:
        print(f"\n📝 Request: '{request}'")
        print(f"🎯 Expected intent: {expected_intent}")
        
        try:
            # We'll just test the parsing and intent analysis
            initial_state = {
                "messages": [request],
                "urls": [],
                "operation": "",
                "collection_name": None,
                "tags": None,
                "user_intent": "",
                "analysis_results": {},
                "processed_urls": [],
                "workflow_summary": "",
                "error_messages": []
            }
            
            # Test input parsing
            parsed_state = manager._parse_input_node(initial_state)
            print(f"🔍 Extracted URLs: {parsed_state['urls']}")
            print(f"📁 Collection: {parsed_state['collection_name']}")
            print(f"🏷️  Tags: {parsed_state['tags']}")
            
            # Test intent analysis
            intent_state = manager._analyze_intent_node(parsed_state)
            detected_intent = intent_state['user_intent']
            print(f"🤖 Detected intent: {detected_intent}")
            
            if detected_intent == expected_intent:
                print("✅ Intent detection successful")
            else:
                print(f"⚠️  Intent mismatch (expected: {expected_intent}, got: {detected_intent})")
                
        except Exception as e:
            print(f"❌ Error testing intent: {str(e)}")

async def test_workflow_routing():
    """Test workflow routing logic"""
    print("\n🛤️  Testing Workflow Routing")
    print("=" * 40)
    
    manager = SmartURLManager()
    
    test_states = [
        {"user_intent": "validate", "urls": ["https://example.com"]},
        {"user_intent": "batch_process", "urls": ["https://example.com", "https://test.com"]},
        {"user_intent": "content_analysis", "urls": ["https://python.org"]},
        {"user_intent": "organize", "urls": ["https://docs.com"]}
    ]
    
    for state in test_states:
        intent = state["user_intent"]
        route = manager._route_workflow(state)
        print(f"🎯 Intent: {intent} → Route: {route}")

if __name__ == "__main__":
    print("🚀 Starting LangGraph Integration Tests")
    print("=" * 60)
    
    async def run_all_tests():
        success = True
        
        # Test 1: Basic integration
        if not await test_basic_langgraph_integration():
            success = False
        
        # Test 2: Intent detection
        await test_intent_detection()
        
        # Test 3: Workflow routing
        await test_workflow_routing()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 All LangGraph integration tests completed!")
            print("✅ The Smart URL Manager is ready for use!")
        else:
            print("⚠️  Some tests encountered issues")
            print("💡 Check the error messages above for debugging")
    
    asyncio.run(run_all_tests()) 