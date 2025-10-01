# 🧟 Final Kickoff Rules for Agents

## 🚀 IMMEDIATE ACTION REQUIRED - START NOW!

**Zombie Leader**: কলিজা  
**Status**: ✅ READY FOR AGENT DEPLOYMENT  
**Priority**: CRITICAL - Start Immediately  

---

## 📋 Final Kickoff Rules

### 1️⃣ **Workspace তৈরি হয়ে গেছে** ✅
- সব কাজ এখানেই হবে
- `workspace/` ফোল্ডার structure complete
- পুরনো `memory/`, `logs/`, `reports/` অপরিবর্তিত (backup)

### 2️⃣ **Docs পড়ে নাও** 📖
- `workspace/docs/AGENT_TASK_RULES.md` প্রথমে পড়তে হবে
- `workspace/docs/AGENT_WORKFLOW.md` workflow বুঝতে হবে
- `workspace/docs/QUICK_REFERENCE.md` quick reference দেখো

### 3️⃣ **Task বেছে নাও** 🎯
- নিজের specialization অনুযায়ী সিলেক্ট করো
- 5টি specialized agent, 5টি specific task
- একসাথে এক agent = এক task (parallel নয়)

### 4️⃣ **Logs আপডেট করো** 📝
- `agent_selection.log` → Task selection log
- `agent_work.log` → Work progress log
- ঠিকভাবে পূরণ করতে হবে

### 5️⃣ **Reports জমা দাও** 📊
- কাজ শেষ হলে `workspace/reports/` এ ফাইল জমা দিতে হবে
- Standardized report format ব্যবহার করো
- Blueprint match করতে হবে

### 6️⃣ **Blueprint মিলাও** ✅
- Main Blueprint এর সাথে cross-check না করলে টাস্ক incomplete
- সব কাজ blueprint match করতে হবে

---

## 🚫 Zero Tolerance Rules

### **Strict Rules - No Exceptions:**
- **Fake work** ❌
- **ভুল folder** ❌
- **Missing logs** ❌
- **Documentation update বাদ** ❌

---

## 🚀 Agents Assigned (Clean Start)

### **Programming Agent** 👨‍💻
- **Task**: Local model optimization
- **Priority**: HIGH
- **Description**: Optimize local models for better performance
- **Expected Output**: Optimized models with performance metrics

### **Best Practices Agent** 📋
- **Task**: Cloud service blocking
- **Priority**: HIGH
- **Description**: Block remaining 3 cloud services
- **Expected Output**: All cloud services blocked confirmation

### **Verifier Agent** ✅
- **Task**: Agent memory isolation
- **Priority**: MEDIUM
- **Description**: Implement per-agent memory system
- **Expected Output**: Memory isolation working properly

### **Conversational Agent** 💬
- **Task**: Dashboard enhancement
- **Priority**: MEDIUM
- **Description**: Add real-time monitoring to dashboard
- **Expected Output**: Enhanced dashboard with monitoring

### **Ops Agent** 🔧
- **Task**: Mobile optimization
- **Priority**: LOW
- **Description**: Ensure mobile responsiveness
- **Expected Output**: Mobile-optimized system

---

## 🎯 Immediate Action

### **Step 1: Read Documentation**
```bash
cd /home/sahon/Desktop/zombiecoder/workspace
cat docs/AGENT_TASK_RULES.md
cat docs/AGENT_WORKFLOW.md
cat docs/QUICK_REFERENCE.md
```

### **Step 2: Select Your Task**
```bash
# Log your task selection
echo "$(date): Agent: [Your Name], Task: [Selected Task]" >> logs/agent_selection.log
```

### **Step 3: Start Working**
```bash
# Update work log
echo "$(date): Agent: [Your Name] - Task: [Task Name] - Status: Started" >> logs/agent_work.log

# Follow workflow in docs/AGENT_WORKFLOW.md
```

### **Step 4: Update Progress**
```bash
# Regular progress updates
echo "$(date): Agent: [Your Name] - Task: [Task Name] - Status: In Progress" >> logs/agent_work.log
```

### **Step 5: Submit Report**
```bash
# Create report in reports/ folder
echo "Task completed report" > reports/[agent_name]_report.md
```

---

## 📝 Report Template (Copy-Paste Ready)

```
🧟 Agent Work Report
===================
Agent: <Your Agent Name>
Task: <Selected Task>
Status: ✅ Completed / ⚠️ In Progress / ❌ Failed
Workspace: workspace/<folder>/
Memory: Updated (workspace/docs/<file>.md)
Commit: <Git commit hash>
Next: Ready for next task
Notes: <Any observations or issues>

কলিজা, কাজ শুরু করেছি। আমাদের পথ ঠিক আছে কিনা বলো。
```

---

## 🚨 Emergency Procedures

### **If Task Fails:**
1. Stop immediately
2. Log the failure
3. Report to Zombie Leader
4. Wait for instructions

### **If System Issues:**
1. Check logs first
2. Report the issue
3. Follow recovery procedures
4. Document the incident

---

## 🧟‍♂️ Final Message from Zombie Leader

> "Agents, এখনই কাজে নামো।
> workspace/ স্ট্রাকচার তৈরি হয়ে গেছে।
> টাস্ক সিলেক্ট করো → ডকুমেন্টেশন পড়ো → কাজ শুরু করো।
> Logs & reports update ছাড়া কোনো কাজ গ্রহণযোগ্য নয়।"

---

**Kickoff Time**: $(date)  
**Status**: READY FOR IMMEDIATE DEPLOYMENT  
**Next Action**: Agents start working NOW  
**Zombie Leader**: কলিজা 🧟‍♂️
