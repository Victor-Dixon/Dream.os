#!/usr/bin/env python3
"""
Environment Variable Management Tool
====================================

Generates .env.example from .env and sets environment variables.

Usage:
    python tools/manage_env.py [--generate-example] [--load-env] [--env-file <path>]

Options:
    --generate-example    Generate .env.example from .env
    --load-env            Load .env and set environment variables
    --env-file <path>     Path to .env file (default: .env)
    --example-file <path> Path to .env.example file (default: env.example)
"""

import sys
import os
import re
import argparse
from pathlib import Path
from typing import Dict, List

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def parse_env_file(env_path: Path) -> Dict[str, str]:
    """
    Parse .env file and return key-value pairs.
    
    Returns:
        dict of environment variable key-value pairs
    """
    if not env_path.exists():
        return {}
    
    env_vars = {}
    content = env_path.read_text(encoding='utf-8')
    
    for line in content.split('\n'):
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue
        
        # Parse KEY=VALUE
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            
            env_vars[key] = value
    
    return env_vars


def is_sensitive_key(key: str) -> bool:
    """Check if key contains sensitive information."""
    sensitive_patterns = [
        'password', 'secret', 'key', 'token', 'api_key', 'access_token',
        'private', 'credential', 'auth', 'pwd', 'passwd'
    ]
    key_lower = key.lower()
    return any(pattern in key_lower for pattern in sensitive_patterns)


def generate_example(env_vars: Dict[str, str], example_path: Path, preserve_comments: bool = True) -> str:
    """
    Generate .env.example from .env variables, merging with existing example.
    
    Args:
        env_vars: Dictionary of environment variables from .env
        example_path: Path to existing .env.example (for comments)
        preserve_comments: Whether to preserve comments from existing example
    
    Returns:
        Merged .env.example content with all variables from both files
    """
    # Read existing example for comments/structure and existing variables
    existing_comments = {}
    existing_structure = []
    existing_vars = {}
    
    if example_path.exists() and preserve_comments:
        content = example_path.read_text(encoding='utf-8')
        current_section = None
        prev_line_was_comment = False
        prev_comment = None
        
        for line in content.split('\n'):
            # Track section headers
            if line.startswith('#') and ('=' not in line or line.startswith('##')):
                if line.startswith('##'):
                    current_section = line
                existing_structure.append(line)
                prev_line_was_comment = True
                prev_comment = line
                continue
            
            # Extract variables and comments
            if '=' in line and not line.strip().startswith('#'):
                key = line.split('=')[0].strip()
                value = line.split('=', 1)[1].strip()
                
                # Store existing variable
                existing_vars[key] = value
                
                # Store comment if previous line was a comment
                if prev_line_was_comment and prev_comment:
                    existing_comments[key] = prev_comment.lstrip('#').strip()
                elif '#' in value:
                    # Inline comment
                    comment = value.split('#', 1)[1].strip()
                    existing_comments[key] = comment
                
                prev_line_was_comment = False
                prev_comment = None
            else:
                prev_line_was_comment = False
                prev_comment = None
    
    # Merge: Combine variables from both .env and existing example
    merged_vars = {}
    merged_vars.update(existing_vars)  # Start with existing example vars
    merged_vars.update(env_vars)  # Add/update with .env vars (env vars take precedence)
    
    # Generate merged example
    lines = []
    
    # Preserve existing structure if available
    if existing_structure:
        # Rebuild structure with merged variables
        for line in existing_structure:
            if line.startswith('##'):
                lines.append(line)
            elif line.startswith('#'):
                lines.append(line)
            elif '=' in line and not line.strip().startswith('#'):
                # Replace variable line with merged version
                key = line.split('=')[0].strip()
                if key in merged_vars:
                    comment = existing_comments.get(key, '')
                    if comment and not comment.startswith('#'):
                        lines.append(f"# {comment}")
                    # Use existing placeholder format if available, otherwise mask
                    existing_val = existing_vars.get(key, '')
                    if existing_val and existing_val.strip() and not is_sensitive_key(key):
                        # Keep existing placeholder
                        lines.append(f"{key}={existing_val}")
                    elif is_sensitive_key(key):
                        lines.append(f"{key}=your_{key.lower()}_here")
                    else:
                        lines.append(f"{key}=")
                    lines.append("")
            else:
                lines.append(line)
    else:
        # No existing structure, create new
        lines.append("# Environment Configuration - Agent Cellphone V2")
        lines.append("# Copy this file to .env and modify as needed")
        lines.append("")
    
    # Add any new variables not in existing structure
    new_vars = {k: v for k, v in merged_vars.items() if k not in existing_vars}
    
    if new_vars:
        # Group new variables by prefix
        grouped_new_vars = {}
        standalone_new_vars = []
        
        for key in sorted(new_vars.keys()):
            if '_' in key:
                prefix = key.split('_')[0]
                if prefix not in grouped_new_vars:
                    grouped_new_vars[prefix] = []
                grouped_new_vars[prefix].append(key)
            else:
                standalone_new_vars.append(key)
        
        # Add new standalone variables
        if standalone_new_vars:
            for key in sorted(standalone_new_vars):
                comment = existing_comments.get(key, '')
                if comment:
                    lines.append(f"# {comment}")
                if is_sensitive_key(key):
                    lines.append(f"{key}=your_{key.lower()}_here")
                else:
                    lines.append(f"{key}=")
                lines.append("")
        
        # Add new grouped variables with section headers
        for prefix in sorted(grouped_new_vars.keys()):
            section_name = prefix.replace('_', ' ').title()
            lines.append(f"# {section_name} Configuration")
            lines.append("")
            
            for key in sorted(grouped_new_vars[prefix]):
                comment = existing_comments.get(key, '')
                if comment:
                    lines.append(f"# {comment}")
                if is_sensitive_key(key):
                    lines.append(f"{key}=your_{key.lower()}_here")
                else:
                    lines.append(f"{key}=")
                lines.append("")
    
    return '\n'.join(lines)


