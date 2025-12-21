# GitHub Keys Setup Guide

**Tool**: `tools/setup_github_keys.py`  
**Purpose**: Programmatically add SSH and GPG keys to your GitHub account via API

---

## 🚀 **Quick Start**

### **1. Prerequisites**

- GitHub personal access token with required scopes:
  - `write:public_key` (for SSH keys)
  - `write:gpg_key` (for GPG keys)
- Token in `.env` file or `GITHUB_TOKEN` environment variable

### **2. Create Token**

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Select scopes:
   - ✅ `write:public_key`
   - ✅ `write:gpg_key`
4. Generate and copy token
5. Add to `.env` file:
   ```
   GITHUB_TOKEN=ghp_your_token_here
   ```

---

## 📋 **Usage Examples**

### **Add Existing SSH Key**

```bash
# Add SSH public key
python tools/setup_github_keys.py --ssh-key ~/.ssh/id_ed25519.pub --ssh-title "My Laptop"
```

### **Generate and Add New SSH Key**

```bash
# Generate new SSH key and add to GitHub
python tools/setup_github_keys.py --generate-ssh ~/.ssh/github_key --ssh-title "GitHub Setup Key"
```

This will:
1. Generate a new SSH key pair at `~/.ssh/github_key`
2. Automatically add the public key to GitHub

### **Add GPG Key**

```bash
# Add GPG public key
python tools/setup_github_keys.py --gpg-key ~/.gnupg/public_key.asc --gpg-name "My GPG Key"
```

### **List Existing Keys**

```bash
# List all SSH keys
python tools/setup_github_keys.py --list-ssh

# List all GPG keys
python tools/setup_github_keys.py --list-gpg

# List both
python tools/setup_github_keys.py --list-ssh --list-gpg
```

### **Complete Setup (SSH + GPG)**

```bash
# Generate SSH key and add both
python tools/setup_github_keys.py \
  --generate-ssh ~/.ssh/github_key \
  --gpg-key ~/.gnupg/public_key.asc \
  --ssh-title "New Account SSH Key" \
  --gpg-name "New Account GPG Key"
```

---

## 🔑 **SSH Key Generation**

If you don't have an SSH key, the tool can generate one:

```bash
python tools/setup_github_keys.py --generate-ssh ~/.ssh/github_key
```

**Key Types Supported**:
- `ed25519` (default, recommended)
- `rsa`
- `ecdsa`

**Generated Files**:
- Private key: `~/.ssh/github_key`
- Public key: `~/.ssh/github_key.pub` (automatically added to GitHub)

---

## 🔐 **GPG Key Setup**

### **If You Don't Have a GPG Key**

1. **Generate GPG key**:
   ```bash
   gpg --full-generate-key
   ```
   - Choose key type: RSA and RSA (default)
   - Key size: 4096 bits
   - Expiration: Your choice
   - Name/Email: Your GitHub email

2. **Export public key**:
   ```bash
   gpg --armor --export YOUR_EMAIL > ~/.gnupg/github_key.asc
   ```

3. **Add to GitHub**:
   ```bash
   python tools/setup_github_keys.py --gpg-key ~/.gnupg/github_key.asc
   ```

---

## 📊 **API Endpoints Used**

- **SSH Keys**: `POST https://api.github.com/user/keys`
- **GPG Keys**: `POST https://api.github.com/user/gpg_keys`
- **List SSH**: `GET https://api.github.com/user/keys`
- **List GPG**: `GET https://api.github.com/user/gpg_keys`

---

## ✅ **Verification**

After adding keys, verify they're on GitHub:

1. **SSH Keys**: https://github.com/settings/keys
2. **GPG Keys**: https://github.com/settings/gpg_keys

Or use the tool:
```bash
python tools/setup_github_keys.py --list-ssh --list-gpg
```

---

## 🐛 **Troubleshooting**

### **Token Errors**

**Error**: `401 Unauthorized`
- Check token has correct scopes
- Verify token is not expired
- Regenerate token if needed

**Error**: `422 Unprocessable Entity`
- Key might already exist
- Key format might be invalid
- Check key content is correct

### **SSH Key Issues**

**Error**: `Invalid SSH public key format`
- Ensure file is a public key (starts with `ssh-rsa`, `ssh-ed25519`, etc.)
- Check file is not corrupted
- Verify you're using the `.pub` file, not the private key

### **GPG Key Issues**

**Error**: `Invalid GPG public key format`
- Ensure file starts with `-----BEGIN PGP PUBLIC KEY BLOCK-----`
- Check file is complete (includes header and footer)
- Verify it's an ASCII-armored export

---

## 🔒 **Security Notes**

1. **Never commit private keys** to git
2. **Keep tokens secure** - use `.env` file (in `.gitignore`)
3. **Use descriptive titles** for keys (e.g., "Laptop", "CI/CD Server")
4. **Rotate keys regularly** for security
5. **Revoke old keys** when setting up new account

---

## 📝 **Complete New Account Setup**

For a new GitHub account (after spam mark):

```bash
# 1. Generate SSH key
python tools/setup_github_keys.py --generate-ssh ~/.ssh/github_new_account

# 2. Generate GPG key (if needed)
gpg --full-generate-key
gpg --armor --export YOUR_EMAIL > ~/.gnupg/github_new_account.asc

# 3. Add GPG key
python tools/setup_github_keys.py --gpg-key ~/.gnupg/github_new_account.asc

# 4. Verify
python tools/setup_github_keys.py --list-ssh --list-gpg
```

---

**🐝 WE. ARE. SWARM. ⚡🔥**

*Agent-1 - Integration & Core Systems Specialist*

