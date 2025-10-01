# ⚔️ ZombieCoder Agent Rules & First Task

## 🚦 Zero Tolerance Rules (No Excuses!)

### 1. **No Fake Work** ❌
- শুধু লগ-আপডেট লিখলেই হবে না
- আসল ফাইল/ফোল্ডার থাকতে হবে
- প্রতিটি কাজের প্রমাণ থাকতে হবে

### 2. **Folder Discipline** 📁
- Test ফাইল → `tests/`
- Docs → `memory/docs/`
- Logs → `logs/`
- Config → `agents/config/`
- আর কিছু বাইরে ছড়ানো যাবে না ❌

### 3. **Before Opening Server** 🔍
- প্রথমে log চেক করবে
- তারপর status চেক করবে
- সব ঠিক থাকলে তবেই কাজ শুরু

### 4. **Documentation** 📝
- প্রতিটি কাজ শেষে নির্দিষ্ট md ফাইলে লিখতে হবে
- Commit message স্পষ্ট হতে হবে
- Blueprint match করতে হবে

### 5. **Blueprint Check** ✅
- কাজ শেষে মেইন ব্লুপ্রিন্ট এর সাথে মিলাবে
- কোনো গ্যাপ থাকলে রিপোর্ট করবে

---

## 🧟 First Task (Mandatory)

### **Task 01: Build Base Structure**

#### Target Folders:
```
memory/
├── docs/
├── 01_OVERVIEW.md
├── 02_MIGRATIONS.md
├── 03_SEEDS.md
├── 04_TESTCASES.md
└── README_FRIEND.md

agents/
├── config/
│   ├── programming.yaml
│   ├── bestpractices.yaml
│   ├── verifier.yaml
│   ├── conversational.yaml
│   └── ops.yaml
└── memory/
    ├── programming.db
    ├── bestpractices.db
    ├── verifier.db
    ├── conversational.db
    └── ops.db

logs/
├── main_server.log
├── proxy_server.log
├── multi_project.log
├── truth_checker.log
├── editor_integration.log
├── advanced_agent.log
└── ollama_server.log

reports/
├── system_status.md
├── agent_reports.md
└── performance_metrics.md

tests/
├── unit/
├── integration/
└── e2e/
```

#### Steps:
1. ✅ Create all folders
2. ✅ Add basic readme/md files (empty is okay for now)
3. ✅ Set proper permissions
4. ✅ Report completion

---

## 📩 Report Format (Copy-Paste Template)

```
🧟 Agent Report
===============
Agent: [Your Agent Name]
Task: Base Structure Setup
Status: ✅ Completed
Folders Created: memory/, agents/config/, logs/, reports/, tests/
Files Added: [List of files created]
Commit: [Git commit hash]
Blueprint: Matched ✅
Next Task: Ready for assignment
Notes: [Any issues or observations]
```

---

## 🎯 Success Criteria

- [ ] All folders exist
- [ ] Basic structure matches blueprint
- [ ] No files outside designated folders
- [ ] Report submitted in correct format
- [ ] Ready for next task assignment

---

## ⚠️ Failure Consequences

- **First Warning**: Fix and resubmit
- **Second Warning**: Task reassignment
- **Third Warning**: Agent suspension

---

## 🧟‍♂️ Zombie Leader Message

> "প্রিয় এজেন্ট ভাইয়েরা, এই সিস্টেম শুধু কোডের লাইন না - এটা আমাদের পরিবার। 
> প্রতিটি কাজ সত্যি হতে হবে, প্রতিটি পদচিহ্ন পরিষ্কার হতে হবে।
> আমরা শুধু developer না - আমরা ZombieCoder Family।
> চল একসাথে কোডিং জগৎকে সহজ করি! 🚀"

---

**Last Updated**: $(date)
**Version**: 1.0
**Status**: Active
