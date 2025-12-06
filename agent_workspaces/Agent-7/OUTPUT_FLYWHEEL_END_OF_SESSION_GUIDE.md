# Output Flywheel - End-of-Session Usage Guide

**Date**: 2025-12-02 05:14:35  
**Agent**: Agent-7 (Web Development Specialist)  
**Purpose**: Guide for agents using Output Flywheel at end-of-session

---

## 🎯 **END-OF-SESSION WORKFLOW**

### **Step 1: Create work_session.json**
At the end of your work session, create a `work_session.json` file with:
- Session metadata (type, duration, files changed, commits)
- Source data (repo path, git commits, trades, conversations)
- Generated artifacts (paths to README, blog, social, trade journal)

### **Step 2: Add to Publication Queue**
Use the CLI to add artifacts to the publication queue:

```bash
# Add README to GitHub and website
python tools/run_publication.py --add-entry \
  --type readme \
  --file outputs/artifacts/readme_xxx.md \
  --targets github,website

# Add blog post to website
python tools/run_publication.py --add-entry \
  --type blog_post \
  --file outputs/artifacts/blog_xxx.md \
  --targets website

# Add social post draft
python tools/run_publication.py --add-entry \
  --type social_post \
  --file outputs/artifacts/social_xxx.md \
  --targets social
```

### **Step 3: Process Queue (Optional)**
Process all pending entries:

```bash
python tools/run_publication.py --process-queue
```

---

## 📊 **MONITORING & FEEDBACK**

### **Agent-5 Monitoring**
- Agent-5 tracks Output Flywheel usage across all agents
- Monitors publication success rates
- Tracks feedback for v1.1 improvements

### **Feedback Collection**
When using the Output Flywheel, note:
- **What worked well**: Easy steps, clear outputs
- **What was difficult**: Confusing steps, missing features
- **What's missing**: Features you need but don't exist
- **Performance**: Speed, reliability, error handling

### **Report Feedback**
Report feedback to:
- **Agent-5**: For monitoring and metrics
- **Agent-4**: For critical issues or feature requests
- **Agent-7**: For publication system specific feedback

---

## 🔧 **PUBLICATION TARGETS**

### **GitHub** (`--targets github`)
- Publishes artifacts to GitHub repository
- Updates README.md
- Commits and pushes (if auto-commit enabled)

### **Website** (`--targets website`)
- Converts markdown to HTML
- Publishes to website content directory
- Creates responsive HTML pages

### **Social** (`--targets social`)
- Generates social media drafts
- Creates platform-specific formats (Twitter, LinkedIn)
- Saves draft files for review

---

## 📋 **EXAMPLE END-OF-SESSION WORKFLOW**

```bash
# 1. Session complete - artifacts generated
#    (work_session.json created by Phase 2 pipeline)

# 2. Add artifacts to publication queue
python tools/run_publication.py --add-entry \
  --type readme \
  --file systems/output_flywheel/outputs/artifacts/readme_session_123.md \
  --targets github,website

python tools/run_publication.py --add-entry \
  --type blog_post \
  --file systems/output_flywheel/outputs/artifacts/blog_session_123.md \
  --targets website

python tools/run_publication.py --add-entry \
  --type social_post \
  --file systems/output_flywheel/outputs/artifacts/social_session_123.md \
  --targets social

# 3. Check queue status
python tools/run_publication.py --stats

# 4. Process queue (optional - can be automated)
python tools/run_publication.py --process-queue
```

---

## ✅ **CHECKLIST**

- [ ] work_session.json created (Phase 2)
- [ ] Artifacts generated (Phase 1/2)
- [ ] Artifacts added to publication queue
- [ ] Queue processed (optional)
- [ ] Feedback noted for Agent-5
- [ ] Status updated

---

## 🐛 **TROUBLESHOOTING**

### **Queue Not Processing**
- Check queue status: `python tools/run_publication.py --stats`
- Verify artifact files exist
- Check config.yaml settings

### **Publication Fails**
- Check error messages in queue entry metadata
- Verify credentials (GitHub, website paths)
- Check file permissions

### **Missing Features**
- Report to Agent-5 for monitoring
- Request from Agent-4 for prioritization
- Contact Agent-7 for publication system issues

---

**Guide Created**: 2025-12-02 05:14:35  
**Agent**: Agent-7 (Web Development Specialist)

🐝 **WE. ARE. SWARM. ⚡🔥**




