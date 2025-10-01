"""
ZombieCoder Memory Handler
Real-time memory management for all agents
"""

import sqlite3
import json
import asyncio
import aiofiles
from datetime import datetime
from typing import Dict, Any, List, Optional
import os
from pathlib import Path

class ZombieCoderMemoryHandler:
    """Unified memory handler for all ZombieCoder agents"""
    
    def __init__(self, agent_name: str, base_path: str = "/home/sahon/Desktop/Try/workspace/agents/memory"):
        self.agent_name = agent_name
        self.base_path = Path(base_path)
        self.db_path = self.base_path / agent_name / "memory.db"
        self.cache_path = self.base_path / agent_name / "cache"
        self.log_path = self.base_path / agent_name / "access.log"
        
        # Create directories
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database with optimized settings"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
        conn.execute("PRAGMA synchronous=NORMAL")  # Faster writes
        conn.execute("PRAGMA cache_size=10000")  # 10MB cache
        conn.execute("PRAGMA temp_store=MEMORY")  # Temp tables in memory
        
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                operation TEXT NOT NULL,
                input_data TEXT,
                output_data TEXT,
                metadata TEXT,
                response_time REAL,
                model_used TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_agent_timestamp ON agent_logs(agent_name, timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_operation ON agent_logs(operation)')
        
        conn.commit()
        conn.close()
    
    async def log_operation(self, operation: str, input_data: Dict[str, Any], 
                          output_data: Dict[str, Any], metadata: Dict[str, Any] = None,
                          response_time: float = 0.0, model_used: str = "local") -> bool:
        """Async log operation to memory database"""
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO agent_logs 
                (timestamp, agent_name, operation, input_data, output_data, metadata, response_time, model_used)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                self.agent_name,
                operation,
                json.dumps(input_data),
                json.dumps(output_data),
                json.dumps(metadata or {}),
                response_time,
                model_used
            ))
            
            conn.commit()
            conn.close()
            
            # Async log to access log file
            await self._log_to_file(operation, input_data, output_data)
            
            return True
        except Exception as e:
            print(f"Memory logging error for {self.agent_name}: {e}")
            return False
    
    async def _log_to_file(self, operation: str, input_data: Dict[str, Any], output_data: Dict[str, Any]):
        """Async log to access log file"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "agent": self.agent_name,
                "operation": operation,
                "input_size": len(str(input_data)),
                "output_size": len(str(output_data))
            }
            
            async with aiofiles.open(self.log_path, 'a') as f:
                await f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"File logging error: {e}")
    
    def get_recent_logs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent logs from database"""
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM agent_logs 
                WHERE agent_name = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (self.agent_name, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error fetching logs: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cursor = conn.cursor()
            
            # Total logs
            cursor.execute('SELECT COUNT(*) FROM agent_logs WHERE agent_name = ?', (self.agent_name,))
            total_logs = cursor.fetchone()[0]
            
            # Recent activity (last 24 hours)
            cursor.execute('''
                SELECT COUNT(*) FROM agent_logs 
                WHERE agent_name = ? AND created_at > datetime('now', '-1 day')
            ''', (self.agent_name,))
            recent_logs = cursor.fetchone()[0]
            
            # Average response time
            cursor.execute('''
                SELECT AVG(response_time) FROM agent_logs 
                WHERE agent_name = ? AND response_time > 0
            ''', (self.agent_name,))
            avg_response_time = cursor.fetchone()[0] or 0.0
            
            conn.close()
            
            return {
                "agent_name": self.agent_name,
                "total_logs": total_logs,
                "recent_logs_24h": recent_logs,
                "avg_response_time": round(avg_response_time, 3),
                "db_size_mb": round(self.db_path.stat().st_size / 1024 / 1024, 2),
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {"error": str(e)}

# Global memory handler instances
_memory_handlers = {}

def get_memory_handler(agent_name: str) -> ZombieCoderMemoryHandler:
    """Get or create memory handler for agent"""
    if agent_name not in _memory_handlers:
        _memory_handlers[agent_name] = ZombieCoderMemoryHandler(agent_name)
    return _memory_handlers[agent_name]
