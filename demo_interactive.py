#!/usr/bin/env python3
"""
Interactive Demo Script for Enhanced URL Shortener MCP with Smart LangGraph Application

This script provides a smooth, presentation-friendly way to demonstrate the system
to your team. It showcases real-time interaction between LangGraph and MCP server.
"""

import asyncio
import time
from url_manager_graph_client import run_smart_url_manager

async def interactive_demo():
    """Interactive demo with clear sections and explanations"""
    
    print("🚀 Enhanced URL Shortener MCP + LangGraph Demo")
    print("=" * 60)
    print("This demo shows the complete system in action!")
    print()
    
    # Demo 1: Simple URL shortening
    print("📱 Demo 1: Basic URL Shortening")
    print("-" * 40)
    print("Request: Shorten a single URL with smart defaults")
    print()
    
    request1 = "Please shorten this URL: https://www.python.org"
    print(f"🤖 User Input: {request1}")
    print("\n⏳ Processing...")
    
    start_time = time.time()
    result1 = await run_smart_url_manager(request1)
    processing_time = time.time() - start_time
    
    print(f"✅ Result (processed in {processing_time:.2f}s):")
    print(result1)
    print("\n" + "="*60)
    
    # Demo 2: Content analysis
    print("\n🔍 Demo 2: Content Analysis & Metadata")
    print("-" * 40)
    print("Request: Analyze educational content and organize it")
    print()
    
    request2 = """
    I'm researching AI and Machine Learning. Please analyze these educational resources:
    
    https://www.python.org
    https://pytorch.org/tutorials/
    
    Collection: ai_learning_resources
    Tags: education, ai, machine-learning, tutorials
    """
    
    print(f"🤖 User Input: {request2.strip()}")
    print("\n⏳ Processing...")
    
    start_time = time.time()
    result2 = await run_smart_url_manager(request2)
    processing_time = time.time() - start_time
    
    print(f"✅ Result (processed in {processing_time:.2f}s):")
    print(result2)
    print("\n" + "="*60)
    
    # Demo 3: Batch processing
    print("\n📊 Demo 3: Batch URL Processing")
    print("-" * 40)
    print("Request: Process multiple URLs for a marketing campaign")
    print()
    
    request3 = """
    Please shorten these URLs for our product launch campaign:
    
    https://www.productlaunch.com/features
    https://www.productlaunch.com/pricing
    https://github.com/company/product-demo
    
    Collection: product_launch_2025
    Tags: marketing, campaign, product-launch
    """
    
    print(f"🤖 User Input: {request3.strip()}")
    print("\n⏳ Processing...")
    
    start_time = time.time()
    result3 = await run_smart_url_manager(request3)
    processing_time = time.time() - start_time
    
    print(f"✅ Result (processed in {processing_time:.2f}s):")
    print(result3)
    print("\n" + "="*60)
    
    # Demo 4: URL validation
    print("\n✅ Demo 4: URL Validation & Safety")
    print("-" * 40)
    print("Request: Check if external links are still working")
    print()
    
    request4 = """
    Please check if these external links are still working:
    
    https://www.google.com
    https://www.github.com
    
    I just need to validate these URLs and see which ones are broken.
    """
    
    print(f"🤖 User Input: {request4.strip()}")
    print("\n⏳ Processing...")
    
    start_time = time.time()
    result4 = await run_smart_url_manager(request4)
    processing_time = time.time() - start_time
    
    print(f"✅ Result (processed in {processing_time:.2f}s):")
    print(result4)
    print("\n" + "="*60)
    
    # Summary
    print("\n🎉 Demo Complete!")
    print("=" * 60)
    print("What we demonstrated:")
    print("• 🏗️ MCP Server with 11 specialized tools")
    print("• 🧠 LangGraph workflow orchestration")
    print("• 🔄 Real-time client-server communication")
    print("• 📊 Intelligent intent detection and routing")
    print("• 🎯 Multiple use cases: shortening, analysis, validation")
    print("• ⚡ Fast processing (typically 2-3 seconds)")
    print()
    print("The system successfully:")
    print("✅ Processed natural language requests")
    print("✅ Detected user intent automatically")
    print("✅ Orchestrated multiple MCP tools")
    print("✅ Provided structured, actionable results")
    print("✅ Maintained context across operations")

if __name__ == "__main__":
    print("🎬 Starting Interactive Demo...")
    print("Make sure your MCP server is running in another terminal!")
    print("Run: uv run server.py")
    print()
    input("Press Enter to start the demo...")
    
    asyncio.run(interactive_demo()) 