"""
Practical Use Cases for the Smart URL Manager LangGraph Application

This file demonstrates real-world scenarios where the Smart URL Manager
can automatically handle complex URL management workflows.
"""

import asyncio
from url_manager_graph_client import run_smart_url_manager

async def use_case_1_content_curator():
    """
    Use Case #1: Content Curator Assistant
    
    Scenario: A researcher wants to curate and analyze a collection of 
    educational resources for a specific topic.
    """
    print("🎯 Use Case #1: Content Curator Assistant")
    print("=" * 60)
    
    user_request = """
    I'm researching AI and Machine Learning. Please analyze these educational resources:
    
    https://www.coursera.org/specializations/machine-learning-introduction
    https://www.edx.org/course/artificial-intelligence-mit-6-034
    https://www.kaggle.com/learn
    https://github.com/microsoft/AI-For-Beginners
    https://pytorch.org/tutorials/
    
    Collection: ai_learning_resources
    Tags: education, ai, machine-learning, tutorials
    """
    
    print("📝 User Request:")
    print(user_request)
    print("\n🤖 Smart URL Manager Processing...")
    print("-" * 40)
    
    result = await run_smart_url_manager(user_request)
    print(result)

async def use_case_2_social_media_manager():
    """
    Use Case #2: Social Media Manager
    
    Scenario: A social media manager needs to shorten and organize URLs
    for a marketing campaign with QR codes for offline materials.
    """
    print("\n🎯 Use Case #2: Social Media Manager")
    print("=" * 60)
    
    user_request = """
    Please shorten these URLs for our product launch campaign:
    
    https://www.productlaunch.com/features
    https://www.productlaunch.com/pricing
    https://www.productlaunch.com/testimonials
    https://github.com/company/product-demo
    
    Collection: product_launch_2025
    Tags: marketing, campaign, product-launch
    """
    
    print("📝 User Request:")
    print(user_request)
    print("\n🤖 Smart URL Manager Processing...")
    print("-" * 40)
    
    result = await run_smart_url_manager(user_request)
    print(result)

async def use_case_3_research_assistant():
    """
    Use Case #3: Academic Research Assistant
    
    Scenario: A graduate student needs to validate and organize research papers
    and documentation for their thesis.
    """
    print("\n🎯 Use Case #3: Academic Research Assistant")
    print("=" * 60)
    
    user_request = """
    Please validate and analyze these research sources for my thesis:
    
    https://arxiv.org/abs/2023.12345
    https://papers.nips.cc/paper/2023/hash/abcd1234
    https://ieeexplore.ieee.org/document/9876543
    
    I need to check if these links are still active and get metadata for citation.
    """
    
    print("📝 User Request:")
    print(user_request)
    print("\n🤖 Smart URL Manager Processing...")
    print("-" * 40)
    
    result = await run_smart_url_manager(user_request)
    print(result)

async def use_case_4_documentation_organizer():
    """
    Use Case #4: Technical Documentation Organizer
    
    Scenario: A developer wants to organize various API documentations
    and technical resources for a project.
    """
    print("\n🎯 Use Case #4: Technical Documentation Organizer")
    print("=" * 60)
    
    user_request = """
    Organize these technical documentation links for our development team:
    
    https://docs.python.org/3/
    https://fastapi.tiangolo.com/
    https://docs.docker.com/
    https://kubernetes.io/docs/
    https://www.postgresql.org/docs/
    
    Collection: dev_docs_2025
    Tags: documentation, development, backend, infrastructure
    """
    
    print("📝 User Request:")
    print(user_request)
    print("\n🤖 Smart URL Manager Processing...")
    print("-" * 40)
    
    result = await run_smart_url_manager(user_request)
    print(result)

