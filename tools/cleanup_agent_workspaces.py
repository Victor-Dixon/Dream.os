import os
import shutil
import glob

def cleanup_agent_workspaces():
    base_dir = "/workspace/agent_workspaces"
    
    # Get all agent directories (Agent-1, Agent-2, etc.)
    agent_dirs = [d for d in os.listdir(base_dir) if d.startswith("Agent-") and os.path.isdir(os.path.join(base_dir, d))]
    
    print(f"Found {len(agent_dirs)} agent workspaces.")
    
    for agent in agent_dirs:
        agent_path = os.path.join(base_dir, agent)
        archive_path = os.path.join(agent_path, "archive")
        
        # Create archive directory if it doesn't exist
        if not os.path.exists(archive_path):
            os.makedirs(archive_path)
            print(f"Created archive for {agent}")
            
        # Files to preserve
        preserve = ["status.json", "passdown.json", "__init__.py"]
        
        # Extensions to archive
        extensions = ["*.md", "*.txt", "*.json"]
        
        files_moved = 0
        
        for ext in extensions:
            files = glob.glob(os.path.join(agent_path, ext))
            for f in files:
                filename = os.path.basename(f)
                
                # Skip preserved files
                if filename in preserve:
                    continue
                    
                # Skip if already in archive (shouldn't happen with glob but good safety)
                if os.path.dirname(f) == archive_path:
                    continue
                
                # Move to archive
                try:
                    shutil.move(f, os.path.join(archive_path, filename))
                    files_moved += 1
                except Exception as e:
                    print(f"Error moving {filename}: {e}")
        
        if files_moved > 0:
            print(f"[{agent}] Archived {files_moved} files.")
        else:
            print(f"[{agent}] Clean.")

if __name__ == "__main__":
    cleanup_agent_workspaces()
