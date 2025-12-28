#!/usr/bin/env python3
"""
MCP Server for Database Management
Provides direct and safe database operations for swarm agents.

<!-- SSOT Domain: database -->

Author: Agent-5 (Business Intelligence Specialist)
Created: 2025-12-28
"""

import json
import os
import sys
import sqlite3
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

PROJECT_ROOT = Path(__file__).parent.parent

class DatabaseManager:
    """Manages database operations with safety checks."""

    def __init__(self):
        """Initialize the database manager."""
        self.readonly_keywords = ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN"]
        self.write_keywords = ["INSERT", "UPDATE", "DELETE", "REPLACE", "CREATE", "DROP", "ALTER", "TRUNCATE"]

    def _validate_query(self, query: str, readonly: bool = True) -> Tuple[bool, Optional[str]]:
        """Validate a query for safety and intent."""
        query_upper = query.strip().upper()
        
        if not query_upper:
            return False, "Empty query"

        # Check for multiple statements (semicolon injection)
        if ";" in query and query.strip().rstrip(";").find(";") != -1:
            return False, "Multiple statements not allowed"

        # Check readonly intent
        if readonly:
            for word in self.write_keywords:
                if re.search(rf"\b{word}\b", query_upper):
                    return False, f"Write operation '{word}' not allowed in readonly mode"
        
        return True, None

    def execute_query(self, db_path: str, query: str, params: Optional[List[Any]] = None, readonly: bool = True) -> Dict[str, Any]:
        """Execute a query on a SQLite database."""
        # For now, we only support SQLite as a safe starting point
        # In the future, this could be expanded to support MySQL/MariaDB for WordPress
        
        valid, error = self._validate_query(query, readonly)
        if not valid:
            return {"success": False, "error": error}

        try:
            path = Path(db_path)
            if not path.is_absolute():
                path = PROJECT_ROOT / path

            if not path.exists() and readonly:
                return {"success": False, "error": f"Database file not found: {db_path}"}

            conn = sqlite3.connect(f"file:{path}?mode={'ro' if readonly else 'rw'}", uri=True)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if readonly:
                rows = cursor.fetchall()
                results = [dict(row) for row in rows]
                conn.close()
                return {
                    "success": True,
                    "count": len(results),
                    "results": results
                }
            else:
                conn.commit()
                affected = cursor.rowcount
                conn.close()
                return {
                    "success": True,
                    "affected_rows": affected
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

def main():
    """MCP server main loop."""
    server_info = {"name": "database-manager-server", "version": "1.0.0"}
    db_manager = DatabaseManager()
    
    tools_definitions = {
        "execute_read_query": {
            "description": "Execute a read-only SQL query (SELECT, SHOW, etc.) on a SQLite database",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "db_path": {"type": "string", "description": "Path to the SQLite database file"},
                    "query": {"type": "string", "description": "SQL query to execute"},
                    "params": {"type": "array", "items": {"type": "string"}, "description": "Optional query parameters"}
                },
                "required": ["db_path", "query"]
            }
        },
        "execute_write_query": {
            "description": "Execute a write SQL query (INSERT, UPDATE, DELETE, etc.) on a SQLite database. Requires confirmation.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "db_path": {"type": "string", "description": "Path to the SQLite database file"},
                    "query": {"type": "string", "description": "SQL query to execute"},
                    "params": {"type": "array", "items": {"type": "string"}, "description": "Optional query parameters"},
                    "confirm": {"type": "boolean", "description": "Confirmation flag must be True to execute write operations"}
                },
                "required": ["db_path", "query", "confirm"]
            }
        }
    }

    tool_map = {
        "execute_read_query": lambda db_path, query, params=None: db_manager.execute_query(db_path, query, params, readonly=True),
        "execute_write_query": lambda db_path, query, confirm, params=None: (
            db_manager.execute_query(db_path, query, params, readonly=False) if confirm 
            else {"success": False, "error": "Write operation not confirmed"}
        )
    }

    # Handle requests from stdin
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")

            if method == "initialize":
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": tools_definitions},
                        "serverInfo": server_info,
                    },
                }))
                sys.stdout.flush()

            elif method == "tools/list":
                tools_list = [
                    {"name": name, "description": defn["description"], "inputSchema": defn["inputSchema"]}
                    for name, defn in tools_definitions.items()
                ]
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": tools_list, "serverInfo": server_info},
                }))
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})

                if tool_name in tool_map:
                    result = tool_map[tool_name](**arguments)
                else:
                    result = {"success": False, "error": f"Unknown tool: {tool_name}"}

                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result)}]},
                }))
                sys.stdout.flush()

        except json.JSONDecodeError as e:
            pass # Silent ignore
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)},
            }))
            sys.stdout.flush()

if __name__ == "__main__":
    main()

