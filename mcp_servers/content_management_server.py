#!/usr/bin/env python3
"""
Content Management MCP Server
=============================

WordPress content operations including posts, pages, categories, tags,
and content deployment across all websites.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-28
V2 Compliant: Yes (<300 lines per function)
"""

import json
import sys
import os
import requests
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import xmlrpc.client
    WORDPRESS_XMLRPC_AVAILABLE = True
except ImportError:
    WORDPRESS_XMLRPC_AVAILABLE = False


@dataclass
class WordPressCredentials:
    """WordPress site credentials."""
    url: str
    username: str
    password: str
    xmlrpc_url: Optional[str] = None

    @property
    def xmlrpc_endpoint(self) -> str:
        """Get XML-RPC endpoint URL."""
        if self.xmlrpc_url:
            return self.xmlrpc_url
        return f"{self.url}/xmlrpc.php"


@dataclass
class ContentItem:
    """WordPress content item (post/page)."""
    id: int
    title: str
    content: str
    status: str
    type: str
    categories: List[str]
    tags: List[str]
    excerpt: str = ""
    slug: str = ""
    date_created: Optional[datetime] = None


class WordPressContentManager:
    """WordPress content management operations."""

    def __init__(self, credentials: WordPressCredentials):
        self.credentials = credentials
        self.client = None

        if WORDPRESS_XMLRPC_AVAILABLE:
            try:
                self.client = xmlrpc.client.ServerProxy(self.credentials.xmlrpc_endpoint)
            except Exception as e:
                print(f"Warning: Failed to initialize XML-RPC client: {e}")

    def get_recent_posts(self, count: int = 10, post_type: str = "post") -> List[ContentItem]:
        """Get recent posts/pages."""
        if not self.client:
            return []

        try:
            # Get posts using XML-RPC
            posts_data = self.client.metaWeblog.getRecentPosts(
                0,  # blog_id (usually 0 or 1)
                self.credentials.username,
                self.credentials.password,
                count
            )

            posts = []
            for post_data in posts_data:
                # Filter by post type if specified
                if post_type != "any" and post_data.get('post_type') != post_type:
                    continue

                post = ContentItem(
                    id=int(post_data['postid']),
                    title=post_data['title'],
                    content=post_data['description'],
                    status=post_data.get('post_status', 'publish'),
                    type=post_data.get('post_type', 'post'),
                    categories=post_data.get('categories', []),
                    tags=post_data.get('mt_keywords', '').split(',') if post_data.get('mt_keywords') else [],
                    excerpt=post_data.get('mt_excerpt', ''),
                    slug=post_data.get('wp_slug', ''),
                    date_created=self._parse_date(post_data.get('dateCreated'))
                )
                posts.append(post)

            return posts

        except Exception as e:
            print(f"Error getting recent posts: {e}")
            return []

    def create_post(self, title: str, content: str, post_type: str = "post",
                   categories: List[str] = None, tags: List[str] = None,
                   status: str = "draft") -> Optional[int]:
        """Create a new post/page."""
        if not self.client:
            return None

        try:
            # Prepare post data
            post_data = {
                'title': title,
                'description': content,
                'post_type': post_type,
                'post_status': status
            }

            if categories:
                post_data['categories'] = categories
            if tags:
                post_data['mt_keywords'] = ','.join(tags)

            # Create post
            post_id = self.client.metaWeblog.newPost(
                0,  # blog_id
                self.credentials.username,
                self.credentials.password,
                post_data,
                True  # publish immediately if status is 'publish'
            )

            return int(post_id)

        except Exception as e:
            print(f"Error creating post: {e}")
            return None

    def update_post(self, post_id: int, updates: Dict[str, Any]) -> bool:
        """Update an existing post/page."""
        if not self.client:
            return False

        try:
            # Get current post data first
            current_post = self.client.metaWeblog.getPost(
                post_id,
                self.credentials.username,
                self.credentials.password
            )

            # Merge updates
            post_data = {
                'title': updates.get('title', current_post.get('title', '')),
                'description': updates.get('content', current_post.get('description', '')),
                'post_status': updates.get('status', current_post.get('post_status', 'draft')),
                'post_type': current_post.get('post_type', 'post')
            }

            if 'categories' in updates:
                post_data['categories'] = updates['categories']
            if 'tags' in updates:
                post_data['mt_keywords'] = ','.join(updates['tags'])

            # Update post
            result = self.client.metaWeblog.editPost(
                post_id,
                self.credentials.username,
                self.credentials.password,
                post_data,
                True
            )

            return bool(result)

        except Exception as e:
            print(f"Error updating post: {e}")
            return False

    def delete_post(self, post_id: int) -> bool:
        """Delete a post/page."""
        if not self.client:
            return False

        try:
            result = self.client.blogger.deletePost(
                "",  # app_key (usually empty)
                post_id,
                self.credentials.username,
                self.credentials.password,
                True  # publish status (not used for deletion)
            )
            return bool(result)
        except Exception as e:
            print(f"Error deleting post: {e}")
            return False

    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all categories."""
        if not self.client:
            return []

        try:
            categories = self.client.metaWeblog.getCategories(
                0,  # blog_id
                self.credentials.username,
                self.credentials.password
            )
            return categories
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []

    def create_category(self, name: str, description: str = "", parent_id: int = 0) -> Optional[int]:
        """Create a new category."""
        if not self.client:
            return None

        try:
            category_data = {
                'name': name,
                'description': description,
                'parent_id': parent_id
            }

            result = self.client.wp.newCategory(
                0,  # blog_id
                self.credentials.username,
                self.credentials.password,
                category_data
            )

            return int(result) if result else None

        except Exception as e:
            print(f"Error creating category: {e}")
            return None

    def upload_media(self, file_path: str, name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Upload media file to WordPress."""
        if not self.client or not os.path.exists(file_path):
            return None

        try:
            # Read file data
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # Prepare media data
            if not name:
                name = os.path.basename(file_path)

            media_data = {
                'name': name,
                'type': self._get_mime_type(file_path),
                'bits': xmlrpc.client.Binary(file_data)
            }

            # Upload media
            result = self.client.metaWeblog.newMediaObject(
                0,  # blog_id
                self.credentials.username,
                self.credentials.password,
                media_data
            )

            return result

        except Exception as e:
            print(f"Error uploading media: {e}")
            return None

    def _get_mime_type(self, file_path: str) -> str:
        """Get MIME type for file."""
        import mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or 'application/octet-stream'

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse XML-RPC date string."""
        if not date_str:
            return None
        try:
            # XML-RPC date format: 20231228T12:00:00
            return datetime.strptime(date_str, '%Y%m%dT%H:%M:%S')
        except:
            return None

    def bulk_update_content(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bulk update multiple content items."""
        results = {
            'successful': [],
            'failed': [],
            'total_processed': len(updates)
        }

        for update in updates:
            try:
                post_id = update.get('id')
                if not post_id:
                    results['failed'].append({'update': update, 'error': 'Missing post ID'})
                    continue

                success = self.update_post(post_id, update)
                if success:
                    results['successful'].append(post_id)
                else:
                    results['failed'].append({'post_id': post_id, 'error': 'Update failed'})

            except Exception as e:
                results['failed'].append({'update': update, 'error': str(e)})

        results['success_count'] = len(results['successful'])
        results['failure_count'] = len(results['failed'])

        return results

    def get_content_stats(self) -> Dict[str, Any]:
        """Get content statistics."""
        if not self.client:
            return {'error': 'XML-RPC client not available'}

        try:
            # Get post counts by status
            stats = {
                'posts': {'publish': 0, 'draft': 0, 'pending': 0, 'private': 0, 'trash': 0},
                'pages': {'publish': 0, 'draft': 0, 'pending': 0, 'private': 0, 'trash': 0},
                'total_posts': 0,
                'total_pages': 0
            }

            # Get recent posts to count (limited approach)
            recent_posts = self.get_recent_posts(100, "any")
            for post in recent_posts:
                post_type = 'posts' if post.type == 'post' else 'pages'
                status = post.status if post.status in stats[post_type] else 'publish'

                stats[post_type][status] += 1
                stats[f'total_{post_type[:-1]}s'] += 1

            return stats

        except Exception as e:
            return {'error': str(e)}


