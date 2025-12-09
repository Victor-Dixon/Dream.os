# GitHub Repository Transfer Guide

**Purpose**: Transfer repositories from old GitHub account to new FG Professional Development Account

**Tool**: `tools/transfer_repos_to_new_github.py`

---

## 🚀 **Quick Start**

### **1. Setup SSH/GPG Keys First**

Before transferring repos, ensure SSH/GPG keys are set up:

```bash
# Setup SSH key
python tools/setup_github_keys.py --generate-ssh ~/.ssh/fg_professional_dev --ssh-title "FG Professional Dev Account"

# Setup GPG key (if needed)
gpg --full-generate-key
gpg --armor --export your_email@example.com > ~/.gnupg/fg_professional_dev.asc
python tools/setup_github_keys.py --gpg-key ~/.gnupg/fg_professional_dev.asc --gpg-name "FG Professional Dev Account"
```

### **2. Ensure Token Has Repository Permissions**

Your `FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN` needs:
- ✅ `repo` scope (full control of private repositories)
- ✅ Or for fine-grained tokens: `Repositories` → `Read and write`

---

## 📋 **Transfer Single Repository**

### **From Repository Directory**

```bash
cd /path/to/your/repo
python tools/transfer_repos_to_new_github.py
```

### **From Anywhere**

```bash
python tools/transfer_repos_to_new_github.py /path/to/your/repo
```

### **Create Private Repository**

```bash
python tools/transfer_repos_to_new_github.py --private
```

### **With Custom Description**

```bash
python tools/transfer_repos_to_new_github.py --description "My awesome project"
```

---

## 🔍 **List Local Repositories**

Find all git repositories in a directory:

```bash
python tools/transfer_repos_to_new_github.py --list-repos
```

Or from specific directory:

```bash
python tools/transfer_repos_to_new_github.py --list-repos /path/to/search
```

---

## 🔄 **What the Tool Does**

1. **Creates new repository** on new GitHub account
2. **Updates local git remote** to point to new account
3. **Pushes all code** to new repository
4. **Preserves branch structure** (main/master)

---

## 📝 **Manual Transfer Steps** (Alternative)

If you prefer manual control:

### **1. Create Repository on GitHub**

1. Go to: https://github.com/new
2. Create repository with same name
3. **Don't** initialize with README/license

### **2. Update Local Remote**

```bash
cd /path/to/your/repo
git remote set-url origin https://github.com/NEW_USERNAME/REPO_NAME.git
```

### **3. Push Code**

```bash
git push -u origin main
# Or if using master:
git push -u origin master
```

---

## 🔐 **SSH vs HTTPS**

### **Using SSH** (Recommended)

After SSH key is set up:

```bash
# Update remote to use SSH
git remote set-url origin git@github.com:NEW_USERNAME/REPO_NAME.git
git push -u origin main
```

### **Using HTTPS**

```bash
# Update remote to use HTTPS
git remote set-url origin https://github.com/NEW_USERNAME/REPO_NAME.git
git push -u origin main
```

**Note**: HTTPS will prompt for credentials. Use token as password.

---

## 🎯 **Bulk Transfer Workflow**

### **Step 1: List All Repos**

```bash
python tools/transfer_repos_to_new_github.py --list-repos
```

### **Step 2: Transfer Each Repo**

```bash
# For each repository
cd /path/to/repo1
python tools/transfer_repos_to_new_github.py

cd /path/to/repo2
python tools/transfer_repos_to_new_github.py --private

cd /path/to/repo3
python tools/transfer_repos_to_new_github.py --description "Custom description"
```

---

## ⚠️ **Important Notes**

### **Old Repository**

- **Don't delete** old repository immediately
- Keep as backup until you verify new repo works
- You can archive it later: Settings → Archive repository

### **Collaborators**

- Collaborators need to be re-invited to new repositories
- Update any CI/CD pipelines with new repository URLs

### **Issues & Pull Requests**

- Issues/PRs don't transfer automatically
- Export manually if needed: Settings → Export repository data

### **Releases & Tags**

- Tags are pushed automatically with `git push --tags`
- Releases need to be recreated manually

---

## 🔧 **Troubleshooting**

### **Token Permissions**

**Error**: "Resource not accessible by personal access token"

**Fix**: 
- For classic tokens: Ensure `repo` scope is selected
- For fine-grained tokens: Set `Repositories` → `Read and write`

### **Repository Already Exists**

**Error**: "Repository already exists"

**Fix**: 
- Delete existing repository on GitHub first
- Or use different name: `--new-name different-name`

### **Push Fails**

**Error**: "Permission denied" or "Authentication failed"

**Fix**:
- Verify SSH key is added: `python tools/setup_github_keys.py --list-ssh`
- Test SSH connection: `ssh -T git@github.com`
- Or use HTTPS with token as password

### **Remote URL Not Updated**

**Error**: Remote still points to old account

**Fix**:
```bash
git remote -v  # Check current remote
git remote set-url origin https://github.com/NEW_USERNAME/REPO_NAME.git
git remote -v  # Verify update
```

---

## 📊 **Verification Checklist**

After transfer:

- [ ] Repository exists on new GitHub account
- [ ] All branches pushed successfully
- [ ] Local remote URL updated
- [ ] Code is accessible on new account
- [ ] SSH/HTTPS authentication works
- [ ] Old repository archived (optional)

---

## 🚀 **Next Steps After Transfer**

1. **Update CI/CD**: Update repository URLs in GitHub Actions, etc.
2. **Update Documentation**: Update any links to repositories
3. **Notify Collaborators**: Share new repository URLs
4. **Archive Old Repos**: Archive old repositories (don't delete immediately)

---

**🐝 WE. ARE. SWARM. ⚡🔥**

*Agent-1 - Integration & Core Systems Specialist*

