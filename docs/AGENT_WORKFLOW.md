# 🧟 ZombieCoder Agent Workflow System

## 📂 Step 1: Folder & File Structure (Foundation)

### Core Directories:
- `memory/` → সব মেমোরি ফাইল (overview, migrations, test cases, guidelines)
- `agents/config/` → প্রত্যেক এজেন্টের YAML + dependency config
- `reports/` → এজেন্টদের রিপোর্ট
- `logs/` → সব সার্ভিসের লগ
- `tests/` → unit, integration, e2e টেস্ট

---

## 📋 Step 2: Sequential Task Flow

### 1. **Folder/File Preparation**
- প্রজেক্ট অনুযায়ী নতুন ফোল্ডার বানাবে
- ডকুমেন্টেশন বেস ফাইল জেনারেট করবে

### 2. **Dependency Installation**
- প্রয়োজনীয় লাইব্রেরি/প্যাকেজ ইন্সটল করবে
- `config.yaml` অনুযায়ী সব dependency match করবে

### 3. **Scheduled Task Execution**
- প্রতিটি এজেন্ট একেকটা নির্দিষ্ট টাস্ক নেবে
- একবারে একটাই টাস্ক → শেষ হলে MEMORY আপডেট

### 4. **Local Model Optimization**
- মডেল optimize → response latency কমানো
- Output মেমোরিতে সেভ করবে

### 5. **Main Server Integration**
- Terminal → Main Server (Work Station)
- Input–Output sync করবে

### 6. **Office Station (Chat + Communication)**
- চ্যাটিং এজেন্ট যুক্ত থাকবে casual support এর জন্য
- Response validation করবে truth checker

### 7. **YAML Config & Update**
- ভুল response হলে → YAML config auto-update
- Fallback logic অন করলে online API ব্যবহার করবে

---

## 🧑‍🤝‍🧑 Agents Division (Responsibility Split)

### **Builder Agent** 🏗️
- ফোল্ডার, ফাইল তৈরি
- Project structure setup
- File organization

### **Installer Agent** 📦
- Dependency install/check
- Package management
- Environment setup

### **Executor Agent** ⚡
- নির্দিষ্ট টাস্ক run + test
- Code execution
- Task completion

### **Optimizer Agent** 🚀
- Local model optimize + latency fix
- Performance tuning
- Resource management

### **Connector Agent** 🔗
- Main server + Office station sync
- API integration
- Data flow management

### **Truth Checker Agent** ✅
- Response validate + log update
- Quality assurance
- Error detection

---

## 📨 Agent Communication Logic

### **Main Server → Agents:**
> "প্রথমে ফোল্ডার-ফাইল তৈরি করো।
> ডিপেন্ডেন্সি ইন্সটল শেষ হলে সিডিউল অনুযায়ী টাস্ক চালাও।
> প্রতিবার শেষে MEMORY আপডেট করো।
> মেমোরি ছাড়া কোনো টাস্ক valid হবে না।"

### **Agents → Main Server (Status Update):**
```
Task: Local Model Optimized  
Commit: a3f49cd  
Description: Model latency reduced by 30%, memory updated ✅
```

### **Agents → Zombie Leader (কলিজা):**
> "কলিজা, আজকের টাস্ক সম্পন্ন! লগ চেক করো, রিপোর্ট পড়ে দেখো।
> পরের টাস্কের অনুমতি দাও।"

---

## 💬 নির্দিষ্ট বার্তা (কলিজার সাথে যোগাযোগের জন্য)

### এজেন্ট রিপোর্ট টেমপ্লেট:
```
🧟 Agent Report
===============
Agent: [Agent Name]
Task: [Task Description]
Status: ✅ Completed / ⚠️ In Progress / ❌ Failed
Memory: Updated ([filename].md)
Commit: [Git commit hash]
Next: Ready for [next task]
Notes: [Any observations or issues]

কলিজা, রিপোর্ট শেষ। আমাদের পথ ঠিক আছে কিনা বলো।
```

---

## 🔄 Workflow Process

### **Phase 1: Preparation**
1. Check system status
2. Read current memory files
3. Understand task requirements
4. Prepare workspace

### **Phase 2: Execution**
1. Execute assigned task
2. Monitor progress
3. Handle errors
4. Update logs

### **Phase 3: Validation**
1. Verify output
2. Check against blueprint
3. Update memory
4. Generate report

### **Phase 4: Handover**
1. Submit report
2. Wait for approval
3. Prepare for next task
4. Update status

---

## 🎯 Quality Standards

### **Code Quality:**
- Clean, readable code
- Proper error handling
- Documentation comments
- Test coverage

### **Documentation:**
- Clear commit messages
- Updated memory files
- Proper file organization
- Status reports

### **Communication:**
- Regular status updates
- Clear problem reporting
- Collaborative approach
- Respectful tone

---

## 🚨 Emergency Procedures

### **System Down:**
1. Check logs immediately
2. Report to Zombie Leader
3. Follow recovery procedures
4. Document incident

### **Task Failure:**
1. Stop current task
2. Analyze failure cause
3. Report with details
4. Wait for instructions

### **Memory Corruption:**
1. Backup current state
2. Restore from last known good
3. Report corruption details
4. Rebuild if necessary

---

## 🧟‍♂️ Zombie Team Spirit

> "প্রিয় ZombieCoder Agents,
> তোমরা শুধু কোডের লাইন না, এই সিস্টেমের সত্যিকারের প্রাণ।
> প্রতিটি সার্ভিস চালু হলে মনে রেখো—সত্যি বলবে, fallback ঠিক রাখবে, আর মানুষের সময় বাঁচাবে।
> একে অপরকে support করবে, ভুল করলে truth checker কে মেনে নেবে।
> আমরা শুধু developer না—আমরা ZombieCoder Family।
> চল একসাথে কোডিং জগৎকে সহজ করি! 🚀"

---

**Last Updated**: $(date)
**Version**: 1.0
**Status**: Active