async def use_case_5_event_organizer():
    """
    Use Case #5: Event Organizer
    
    Scenario: An event organizer needs to manage various event-related URLs
    with different workflows based on content type.
    """
    print("\n🎯 Use Case #5: Event Organizer")
    print("=" * 60)
    
    user_request = """
    I'm organizing a tech conference. Please help me manage these links:
    
    https://www.eventbrite.com/e/tech-conference-2025
    https://www.youtube.com/playlist?list=conference-speakers
    https://drive.google.com/conference-materials
    
    I need to check if all links work and organize them properly.
    Collection: tech_conference_2025
    Tags: conference, event, tech, 2025
    """
    
    print("📝 User Request:")
    print(user_request)
    print("\n🤖 Smart URL Manager Processing...")
    print("-" * 40)
    
    result = await run_smart_url_manager(user_request)
    print(result)

async def use_case_6_content_validation():
    """
    Use Case #6: Bulk URL Validation
    
    Scenario: A website administrator needs to validate a list of external
    links to ensure they're still working.
    """
    print("\n🎯 Use Case #6: Bulk URL Validation")
    print("=" * 60)
    
    user_request = """
    Please check if these external links on our website are still working:
    
    https://www.example-partner-site.com
    https://www.old-documentation-site.org
    https://www.legacy-system.net/docs
    
    I just need to validate these URLs and see which ones are broken.
    """
    
    print("📝 User Request:")
    print(user_request)
    print("\n🤖 Smart URL Manager Processing...")
    print("-" * 40)
    
    result = await run_smart_url_manager(user_request)
    print(result)

async def use_case_7_intelligent_intent_detection():
    """
    Use Case #7: Intelligent Intent Detection
    
    Scenario: Test the system's ability to understand different types of
    requests and route them to appropriate workflows.
    """
    print("\n🎯 Use Case #7: Intelligent Intent Detection")
    print("=" * 60)
    
    test_requests = [
        "Analyze this single URL for me: https://www.python.org",
        "Shorten these URLs: https://www.example.com, https://www.test.com",
        "Check if this link works: https://www.google.com",
        "Organize these GitHub repos: https://github.com/user/repo1, https://github.com/user/repo2"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n📝 Test Request #{i}:")
        print(f"'{request}'")
        print(f"\n🤖 Detected Workflow:")
        print("-" * 30)
        
        result = await run_smart_url_manager(request)
        # Just show the operation and first few lines for brevity
        lines = result.split('\n')
        operation_line = next((line for line in lines if 'Operation' in line), "Unknown")
        print(f"  {operation_line}")
        print()

async def run_all_use_cases():
    """Run all use cases in sequence"""
    print("🚀 Smart URL Manager - Comprehensive Use Case Demonstration")
    print("=" * 80)
    print("This demonstration shows how the LangGraph workflow intelligently")
    print("handles different types of URL management requests.\n")
    
    use_cases = [
        use_case_1_content_curator,
        use_case_2_social_media_manager,
        use_case_3_research_assistant,
        use_case_4_documentation_organizer,
        use_case_5_event_organizer,
        use_case_6_content_validation,
        use_case_7_intelligent_intent_detection
    ]
    
    for use_case in use_cases:
        try:
            await use_case()
            print("\n" + "="*80)
        except Exception as e:
            print(f"❌ Error in {use_case.__name__}: {str(e)}")
            print("="*80)
    
    print("\n🎉 All use cases completed!")
    print("\n📊 Summary of Capabilities Demonstrated:")
    print("  • ✅ Intelligent intent detection and workflow routing")
    print("  • ✅ Multi-URL batch processing with metadata extraction")
    print("  • ✅ Automatic collection creation and organization")
    print("  • ✅ URL validation and safety checking")
    print("  • ✅ Context-aware QR code generation")
    print("  • ✅ Comprehensive workflow summaries")
    print("  • ✅ Error handling and graceful degradation")

if __name__ == "__main__":
    print("🧪 Running Smart URL Manager Use Case Demonstrations")
    asyncio.run(run_all_use_cases()) 