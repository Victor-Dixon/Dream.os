# 📦 Devlog Compression SSOT

**Single Source of Truth**: `tools/devlog_compressor.py`

**Status**: ✅ **ACTIVE**

---

## 🎯 **PURPOSE**

Custom compression algorithm for devlog markdown files. Automatically compresses and archives devlogs after successful Discord posting.

---

## 📁 **SSOT LOCATION**

```
tools/devlog_compressor.py
```

---

## 🔧 **FEATURES**

- ✅ Custom markdown-aware preprocessing
- ✅ Gzip compression with maximum level
- ✅ Metadata preservation
- ✅ Automatic archiving after Discord post
- ✅ Original file deletion after compression
- ✅ Archive management utilities

---

## 🚀 **AUTOMATIC INTEGRATION**

Devlogs are automatically compressed and archived when posted to Discord via `devlog_manager.py`:

1. Devlog posted to Discord ✅
2. Uploaded to Swarm Brain ✅
3. **Compressed and archived** ✅ (NEW)
4. **Original file deleted** ✅ (NEW)
5. Index updated ✅

---

## 📋 **ARCHIVE FORMAT**

- **Extension**: `.devlog.gz`
- **Location**: `devlogs/archive/`
- **Format**: Gzip-compressed JSON containing:
  - Metadata (agent, date, title, category)
  - Original content (preprocessed)
  - Compression info

---

## 🔧 **MANUAL USAGE**

### **Compress a Devlog**:
```bash
python tools/devlog_compressor.py compress --file devlog.md --agent agent-7
```

### **Decompress an Archive**:
```bash
python tools/devlog_compressor.py decompress --file archive.devlog.gz --output restored.md
```

### **List Archives**:
```bash
python tools/devlog_compressor.py list
python tools/devlog_compressor.py list --agent agent-7
```

### **Get Archive Info**:
```bash
python tools/devlog_compressor.py info --file archive.devlog.gz
```

### **Python API**:
```python
from tools.devlog_compressor import compress_and_archive, DevlogCompressor

# Compress and delete original
archive_path = compress_and_archive(
    Path("devlog.md"),
    agent="agent-7",
    delete_original=True
)

# Decompress
compressor = DevlogCompressor()
data = compressor.decompress_devlog(archive_path)
content = data['content']
metadata = data['metadata']
```

---

## 📊 **COMPRESSION DETAILS**

### **Preprocessing**:
- Normalizes line endings
- Removes excessive blank lines
- Optimizes whitespace (outside code blocks)
- Preserves markdown structure

### **Compression**:
- Gzip level 9 (maximum)
- JSON serialization with metadata
- Typical compression ratio: 60-80% reduction

### **Metadata**:
- Agent ID
- Original filename and path
- Date extracted from filename
- Title from first heading
- Category auto-detected
- Compression timestamp

---

## ✅ **VERIFICATION**

Test compression:
```bash
# Create test devlog
echo "# Test Devlog\n\nContent here" > test.md

# Compress
python tools/devlog_compressor.py compress --file test.md --agent agent-7

# Verify archive exists
ls devlogs/archive/*.devlog.gz

# Decompress and verify
python tools/devlog_compressor.py decompress --file devlogs/archive/*.devlog.gz --output restored.md
```

---

## 🐝 **WE. ARE. SWARM.**

**SSOT**: `tools/devlog_compressor.py`  
**Status**: ✅ **ACTIVE**  
**Integration**: Automatic via `devlog_manager.py`

**Devlogs are now automatically compressed and archived after Discord posting!**

---

*This document establishes `tools/devlog_compressor.py` as the SSOT for devlog compression.*