def load_credentials(site_name: str) -> Optional[WordPressCredentials]:
    """Load WordPress credentials for a site."""
    # This would typically load from a secure config file
    # For now, return None to indicate not configured
    return None


def get_recent_posts(site_name: str, count: int = 10, post_type: str = "post") -> Dict[str, Any]:
    """Get recent posts/pages from a WordPress site."""
    try:
        credentials = load_credentials(site_name)
        if not credentials:
            return {"success": False, "error": f"Credentials not found for site: {site_name}"}

        manager = WordPressContentManager(credentials)
        posts = manager.get_recent_posts(count, post_type)

        # Convert to serializable format
        posts_data = []
        for post in posts:
            posts_data.append({
                'id': post.id,
                'title': post.title,
                'content': post.content[:500] + '...' if len(post.content) > 500 else post.content,
                'status': post.status,
                'type': post.type,
                'categories': post.categories,
                'tags': post.tags,
                'excerpt': post.excerpt,
                'slug': post.slug,
                'date_created': post.date_created.isoformat() if post.date_created else None
            })

        return {
            "success": True,
            "posts": posts_data,
            "count": len(posts_data)
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def create_post(site_name: str, title: str, content: str, post_type: str = "post",
               categories: List[str] = None, tags: List[str] = None, status: str = "draft") -> Dict[str, Any]:
    """Create a new post/page."""
    try:
        credentials = load_credentials(site_name)
        if not credentials:
            return {"success": False, "error": f"Credentials not found for site: {site_name}"}

        manager = WordPressContentManager(credentials)
        post_id = manager.create_post(title, content, post_type, categories, tags, status)

        if post_id:
            return {"success": True, "post_id": post_id}
        else:
            return {"success": False, "error": "Failed to create post"}

    except Exception as e:
        return {"success": False, "error": str(e)}


def update_post(site_name: str, post_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing post/page."""
    try:
        credentials = load_credentials(site_name)
        if not credentials:
            return {"success": False, "error": f"Credentials not found for site: {site_name}"}

        manager = WordPressContentManager(credentials)
        success = manager.update_post(post_id, updates)

        return {"success": success}

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_categories(site_name: str) -> Dict[str, Any]:
    """Get categories from a WordPress site."""
    try:
        credentials = load_credentials(site_name)
        if not credentials:
            return {"success": False, "error": f"Credentials not found for site: {site_name}"}

        manager = WordPressContentManager(credentials)
        categories = manager.get_categories()

        return {
            "success": True,
            "categories": categories,
            "count": len(categories)
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_content_stats(site_name: str) -> Dict[str, Any]:
    """Get content statistics for a WordPress site."""
    try:
        credentials = load_credentials(site_name)
        if not credentials:
            return {"success": False, "error": f"Credentials not found for site: {site_name}"}

        manager = WordPressContentManager(credentials)
        stats = manager.get_content_stats()

        return {"success": True, "stats": stats}

    except Exception as e:
        return {"success": False, "error": str(e)}


def bulk_update_content(site_name: str, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Bulk update multiple content items."""
    try:
        credentials = load_credentials(site_name)
        if not credentials:
            return {"success": False, "error": f"Credentials not found for site: {site_name}"}

        manager = WordPressContentManager(credentials)
        result = manager.bulk_update_content(updates)

        return {"success": True, "result": result}

    except Exception as e:
        return {"success": False, "error": str(e)}


# MCP Server Protocol
def main():
    """MCP server main loop."""
    server_info = {"name": "content-management-server", "version": "1.0.0"}

    tools_definitions = {
        "get_recent_posts": {
            "description": "Get recent posts/pages from a WordPress site",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_name": {"type": "string", "description": "WordPress site name"},
                    "count": {"type": "integer", "description": "Number of posts to retrieve", "default": 10},
                    "post_type": {"type": "string", "description": "Post type (post, page, any)", "default": "post"}
                },
                "required": ["site_name"]
            }
        },
        "create_post": {
            "description": "Create a new post/page on a WordPress site",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_name": {"type": "string", "description": "WordPress site name"},
                    "title": {"type": "string", "description": "Post/page title"},
                    "content": {"type": "string", "description": "Post/page content"},
                    "post_type": {"type": "string", "description": "Post type", "default": "post", "enum": ["post", "page"]},
                    "categories": {"type": "array", "items": {"type": "string"}, "description": "Categories"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags"},
                    "status": {"type": "string", "description": "Post status", "default": "draft", "enum": ["draft", "publish", "pending", "private"]}
                },
                "required": ["site_name", "title", "content"]
            }
        },
        "update_post": {
            "description": "Update an existing post/page",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_name": {"type": "string", "description": "WordPress site name"},
                    "post_id": {"type": "integer", "description": "Post/page ID"},
                    "updates": {"type": "object", "description": "Fields to update (title, content, status, categories, tags)"}
                },
                "required": ["site_name", "post_id", "updates"]
            }
        },
        "get_categories": {
            "description": "Get categories from a WordPress site",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_name": {"type": "string", "description": "WordPress site name"}
                },
                "required": ["site_name"]
            }
        },
        "get_content_stats": {
            "description": "Get content statistics for a WordPress site",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_name": {"type": "string", "description": "WordPress site name"}
                },
                "required": ["site_name"]
            }
        },
        "bulk_update_content": {
            "description": "Bulk update multiple posts/pages",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_name": {"type": "string", "description": "WordPress site name"},
                    "updates": {"type": "array", "items": {"type": "object"}, "description": "List of updates with post_id and update data"}
                },
                "required": ["site_name", "updates"]
            }
        }
    }

    initialized = False

    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")

            if method == "initialize":
                initialized = True
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": tools_definitions},
                        "serverInfo": server_info
                    }
                }))
                sys.stdout.flush()

            elif method == "tools/list":
                tools_list = []
                for tool_name, tool_def in tools_definitions.items():
                    tools_list.append({
                        "name": tool_name,
                        "description": tool_def["description"],
                        "inputSchema": tool_def["inputSchema"]
                    })
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": tools_list, "serverInfo": server_info}
                }))
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})

                if tool_name == "get_recent_posts":
                    result = get_recent_posts(**arguments)
                elif tool_name == "create_post":
                    result = create_post(**arguments)
                elif tool_name == "update_post":
                    result = update_post(**arguments)
                elif tool_name == "get_categories":
                    result = get_categories(**arguments)
                elif tool_name == "get_content_stats":
                    result = get_content_stats(**arguments)
                elif tool_name == "bulk_update_content":
                    result = bulk_update_content(**arguments)
                else:
                    result = {"success": False, "error": f"Unknown tool: {tool_name}"}

                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result)}]}
                }))
                sys.stdout.flush()

            else:
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Unknown method: {method}"}
                }))
                sys.stdout.flush()

        except json.JSONDecodeError as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": request.get("id") if "request" in locals() else None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": request.get("id") if "request" in locals() else None,
                "error": {"code": -32603, "message": str(e)}
            }))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
