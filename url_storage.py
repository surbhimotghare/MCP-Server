import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any

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
                service_used TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                click_count INTEGER DEFAULT 0,
                is_safe BOOLEAN DEFAULT 1,
                metadata TEXT
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
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO urls (
                original_url, shortened_url, custom_alias, title, 
                description, tags, collection_name, service_used, 
                is_safe, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            original,
            shortened,
            kwargs.get('custom_alias'),
            kwargs.get('title'),
            kwargs.get('description'),
            json.dumps(kwargs.get('tags', [])),
            kwargs.get('collection_name'),
            kwargs.get('service_used'),
            kwargs.get('is_safe', True),
            json.dumps(kwargs.get('metadata', {}))
        ))
        
        url_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return url_id
    
    def get_urls(self, collection: str = None, tags: List[str] = None, limit: int = 100) -> List[Dict]:
        """Retrieve URLs with optional filtering"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM urls WHERE 1=1"
        params = []
        
        if collection:
            query += " AND collection_name = ?"
            params.append(collection)
        
        if tags:
            # Simple tag filtering - in production would use proper JSON queries
            for tag in tags:
                query += " AND tags LIKE ?"
                params.append(f'%"{tag}"%')
        
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    def search_urls(self, search_term: str, limit: int = 50) -> List[Dict]:
        """Search URLs by title, description, or original URL"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM urls 
            WHERE title LIKE ? OR description LIKE ? OR original_url LIKE ?
            ORDER BY created_at DESC LIMIT ?
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    def create_collection(self, name: str, description: str = "") -> bool:
        """Create a new URL collection"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO collections (name, description) VALUES (?, ?)
            ''', (name, description))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False  # Collection already exists
    
    def get_collections(self) -> List[Dict]:
        """Get all collections"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM collections ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows] 