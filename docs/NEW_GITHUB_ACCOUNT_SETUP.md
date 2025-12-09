# New GitHub Account Setup Guide

**Purpose**: Set up SSH and GPG keys for new GitHub account (FG Professional Development Account)

**Tool**: `tools/setup_github_keys.py`

---

## 🚀 **Quick Setup**

### **1. Create GitHub Personal Access Token**

**Option A: Classic Token (Recommended for Keys Setup)**

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. **Name**: `FG Professional Development Account - Keys Setup`
4. **Expiration**: Your choice (90 days recommended)
5. **Select Scopes**:
   - ✅ `write:public_key` (for SSH keys)
   - ✅ `write:gpg_key` (for GPG keys)
6. Click "Generate token"
7. **Copy the token immediately** (you won't see it again!)

**Option B: Fine-Grained Token**

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (fine-grained)"
3. **Name**: `FG Professional Development Account - Keys Setup`
4. **Expiration**: Your choice
5. **Account permissions**:
   - ✅ `Public SSH keys` → **Read and write**
   - ✅ `GPG keys` → **Read and write**
6. Click "Generate token"
7. **Copy the token immediately** (you won't see it again!)

**Note**: Fine-grained tokens (`github_pat_...`) require explicit account permissions. Make sure to set both SSH and GPG keys to "Read and write" access.

### **2. Add Token to .env File**

Add to your `.env` file in project root:

```bash
# New GitHub account token (for professional development account)
FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN=ghp_your_token_here
```

**Or set as environment variable**:
```powershell
$env:FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN = "ghp_your_token_here"
```

---

## 🔑 **Setup SSH Key**

### **Option 1: Generate New SSH Key**

```bash
# Generate and automatically add to GitHub
python tools/setup_github_keys.py --generate-ssh ~/.ssh/fg_professional_dev --ssh-title "FG Professional Dev Account"
```

This will:
1. Generate a new SSH key pair at `~/.ssh/fg_professional_dev`
2. Automatically add the public key to your new GitHub account

### **Option 2: Use Existing SSH Key**

```bash
# Add existing SSH key
python tools/setup_github_keys.py --ssh-key ~/.ssh/id_ed25519.pub --ssh-title "FG Professional Dev Account"
```

---

## 🔐 **Setup GPG Key**

### **1. Generate GPG Key (if needed)**

```bash
# Generate new GPG key
gpg --full-generate-key
```

**When prompted**:
- Key type: `RSA and RSA` (default)
- Key size: `4096`
- Expiration: Your choice
- Name: Your name
- Email: **Use the email associated with your new GitHub account**

### **2. Export GPG Public Key**

```bash
# Export public key (replace with your email)
gpg --armor --export your_email@example.com > ~/.gnupg/fg_professional_dev.asc
```

### **3. Add to GitHub**

```bash
python tools/setup_github_keys.py --gpg-key ~/.gnupg/fg_professional_dev.asc --gpg-name "FG Professional Dev Account"
```

---

## ✅ **Verify Setup**

### **List Keys on GitHub**

```bash
python tools/setup_github_keys.py --list-ssh --list-gpg
```

### **Verify on GitHub Website**

1. **SSH Keys**: https://github.com/settings/keys
2. **GPG Keys**: https://github.com/settings/gpg_keys

---

## 📋 **Complete Setup Workflow**

```bash
# 1. Generate SSH key and add to GitHub
python tools/setup_github_keys.py --generate-ssh ~/.ssh/fg_professional_dev --ssh-title "FG Professional Dev Account"

# 2. Generate GPG key (if needed)
gpg --full-generate-key
gpg --armor --export your_email@example.com > ~/.gnupg/fg_professional_dev.asc

# 3. Add GPG key to GitHub
python tools/setup_github_keys.py --gpg-key ~/.gnupg/fg_professional_dev.asc --gpg-name "FG Professional Dev Account"

# 4. Verify both keys are added
python tools/setup_github_keys.py --list-ssh --list-gpg
```

---

## 🔧 **Configure Git to Use New Account**

After keys are set up, configure git:

```bash
# Set git config for new account
git config --global user.name "Your New GitHub Username"
git config --global user.email "your_new_email@example.com"

# Or set per-repository
git config user.name "Your New GitHub Username"
git config user.email "your_new_email@example.com"
```

---

## 🎯 **Token Priority**

The tool checks tokens in this order:
1. `FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN` (new account)
2. `GITHUB_TOKEN` (fallback)
3. `.env` file (both variables)

---

## 📝 **Notes**

- **Token Security**: Never commit tokens to git
- **Key Management**: Use descriptive titles for keys
- **Account Separation**: This tool uses the new account token, keeping it separate from old account
- **SSH Key Location**: Keep private keys secure (`~/.ssh/` directory)

---

## 🐛 **Troubleshooting**

### **Token Not Found**
- Check `.env` file has `FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN=...`
- Verify token is not expired
- Check token has correct scopes

### **Key Already Exists**
- GitHub won't allow duplicate keys
- Use `--list-ssh` to see existing keys
- Delete old key on GitHub if needed

### **Authentication Failed**
- Verify token is valid: https://github.com/settings/tokens
- Check token has `write:public_key` and `write:gpg_key` scopes
- Regenerate token if needed

---

**🐝 WE. ARE. SWARM. ⚡🔥**

*Agent-1 - Integration & Core Systems Specialist*

