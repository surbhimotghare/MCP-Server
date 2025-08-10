# 📋 **Comprehensive Plan: Enhanced URL Shortener MCP Implementation**

## 🎯 **Overview**
Enhance the existing URL shortener tool into a comprehensive URL management MCP server, then build a LangGraph application for intelligent URL workflows.

---

## 🏗️ **Activity #1: Enhanced URL Shortener MCP Server**

### **Phase 1: Enhanced Core Functionality** 
Building on your existing `shorten_url` tool, add these capabilities:

#### **Enhanced URL Shortening Tools**
1. **`shorten_url_batch`** - Shorten multiple URLs at once
2. **`expand_url`** - Expand shortened URLs to see original destination
3. **`validate_url`** - Check if URLs are valid and reachable
4. **`get_url_metadata`** - Extract title, description, favicon from URLs
5. **`check_url_safety`** - Check URLs against security blacklists

#### **URL Analytics & Management Tools**
6. **`create_url_collection`** - Group URLs into named collections
7. **`get_click_stats`** - Get analytics for shortened URLs (when supported)
8. **`list_my_urls`** - List all URLs shortened in this session
9. **`search_urls`** - Search through saved URLs by title or tag
10. **`generate_qr_code`** - Generate QR codes for URLs

### **Phase 2: Storage & Persistence** 
```python
# url_storage.py - Simple local storage for URL management
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class URLStorage:
    def __init__(self, db_path: str = "urls.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create tables for URL storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                shortened_url TEXT NOT NULL,
                custom_alias TEXT,
                title TEXT,
                description TEXT,
                tags TEXT,
                collection_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                click_count INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_url(self, original: str, shortened: str, **kwargs) -> int:
        """Save URL information to database"""
        # Implementation here
    
    def get_urls(self, collection: str = None, tags: List[str] = None) -> List[Dict]:
        """Retrieve URLs with optional filtering"""
        # Implementation here
```

### **Phase 3: Advanced Features** 
```python
# enhanced_url_tools.py
import requests
from bs4 import BeautifulSoup
import qrcode
import io
import base64
from urllib.parse import urlparse
import hashlib

class EnhancedURLTools:
    def __init__(self):
        self.storage = URLStorage()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; URL-Tools/1.0)'
        })
    
    def get_url_metadata(self, url: str) -> Dict:
        """Extract metadata from URL"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.find('title')
            description = soup.find('meta', attrs={'name': 'description'})
            og_title = soup.find('meta', property='og:title')
            og_description = soup.find('meta', property='og:description')
            
            return {
                'title': (og_title or title).get('content', '').strip() if (og_title or title) else '',
                'description': (og_description or description).get('content', '').strip() if (og_description or description) else '',
                'domain': urlparse(url).netloc,
                'is_secure': url.startswith('https://')
            }
        except Exception as e:
            return {'error': str(e)}
    
    def generate_qr_code(self, url: str) -> str:
        """Generate QR code for URL and return as base64 string"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        
        return base64.b64encode(buffer.getvalue()).decode()
    
    def check_url_safety(self, url: str) -> Dict:
        """Basic URL safety check"""
        # Simple implementation - in production, use Google Safe Browsing API
        suspicious_domains = ['bit.ly/malware', 'suspicious-site.com']
        domain = urlparse(url).netloc
        
        return {
            'is_safe': domain not in suspicious_domains,
            'warnings': ['Suspicious domain detected'] if domain in suspicious_domains else []
        }
```

---

## 🚀 **Activity #2: URL Management LangGraph Application**

### **Application Concept: "Smart URL Manager"** 
A LangGraph application that intelligently manages URLs for different use cases:
- Content curation workflows
- Link sharing optimization
- URL collection management
- Batch processing operations

### **Phase 1: Core LangGraph Structure** 
```python
# url_manager_graph.py
from langgraph.graph import StateGraph, END
from langchain_mcp import MCPAdapter
from typing import TypedDict, Annotated, Sequence, List
import operator

class URLManagerState(TypedDict):
    messages: Annotated[Sequence[str], operator.add]
    urls: List[str]
    operation: str  # 'shorten', 'curate', 'analyze', 'organize'
    collection_name: str
    results: dict
    user_intent: str

def create_url_manager():
    workflow = StateGraph(URLManagerState)
    
    # Add nodes
    workflow.add_node("analyze_intent", analyze_intent_node)
    workflow.add_node("process_urls", process_urls_node)
    workflow.add_node("enhance_metadata", enhance_metadata_node)
    workflow.add_node("organize_content", organize_content_node)
    workflow.add_node("generate_summary", generate_summary_node)
    
    # Define workflow
    workflow.set_entry_point("analyze_intent")
    workflow.add_conditional_edges(
        "analyze_intent",
        determine_workflow,
        {
            "batch_shorten": "process_urls",
            "content_curation": "enhance_metadata",
            "organization": "organize_content"
        }
    )
    workflow.add_edge("process_urls", "generate_summary")
    workflow.add_edge("enhance_metadata", "organize_content")
    workflow.add_edge("organize_content", "generate_summary")
    workflow.add_edge("generate_summary", END)
    
    return workflow.compile()
```

### **Phase 2: Workflow Nodes Implementation** 

#### **1. Intent Analysis Node**
```python
async def analyze_intent_node(state: URLManagerState):
    """Determine what the user wants to do with URLs"""
    user_input = state["messages"][-1] if state["messages"] else ""
    urls = state["urls"]
    
    # Simple intent classification
    if len(urls) > 5:
        intent = "batch_processing"
    elif "organize" in user_input.lower() or "collection" in user_input.lower():
        intent = "organization"
    elif "analyze" in user_input.lower() or "metadata" in user_input.lower():
        intent = "content_curation"
    else:
        intent = "simple_shorten"
    
    state["user_intent"] = intent
    return state

async def determine_workflow(state: URLManagerState):
    """Route to appropriate workflow based on intent"""
    intent = state["user_intent"]
    url_count = len(state["urls"])
    
    if url_count > 10:
        return "batch_shorten"
    elif intent == "organization":
        return "organization"
    else:
        return "content_curation"
```

#### **2. URL Processing Node**
```python
async def process_urls_node(state: URLManagerState):
    """Process URLs based on operation type"""
    mcp_adapter = MCPAdapter("server.py")
    results = []
    
    for url in state["urls"]:
        if state["operation"] == "shorten":
            result = await mcp_adapter.call_tool("shorten_url", {"url": url})
        elif state["operation"] == "validate":
            result = await mcp_adapter.call_tool("validate_url", {"url": url})
        elif state["operation"] == "analyze":
            result = await mcp_adapter.call_tool("get_url_metadata", {"url": url})
        
        results.append({
            "original_url": url,
            "result": result
        })
    
    state["results"] = {"processed_urls": results}
    return state
```

### **Phase 3: Use Cases & Features** 

#### **Use Case 1: Content Curator Assistant**
- Input: List of article URLs
- Process: Extract metadata, categorize by topic
- Output: Organized collection with summaries

#### **Use Case 2: Social Media Manager**
- Input: URLs to share across platforms
- Process: Shorten with custom aliases, generate QR codes
- Output: Platform-optimized shortened URLs

#### **Use Case 3: Research Link Manager**
- Input: Research URLs with tags
- Process: Validate links, extract abstracts
- Output: Searchable research database

#### **Use Case 4: Event/Campaign URL Manager**
- Input: Campaign materials with URLs
- Process: Batch shorten with campaign prefixes
- Output: Trackable campaign URL collection

---