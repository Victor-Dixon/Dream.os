#!/usr/bin/env python3
"""
HTTP Server Shim for Task Manager
Provides /tasks POST endpoint for working_tree_audit.py
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    import uvicorn
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

if HAS_FASTAPI:
    from mcp_servers.task_manager_server import add_to_inbox
    
    app = FastAPI(title="Task Manager HTTP API")
    
    
    @app.post("/tasks")
    async def create_task(request: Request):
        """Create a task via HTTP POST (for working_tree_audit.py)."""
        try:
            payload = await request.json()
            queue = payload.get("queue", "INBOX")
            owner = payload.get("owner", "")
            title = payload.get("title", "")
            metadata = payload.get("metadata", {})
            
            # Use add_to_inbox function
            agent_id = owner if owner.startswith("Agent-") else None
            task_text = title
            if metadata:
                task_text += f" (metadata: {json.dumps(metadata)})"
            
            result = add_to_inbox(task_text, agent_id=agent_id)
            
            if result.get("success"):
                return JSONResponse({
                    "id": f"task_{hash(task_text)}",
                    "task_id": f"task_{hash(task_text)}",
                    "success": True,
                    "task": task_text
                })
            else:
                return JSONResponse({
                    "success": False,
                    "error": result.get("error", "Unknown error")
                }, status_code=400)
        except Exception as e:
            return JSONResponse({
                "success": False,
                "error": str(e)
            }, status_code=500)
    
    
    @app.post("/broadcast")
    async def broadcast_message(request: Request):
        """Broadcast message endpoint (acknowledgment only for now)."""
        try:
            payload = await request.json()
            # For now, just acknowledge
            return JSONResponse({
                "success": True,
                "acknowledged": True
            })
        except Exception as e:
            return JSONResponse({
                "success": False,
                "error": str(e)
            }, status_code=500)
    
    
    def main():
        """Run HTTP server."""
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--host", default="127.0.0.1")
        parser.add_argument("--port", type=int, default=8000)
        args = parser.parse_args()
        
        uvicorn.run(app, host=args.host, port=args.port)
    
    
    if __name__ == "__main__":
        main()
else:
    # Fallback: simple HTTP server using http.server
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import urllib.parse
    
    from mcp_servers.task_manager_server import add_to_inbox
    
    
    class TaskHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path == "/tasks":
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                
                try:
                    payload = json.loads(body)
                    queue = payload.get("queue", "INBOX")
                    owner = payload.get("owner", "")
                    title = payload.get("title", "")
                    metadata = payload.get("metadata", {})
                    
                    agent_id = owner if owner.startswith("Agent-") else None
                    task_text = title
                    if metadata:
                        task_text += f" (metadata: {json.dumps(metadata)})"
                    
                    result = add_to_inbox(task_text, agent_id=agent_id)
                    
                    if result.get("success"):
                        task_id = f"task_{hash(task_text)}"
                        response = json.dumps({
                            "id": task_id,
                            "task_id": task_id,
                            "success": True,
                            "task": task_text
                        })
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(response.encode())
                    else:
                        self.send_response(400)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "success": False,
                            "error": result.get("error", "Unknown error")
                        }).encode())
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "success": False,
                        "error": str(e)
                    }).encode())
            
            elif self.path == "/broadcast":
                # Acknowledge broadcast
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "acknowledged": True
                }).encode())
            else:
                self.send_response(404)
                self.end_headers()
        
        def log_message(self, format, *args):
            # Suppress default logging
            pass
    
    
    def main():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--host", default="127.0.0.1")
        parser.add_argument("--port", type=int, default=8000)
        args = parser.parse_args()
        
        server = HTTPServer((args.host, args.port), TaskHandler)
        print(f"Task Manager HTTP Server running on http://{args.host}:{args.port}")
        server.serve_forever()
    
    
    if __name__ == "__main__":
        main()

