# 🧟 Zombie Agent Quick Reference Card

## 🚀 Quick Start Checklist

### **Before Starting Any Task:**
- [ ] Check system status: `./SYSTEM_CHECKER.sh`
- [ ] Read current memory files
- [ ] Understand task requirements
- [ ] Prepare workspace

### **During Task:**
- [ ] Create required folders
- [ ] Install dependencies
- [ ] Organize files properly
- [ ] Update logs regularly

### **After Task:**
- [ ] Verify output
- [ ] Update memory files
- [ ] Submit report
- [ ] Wait for approval

---

## 📁 Folder Structure (Must Have)

```
project-root/
├── memory/           # All documentation
├── agents/           # Agent system
│   └── config/       # Agent configs
├── logs/             # All log files
├── reports/          # Generated reports
├── tests/            # Test files
└── README.md         # Project README
```

---

## 📝 Report Template (Copy-Paste)

```
🧟 Agent Report
===============
Agent: <Agent Name>
Task: <Task Description>
Status: ✅ Completed / ❌ Failed
Memory: Updated (file_name.md)
Commit: <Git commit hash>
Next: Ready for next task
Notes: <Any observations>

কলিজা, রিপোর্ট শেষ। আমাদের পথ ঠিক আছে কিনা বলো।
```

---

## 🔧 Essential Commands

### **System Control:**
```bash
# Check status
./SYSTEM_CHECKER.sh

# Start all services
./COMPLETE_SYSTEM_LAUNCHER.sh

# Stop all services
pkill -f 'python3.*zombiecoder'

# View logs
tail -f logs/*.log
```

### **File Management:**
```bash
# Create folder structure
mkdir -p memory agents/config logs reports tests/{unit,integration,e2e}

# Check file permissions
ls -la

# Update git
git add . && git commit -m "Task completed"
```

---

## ⚠️ Zero Tolerance Rules

1. **No Fake Work** - Real files/folders required
2. **Folder Discipline** - Files in correct folders only
3. **Before Server** - Check logs first
4. **Documentation** - Update memory files
5. **Blueprint Check** - Match against main blueprint

---

## 🎯 Success Criteria

- [ ] All folders exist
- [ ] All files created
- [ ] Dependencies installed
- [ ] Files organized
- [ ] Logs updated
- [ ] Report submitted
- [ ] Ready for next task

---

## 🚨 Emergency Contacts

- **Zombie Leader**: কলিজা
- **System Issues**: Check logs first
- **Task Problems**: Report immediately
- **Memory Issues**: Backup and restore

---

**Quick Reference Version**: 1.0  
**Last Updated**: $(date)  
**Status**: Active
