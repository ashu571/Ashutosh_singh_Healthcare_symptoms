"""
Database layer for storing symptom query history
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from config import Config

class Database:
    """SQLite database handler for symptom queries"""
    
    def __init__(self, db_path: str = None):
        """Initialize database connection"""
        self.db_path = db_path or Config.DATABASE_PATH
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symptoms TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_query(self, symptoms: str, response: str, session_id: str = None) -> int:
        """
        Save a symptom query to the database
        
        Args:
            symptoms: User's symptom description
            response: LLM's response
            session_id: Optional session identifier
            
        Returns:
            Query ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO queries (symptoms, response, session_id)
            VALUES (?, ?, ?)
        ''', (symptoms, response, session_id))
        
        query_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return query_id
    
    def get_recent_queries(self, limit: int = 10) -> List[Dict]:
        """
        Get recent queries
        
        Args:
            limit: Maximum number of queries to return
            
        Returns:
            List of query dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, symptoms, response, timestamp
            FROM queries
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_query_by_id(self, query_id: int) -> Optional[Dict]:
        """
        Get a specific query by ID
        
        Args:
            query_id: Query ID
            
        Returns:
            Query dictionary or None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, symptoms, response, timestamp
            FROM queries
            WHERE id = ?
        ''', (query_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def clear_old_queries(self, days: int = 30):
        """
        Clear queries older than specified days
        
        Args:
            days: Number of days to keep
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM queries
            WHERE timestamp < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        conn.commit()
        conn.close()