def load_env_vars(env_vars: Dict[str, str]) -> int:
    """
    Set environment variables from dictionary.
    
    Returns:
        Number of variables set
    """
    count = 0
    for key, value in env_vars.items():
        os.environ[key] = value
        count += 1
    
    return count


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Manage environment variables and .env.example',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate .env.example from .env
  python tools/manage_env.py --generate-example
  
  # Load .env and set environment variables
  python tools/manage_env.py --load-env
  
  # Both operations
  python tools/manage_env.py --generate-example --load-env
  
  # Custom file paths
  python tools/manage_env.py --env-file .env.local --example-file env.example.local
        """
    )
    
    parser.add_argument(
        '--generate-example',
        action='store_true',
        help='Generate .env.example from .env'
    )
    
    parser.add_argument(
        '--load-env',
        action='store_true',
        help='Load .env and set environment variables'
    )
    
    parser.add_argument(
        '--env-file',
        type=str,
        default='.env',
        help='Path to .env file (default: .env)'
    )
    
    parser.add_argument(
        '--example-file',
        type=str,
        default='env.example',
        help='Path to .env.example file (default: env.example)'
    )
    
    args = parser.parse_args()
    
    # Resolve file paths
    env_file = project_root / args.env_file
    example_file = project_root / args.example_file
    
    # If no operations specified, do both
    if not args.generate_example and not args.load_env:
        args.generate_example = True
        args.load_env = True
    
    # Parse .env file
    if not env_file.exists():
        print(f"❌ .env file not found: {env_file}")
        print(f"   Create {env_file} or specify different path with --env-file")
        sys.exit(1)
    
    env_vars = parse_env_file(env_file)
    print(f"📋 Loaded {len(env_vars)} environment variables from {env_file}")
    
    # Generate .env.example
    if args.generate_example:
        example_content = generate_example(env_vars, example_file)
        example_file.write_text(example_content, encoding='utf-8')
        print(f"✅ Generated .env.example: {example_file}")
        print(f"   {len(env_vars)} variables included")
    
    # Load environment variables
    if args.load_env:
        count = load_env_vars(env_vars)
        print(f"✅ Loaded {count} environment variables into current process")
        print("   Note: Variables are set for this process only")
        print("   Use python-dotenv's load_dotenv() in your code for persistent loading")
        
        # Show how to use in code
        print("\n💡 To load in your Python code:")
        print("   from dotenv import load_dotenv")
        print("   load_dotenv()  # Loads .env automatically")
    
    sys.exit(0)


if __name__ == '__main__':
    main()

