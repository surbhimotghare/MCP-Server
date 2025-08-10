from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence, List, Optional
import operator
import json
import re
import asyncio
import subprocess
from datetime import datetime
from fastmcp import Client

class URLManagerState(TypedDict):
    """State for the URL Manager workflow"""
    messages: Annotated[Sequence[str], operator.add]
    urls: List[str]
    operation: str  # 'analyze', 'shorten', 'curate', 'organize', 'validate'
    collection_name: Optional[str]
    tags: Optional[str]
    user_intent: str
    analysis_results: dict
    processed_urls: List[dict]
    workflow_summary: str
    error_messages: List[str]

class SmartURLManager:
    def __init__(self, mcp_server_path: str = "server.py"):
        """Initialize the Smart URL Manager with MCP integration"""
        self.mcp_server_path = mcp_server_path
        self.workflow = self._create_workflow()
        
    async def _call_mcp_tool(self, tool_name: str, parameters: dict):
        """Call MCP tool using fastmcp client"""
        try:
            async with Client(self.mcp_server_path) as client:
                result = await client.call_tool(tool_name, parameters)
                return result.data.result
        except Exception as e:
            return f"Error calling {tool_name}: {str(e)}"
        
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow"""
        workflow = StateGraph(URLManagerState)
        
        # Add nodes for different workflow stages
        workflow.add_node("parse_input", self._parse_input_node)
        workflow.add_node("analyze_intent", self._analyze_intent_node)
        workflow.add_node("validate_urls", self._validate_urls_node)
        workflow.add_node("process_batch", self._process_batch_node)
        workflow.add_node("analyze_content", self._analyze_content_node)
        workflow.add_node("organize_urls", self._organize_urls_node)
        workflow.add_node("generate_summary", self._generate_summary_node)
        
        # Define the workflow routing
        workflow.set_entry_point("parse_input")
        
        workflow.add_edge("parse_input", "analyze_intent")
        
        workflow.add_conditional_edges(
            "analyze_intent",
            self._route_workflow,
            {
                "validate": "validate_urls",
                "batch_process": "process_batch", 
                "content_analysis": "analyze_content",
                "organize": "organize_urls"
            }
        )
        
        workflow.add_edge("validate_urls", "generate_summary")
        workflow.add_edge("process_batch", "analyze_content")
        workflow.add_edge("analyze_content", "organize_urls")
        workflow.add_edge("organize_urls", "generate_summary")
        workflow.add_edge("generate_summary", END)
        
        return workflow.compile()
    
    def _parse_input_node(self, state: URLManagerState) -> URLManagerState:
        """Parse user input to extract URLs and understand the request"""
        user_input = state["messages"][-1] if state["messages"] else ""
        
        # Extract URLs using regex
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, user_input)
        
        # Also look for domain names that might need protocol
        domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
        potential_domains = re.findall(domain_pattern, user_input)
        
        # Filter out URLs already found and add protocol
        for domain in potential_domains:
            full_url = f"https://{domain}"
            if not any(domain in url for url in urls) and domain not in ['example.com', 'test.com']:
                urls.append(full_url)
        
        # Extract collection name if mentioned
        collection_match = re.search(r'collection[:\s]+(["\']?)([^"\'\\s]+)\1', user_input, re.IGNORECASE)
        collection_name = collection_match.group(2) if collection_match else None
        
        # Extract tags if mentioned  
        tags_match = re.search(r'tags?[:\s]+(["\']?)([^"\'\\n]+)\1', user_input, re.IGNORECASE)
        tags = tags_match.group(2) if tags_match else None
        
        state["urls"] = urls
        state["collection_name"] = collection_name
        state["tags"] = tags
        state["analysis_results"] = {}
        state["processed_urls"] = []
        state["error_messages"] = []
        
        return state
    
    def _analyze_intent_node(self, state: URLManagerState) -> URLManagerState:
        """Analyze user intent to determine the appropriate workflow"""
        user_input = state["messages"][-1].lower() if state["messages"] else ""
        urls = state["urls"]
        
        # Intent classification based on keywords and context
        if any(keyword in user_input for keyword in ['validate', 'check', 'verify', 'test']):
            intent = "validate"
        elif any(keyword in user_input for keyword in ['shorten', 'short', 'compress']):
            intent = "batch_process"
        elif any(keyword in user_input for keyword in ['analyze', 'metadata', 'info', 'details']):
            intent = "content_analysis" 
        elif any(keyword in user_input for keyword in ['organize', 'collection', 'group', 'categorize']):
            intent = "organize"
        elif any(keyword in user_input for keyword in ['curate', 'research', 'study']):
            intent = "content_analysis"
        else:
            # Default based on number of URLs
            if len(urls) == 0:
                intent = "validate"  # No URLs, might be asking for help
            elif len(urls) == 1:
                intent = "content_analysis"  # Single URL, probably want details
            else:
                intent = "batch_process"  # Multiple URLs, probably want to process them
        
        state["user_intent"] = intent
        state["operation"] = intent
        
        return state
    
    def _route_workflow(self, state: URLManagerState) -> str:
        """Route to the appropriate workflow based on analyzed intent"""
        intent = state["user_intent"]
        
        if intent == "validate":
            return "validate"
        elif intent == "batch_process":
            return "batch_process"
        elif intent == "content_analysis":
            return "content_analysis" 
        elif intent == "organize":
            return "organize"
        else:
            return "batch_process"  # Default fallback
    
    async def _validate_urls_node(self, state: URLManagerState) -> URLManagerState:
        """Validate URLs for format and reachability"""
        urls = state["urls"]
        
        if not urls:
            state["error_messages"].append("No URLs provided for validation")
            return state
        
        validation_results = []
        
        for url in urls:
            try:
                result = await self._call_mcp_tool("validate_url", {"url": url})
                validation_results.append({
                    "url": url,
                    "validation": result,
                    "status": "validated"
                })
            except Exception as e:
                validation_results.append({
                    "url": url,
                    "validation": {"error": str(e)},
                    "status": "error"
                })
        
        state["processed_urls"] = validation_results
        state["analysis_results"]["validation"] = validation_results
        
        return state
    
    async def _process_batch_node(self, state: URLManagerState) -> URLManagerState:
        """Process multiple URLs for shortening"""
        urls = state["urls"]
        
        if not urls:
            state["error_messages"].append("No URLs provided for batch processing")
            return state
        
        # Prepare batch input
        urls_text = "\n".join(urls)
        
        try:
            result = await self._call_mcp_tool("shorten_url_batch", {
                "urls": urls_text,
                "collection_name": state.get("collection_name", ""),
                "tags": state.get("tags", "")
            })
            
            state["analysis_results"]["batch_processing"] = result
            
            # Also get individual URL details for further analysis
            url_details = []
            for url in urls[:3]:  # Limit to first 3 for performance
                try:
                    metadata = await self._call_mcp_tool("get_url_metadata", {"url": url})
                    safety = await self._call_mcp_tool("check_url_safety", {"url": url})
                    
                    url_details.append({
                        "url": url,
                        "metadata": metadata,
                        "safety": safety,
                        "status": "processed"
                    })
                except Exception as e:
                    url_details.append({
                        "url": url,
                        "error": str(e),
                        "status": "error"
                    })
            
            state["processed_urls"] = url_details
            
        except Exception as e:
            state["error_messages"].append(f"Batch processing failed: {str(e)}")
        
        return state
    
    async def _analyze_content_node(self, state: URLManagerState) -> URLManagerState:
        """Analyze content of URLs for metadata and safety"""
        urls = state["urls"]
        
        if not urls:
            # If no new URLs, work with already processed ones
            urls = [item["url"] for item in state.get("processed_urls", []) if "url" in item]
        
        analysis_results = []
        
        for url in urls[:3]:  # Limit for performance
            try:
                # Get comprehensive metadata
                metadata = await self._call_mcp_tool("get_url_metadata", {"url": url})
                safety = await self._call_mcp_tool("check_url_safety", {"url": url})
                
                # Generate QR code for important URLs
                qr_code = None
                if any(keyword in url.lower() for keyword in ['github', 'docs', 'python']):
                    try:
                        qr_result = await self._call_mcp_tool("generate_qr_code", {"url": url, "size": 8})
                        qr_code = "Generated" if "QR Code Generated" in str(qr_result) else None
                    except:
                        pass  # QR code generation is optional
                
                analysis_results.append({
                    "url": url,
                    "metadata": metadata,
                    "safety": safety,
                    "qr_code": qr_code,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "status": "analyzed"
                })
                
            except Exception as e:
                analysis_results.append({
                    "url": url,
                    "error": str(e),
                    "status": "error"
                })
        
        # Update or extend processed URLs
        if state.get("processed_urls"):
            # Merge with existing data
            existing_urls = {item.get("url"): item for item in state["processed_urls"]}
            for analysis in analysis_results:
                url = analysis["url"]
                if url in existing_urls:
                    existing_urls[url].update(analysis)
                else:
                    state["processed_urls"].append(analysis)
        else:
            state["processed_urls"] = analysis_results
        
        state["analysis_results"]["content_analysis"] = analysis_results
        
        return state
    
    async def _organize_urls_node(self, state: URLManagerState) -> URLManagerState:
        """Organize URLs into collections and apply tags"""
        collection_name = state.get("collection_name")
        
        if not collection_name:
            # Auto-generate collection name based on content
            processed_urls = state.get("processed_urls", [])
            domains = set()
            for item in processed_urls:
                if isinstance(item.get("metadata"), str) and "Domain:" in item["metadata"]:
                    # Extract domain from metadata string
                    lines = item["metadata"].split('\n')
                    domain_line = next((line for line in lines if 'Domain:' in line), None)
                    if domain_line:
                        domain = domain_line.split('Domain:')[-1].strip()
                        domains.add(domain)
            
            if domains:
                if len(domains) == 1:
                    collection_name = f"urls_from_{list(domains)[0].replace('.', '_')}"
                else:
                    collection_name = f"mixed_collection_{datetime.now().strftime('%Y%m%d_%H%M')}"
            else:
                collection_name = f"url_collection_{datetime.now().strftime('%Y%m%d_%H%M')}"
        
        # Create collection if it doesn't exist
        try:
            await self._call_mcp_tool("create_url_collection", {
                "name": collection_name,
                "description": f"Auto-created collection for workflow on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            })
        except:
            pass  # Collection might already exist
        
        # Update state with final collection name
        state["collection_name"] = collection_name
        state["analysis_results"]["organization"] = {
            "collection_name": collection_name,
            "organization_timestamp": datetime.now().isoformat()
        }
        
        return state
    
    def _generate_summary_node(self, state: URLManagerState) -> URLManagerState:
        """Generate a comprehensive summary of the workflow results"""
        operation = state.get("operation", "unknown")
        urls = state.get("urls", [])
        processed_urls = state.get("processed_urls", [])
        analysis_results = state.get("analysis_results", {})
        error_messages = state.get("error_messages", [])
        
        summary = f"# 📊 Smart URL Manager Workflow Results\n\n"
        summary += f"**Operation**: {operation.title().replace('_', ' ')}\n"
        summary += f"**URLs Processed**: {len(urls)}\n"
        summary += f"**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if state.get("collection_name"):
            summary += f"**Collection**: {state['collection_name']}\n"
        
        if state.get("tags"):
            summary += f"**Tags**: {state['tags']}\n"
        
        summary += "\n## 📋 Results\n\n"
        
        # Summarize based on operation type
        if operation == "validate":
            valid_count = sum(1 for item in processed_urls if item.get("status") == "validated")
            summary += f"✅ **Validation Results**: {valid_count}/{len(processed_urls)} URLs validated successfully\n\n"
            
            for item in processed_urls:
                url = item.get("url", "Unknown URL")
                validation = item.get("validation", {})
                if isinstance(validation, str) and "❌" in validation:
                    summary += f"❌ **{url}**: Validation failed\n"
                elif isinstance(validation, str) and "✅" in validation:
                    summary += f"✅ **{url}**: Valid and reachable\n"
                else:
                    summary += f"ℹ️ **{url}**: Validation completed\n"
        
        elif operation == "batch_process":
            batch_result = analysis_results.get("batch_processing", "No batch results")
            if isinstance(batch_result, str) and len(batch_result) > 100:
                # Truncate long results
                summary += f"📊 **Batch Processing**: Successfully processed {len(urls)} URLs\n\n"
            else:
                summary += f"📊 **Batch Processing Results**:\n{batch_result}\n\n"
            
            if processed_urls:
                summary += "📄 **Content Analysis Summary**:\n"
                for item in processed_urls[:3]:  # Show first 3
                    url = item.get("url", "Unknown")
                    if isinstance(item.get("metadata"), str):
                        # Extract title from metadata string
                        metadata = item["metadata"]
                        title_line = next((line for line in metadata.split('\n') if 'Title:' in line), None)
                        title = title_line.split('Title:')[-1].strip() if title_line else "No title"
                        summary += f"• **{title[:50]}...** ({url})\n"
                    else:
                        summary += f"• **{url}**\n"
        
        elif operation == "content_analysis":
            summary += "📄 **Content Analysis Results**:\n\n"
            for item in processed_urls:
                url = item.get("url", "Unknown")
                summary += f"### URL Analysis\n"
                summary += f"**URL**: {url}\n"
                
                if isinstance(item.get("metadata"), str):
                    metadata = item["metadata"]
                    lines = metadata.split('\n')
                    
                    title_line = next((line for line in lines if 'Title:' in line), None)
                    if title_line:
                        title = title_line.split('Title:')[-1].strip()
                        summary += f"**Title**: {title}\n"
                    
                    desc_line = next((line for line in lines if 'Description:' in line), None)
                    if desc_line:
                        desc = desc_line.split('Description:')[-1].strip()
                        summary += f"**Description**: {desc[:100]}...\n"
                
                if isinstance(item.get("safety"), str) and "✅" in item["safety"]:
                    summary += f"**Safety**: ✅ Safe\n"
                elif isinstance(item.get("safety"), str) and "⚠️" in item["safety"]:
                    summary += f"**Safety**: ⚠️ Warning\n"
                    
                if item.get("qr_code"):
                    summary += f"**QR Code**: Generated\n"
                
                summary += "\n"
        
        elif operation == "organize":
            summary += f"🗂️ **Organization Results**:\n"
            summary += f"Collection: {state.get('collection_name', 'None')}\n"
            summary += f"URLs organized: {len(processed_urls)}\n\n"
        
        # Add error summary if any
        if error_messages:
            summary += "## ⚠️ Errors Encountered\n\n"
            for error in error_messages:
                summary += f"• {error}\n"
            summary += "\n"
        
        # Add recommendations
        summary += "## 💡 Recommendations\n\n"
        
        if operation == "validate":
            summary += "• Consider using the batch shortening feature for valid URLs\n"
            summary += "• Review any failed validations and check URL formats\n"
        elif operation == "batch_process":
            summary += "• URLs have been shortened and organized in your collection\n" 
            summary += "• Use search functionality to find specific URLs later\n"
        elif operation == "content_analysis":
            summary += "• Consider organizing analyzed URLs into themed collections\n"
            summary += "• Generate QR codes for frequently accessed URLs\n"
        
        summary += f"• Use `list_my_urls` to view all your saved URLs\n"
        summary += f"• Use `search_urls` to find specific content\n"
        
        state["workflow_summary"] = summary
        
        return state
    
    async def process_request(self, user_input: str) -> str:
        """Process a user request through the workflow"""
        initial_state = URLManagerState(
            messages=[user_input],
            urls=[],
            operation="",
            collection_name=None,
            tags=None,
            user_intent="",
            analysis_results={},
            processed_urls=[],
            workflow_summary="",
            error_messages=[]
        )
        
        # Run the workflow
        final_state = await self.workflow.ainvoke(initial_state)
        
        return final_state["workflow_summary"]

# Helper function to create and run the URL manager
async def run_smart_url_manager(user_input: str) -> str:
    """Convenience function to run the Smart URL Manager"""
    manager = SmartURLManager()
    return await manager.process_request(user_input) 