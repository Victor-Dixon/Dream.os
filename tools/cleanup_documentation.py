import os
import shutil
from datetime import datetime, timedelta
import glob

def cleanup_reports():
    print("Cleaning up reports/ directory...")
    report_dir = "/workspace/reports"
    
    # Patterns to clean
    patterns = [
        "cycle_accomplishments_*.md",
        "ssot_validation_*.md",
        "ssot_validation_*.json",
        "grade_cards_audit_*.json",
        "security_audit_*.json"
    ]
    
    for pattern in patterns:
        files = glob.glob(os.path.join(report_dir, pattern))
        # Sort by modification time (newest first)
        files.sort(key=os.path.getmtime, reverse=True)
        
        # Keep top 2, delete rest
        for f in files[2:]:
            print(f"Deleting old report: {os.path.basename(f)}")
            os.remove(f)

def cleanup_tech_debt_reports():
    print("\nCleaning up systems/technical_debt/reports/ directory...")
    report_dir = "/workspace/systems/technical_debt/reports"
    
    # Clean all JSONs/MDs, keep latest of each type if possible, or just latest 2 overall?
    # Let's keep latest 2 overall for safety.
    files = glob.glob(os.path.join(report_dir, "*"))
    files = [f for f in files if os.path.isfile(f)]
    files.sort(key=os.path.getmtime, reverse=True)
    
    for f in files[2:]:
         print(f"Deleting old tech debt report: {os.path.basename(f)}")
         os.remove(f)

def archive_website_audits():
    print("\nArchiving old website audits...")
    audit_dir = "/workspace/docs/website_audits"
    archive_dir = "/workspace/docs/archive/audits"
    
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        
    # Move files older than 7 days
    cutoff = datetime.now() - timedelta(days=7)
    
    for filename in os.listdir(audit_dir):
        file_path = os.path.join(audit_dir, filename)
        if os.path.isfile(file_path):
            # Check if it has a date in filename or check mtime
            # Trust mtime for now as filenames vary
            mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            if mtime < cutoff:
                print(f"Archiving: {filename}")
                shutil.move(file_path, os.path.join(archive_dir, filename))

def cleanup_temp_txt_files():
    print("\nCleaning up root .txt files...")
    root_dir = "/workspace"
    archive_dir = "/workspace/docs/archive/logs"
    
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        
    for filename in os.listdir(root_dir):
        if filename.endswith(".txt"):
            if filename in ["requirements.txt", "requirements-dev.txt"]:
                continue
            file_path = os.path.join(root_dir, filename)
            print(f"Archiving log: {filename}")
            shutil.move(file_path, os.path.join(archive_dir, filename))

def cleanup_docs_root():
    print("\nCleaning up docs/ root dated files...")
    docs_dir = "/workspace/docs"
    archive_dir = "/workspace/docs/archive/misc"
    
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    
    # Archive website_audit_report_*.json
    files = glob.glob(os.path.join(docs_dir, "website_audit_report_*.json"))
    for f in files:
        print(f"Archiving: {os.path.basename(f)}")
        shutil.move(f, os.path.join(archive_dir, os.path.basename(f)))
    
    # Archive other dated MD files older than 7 days
    cutoff = datetime.now() - timedelta(days=7)
    for filename in os.listdir(docs_dir):
        if filename.endswith(".md") and ("_202" in filename): # Simple check for year
            file_path = os.path.join(docs_dir, filename)
            if os.path.isfile(file_path):
                 mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                 if mtime < cutoff:
                     print(f"Archiving dated doc: {filename}")
                     shutil.move(file_path, os.path.join(archive_dir, filename))

if __name__ == "__main__":
    cleanup_reports()
    cleanup_tech_debt_reports()
    archive_website_audits()
    cleanup_temp_txt_files()
    cleanup_docs_root()
    print("\nCleanup complete!")
