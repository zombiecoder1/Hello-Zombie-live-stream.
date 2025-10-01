#!/usr/bin/env python3
"""
Daily Agent Instructions
Real-life workflow instructions for ZombieCoder agents
"""

import os
import json
from datetime import datetime

class DailyAgentInstructions:
    def __init__(self):
        self.instructions_file = "daily_agent_instructions.md"
        self.workflow_file = "agent_workflow.json"
        
    def create_daily_instructions(self):
        """Create daily instructions for agents"""
        instructions = f"""
# 🧟 Daily Agent Instructions - {datetime.now().strftime('%Y-%m-%d')}

## 🎯 Today's Mission: Complete System Optimization & TTS Documentation

### 📋 Priority Tasks (Complete in Order):

#### 1️⃣ Ollama Service Authentication Fix
**Agent**: Ops Agent
**Task**: Fix Ollama authentication and service permission issues
**Actions**:
- Run `python3 projects/system_fixes/ollama_auth_fix.py`
- Configure sudoers permissions for NOPASSWD
- Restart Ollama service without password prompts
- Verify service connection and API response
- Create management script for future use

**Expected Output**:
- Ollama service running without authentication errors
- Management script created in `workspace/scripts/ollama_manager.sh`
- Fix report generated with status confirmation

#### 2️⃣ System Optimization Documentation
**Agent**: Best Practices Agent
**Task**: Document system optimization and server simplification
**Actions**:
- Review current system architecture
- Document optimization changes and benefits
- Create comprehensive architecture documentation
- Update system blueprints and specifications
- Generate optimization report

**Expected Output**:
- Complete system architecture documentation
- Optimization benefits and metrics
- Updated blueprints and specifications
- Optimization report with recommendations

#### 3️⃣ Google TTS Audio Documentation
**Agent**: Conversational Agent
**Task**: Create 10-minute audio documentation using Google TTS
**Actions**:
- Run `python3 projects/tts_documentation/google_tts_generator.py`
- Generate comprehensive audio documentation
- Create metadata and completion report
- Verify audio quality and duration
- Test audio playback and accessibility

**Expected Output**:
- 10-minute audio documentation file
- Audio metadata and quality metrics
- Completion report with usage instructions
- Tested and verified audio playback

#### 4️⃣ Git Commit & Version Control
**Agent**: Programming Agent
**Task**: Commit all daily updates and changes
**Actions**:
- Review all changes and modifications
- Stage all files for commit
- Create comprehensive commit message
- Push changes to repository
- Update version and changelog

**Expected Output**:
- All changes committed to git
- Comprehensive commit message
- Updated version and changelog
- Repository synchronized

#### 5️⃣ System Validation & Testing
**Agent**: Verifier Agent
**Task**: Validate all systems and run comprehensive tests
**Actions**:
- Test all automation systems
- Verify agent memory isolation
- Check system health and performance
- Validate error detection and fixing
- Run integration tests

**Expected Output**:
- All systems validated and working
- Performance metrics within acceptable ranges
- Error detection and fixing confirmed
- Integration tests passed

### 🔧 Real-life Workflow Implementation:

#### Morning Routine (9:00 AM):
1. **System Health Check**: Verify all services are running
2. **Task Assignment**: Assign tasks to appropriate agents
3. **Resource Check**: Ensure adequate system resources
4. **Priority Review**: Review and prioritize daily tasks

#### Midday Check (12:00 PM):
1. **Progress Review**: Check task completion status
2. **Issue Resolution**: Address any problems or errors
3. **Performance Check**: Monitor system performance
4. **Memory Update**: Update agent memory with progress

#### Evening Wrap-up (6:00 PM):
1. **Final Validation**: Complete all remaining tasks
2. **Report Generation**: Generate comprehensive reports
3. **Git Commit**: Commit all changes and updates
4. **Next Day Prep**: Prepare for next day's tasks

### 🚫 Zero Tolerance Rules (Strict Enforcement):

1. **No Fake Work**: All tasks must produce actual, verifiable results
2. **Folder Discipline**: All files must be in correct directories
3. **Pre-server Checks**: System validation before any deployment
4. **Documentation**: Complete documentation for all processes
5. **Blueprint Compliance**: All work must match system blueprints

### 📊 Success Metrics:

- **Task Completion**: 100% of assigned tasks completed
- **System Health**: All systems running at optimal performance
- **Error Rate**: < 1% error rate with automatic fixing
- **Documentation**: Complete and up-to-date documentation
- **Git Status**: All changes committed and synchronized

### 🎯 Expected Outcomes:

By end of day, the system should have:
- ✅ Ollama service running without authentication issues
- ✅ Complete system optimization documentation
- ✅ 10-minute audio documentation generated
- ✅ All changes committed to git
- ✅ All systems validated and tested
- ✅ Comprehensive reports generated

### 📞 Emergency Procedures:

If any critical issues arise:
1. **Immediate Alert**: Notify system administrator
2. **Rollback**: Revert to last known good state
3. **Investigation**: Identify root cause of issue
4. **Resolution**: Implement fix and validate
5. **Documentation**: Document issue and resolution

### 🔄 Continuous Improvement:

- **Performance Monitoring**: Continuous system performance tracking
- **Error Analysis**: Regular analysis of errors and fixes
- **Optimization**: Continuous system optimization
- **Learning**: Continuous learning and improvement
- **Feedback**: Regular feedback collection and implementation

---

## 🧟‍♂️ Message from Zombie Leader:

> "Agents, today is a critical day for our ZombieCoder system. We need to:
> 1. Fix the Ollama authentication issues that have been plaguing us
> 2. Document our system optimization achievements
> 3. Create professional audio documentation for stakeholders
> 4. Ensure all our work is properly committed and versioned
> 5. Validate that our system is running at peak performance
> 
> Remember: Zero tolerance for fake work, incomplete tasks, or poor documentation.
> We are building a production-ready system that will revolutionize AI development.
> 
> Let's make today count! 🚀
> 
> - কলিজা (Zombie Leader)"

---

**Instructions Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Status**: ✅ READY FOR EXECUTION  
**Priority**: 🔥 CRITICAL  
**Deadline**: End of Business Day
        """
        
        # Save instructions
        with open(self.instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"✅ Daily agent instructions created: {self.instructions_file}")
        return instructions
    
    def create_workflow_json(self):
        """Create workflow JSON for programmatic access"""
        workflow = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "priority_tasks": [
                {
                    "id": "ollama_auth_fix",
                    "agent": "ops",
                    "task": "Fix Ollama authentication and service permission issues",
                    "script": "projects/system_fixes/ollama_auth_fix.py",
                    "status": "pending",
                    "priority": "critical"
                },
                {
                    "id": "system_optimization_doc",
                    "agent": "bestpractices",
                    "task": "Document system optimization and server simplification",
                    "script": "projects/system_optimization/system_architecture_doc.md",
                    "status": "pending",
                    "priority": "high"
                },
                {
                    "id": "tts_documentation",
                    "agent": "conversational",
                    "task": "Create 10-minute audio documentation using Google TTS",
                    "script": "projects/tts_documentation/google_tts_generator.py",
                    "status": "pending",
                    "priority": "high"
                },
                {
                    "id": "git_commit",
                    "agent": "programming",
                    "task": "Commit all daily updates and changes",
                    "script": "git add . && git commit -m 'Daily updates'",
                    "status": "pending",
                    "priority": "medium"
                },
                {
                    "id": "system_validation",
                    "agent": "verifier",
                    "task": "Validate all systems and run comprehensive tests",
                    "script": "projects/agent_instructions/daily_agent_instructions.py",
                    "status": "pending",
                    "priority": "medium"
                }
            ],
            "workflow_schedule": {
                "morning_routine": "9:00 AM",
                "midday_check": "12:00 PM",
                "evening_wrapup": "6:00 PM"
            },
            "zero_tolerance_rules": [
                "No Fake Work",
                "Folder Discipline",
                "Pre-server Checks",
                "Documentation",
                "Blueprint Compliance"
            ],
            "success_metrics": {
                "task_completion": "100%",
                "system_health": "Optimal",
                "error_rate": "< 1%",
                "documentation": "Complete",
                "git_status": "Synchronized"
            }
        }
        
        # Save workflow JSON
        with open(self.workflow_file, 'w') as f:
            json.dump(workflow, f, indent=2)
        
        print(f"✅ Workflow JSON created: {self.workflow_file}")
        return workflow
    
    def generate_agent_report(self):
        """Generate agent report template"""
        report = f"""
# Agent Execution Report - {datetime.now().strftime('%Y-%m-%d')}

## Agent: [AGENT_NAME]
## Task: [TASK_DESCRIPTION]
## Status: [COMPLETED/IN_PROGRESS/FAILED]

### Execution Details:
- **Start Time**: [TIMESTAMP]
- **End Time**: [TIMESTAMP]
- **Duration**: [DURATION]
- **Script Used**: [SCRIPT_PATH]
- **Output Files**: [LIST_OF_FILES]

### Results:
- **Success**: [YES/NO]
- **Issues Found**: [LIST_OF_ISSUES]
- **Fixes Applied**: [LIST_OF_FIXES]
- **Performance Impact**: [POSITIVE/NEGATIVE/NEUTRAL]

### Validation:
- **System Health**: [GOOD/FAIR/POOR]
- **Error Rate**: [PERCENTAGE]
- **Resource Usage**: [CPU/MEMORY/DISK]
- **Network Status**: [STABLE/UNSTABLE]

### Next Steps:
- **Immediate Actions**: [LIST_OF_ACTIONS]
- **Follow-up Tasks**: [LIST_OF_TASKS]
- **Recommendations**: [LIST_OF_RECOMMENDATIONS]

### Blueprint Compliance:
- **Matches Blueprint**: [YES/NO]
- **Deviations**: [LIST_OF_DEVIATIONS]
- **Justification**: [EXPLANATION]

---
**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Agent**: [AGENT_NAME]
**Status**: [FINAL_STATUS]
        """
        
        with open("agent_report_template.md", 'w') as f:
            f.write(report)
        
        print("✅ Agent report template created")
    
    def generate_complete_instructions(self):
        """Generate complete agent instructions"""
        print("🧟 Daily Agent Instructions Generator")
        print("=" * 50)
        
        # Create daily instructions
        print("1. Creating daily instructions...")
        instructions = self.create_daily_instructions()
        
        # Create workflow JSON
        print("2. Creating workflow JSON...")
        workflow = self.create_workflow_json()
        
        # Generate agent report template
        print("3. Generating agent report template...")
        self.generate_agent_report()
        
        print("\n🎉 Daily agent instructions generated successfully!")
        print(f"📁 Instructions file: {self.instructions_file}")
        print(f"📁 Workflow file: {self.workflow_file}")
        print(f"📁 Report template: agent_report_template.md")
        
        return True

def main():
    """Main function"""
    generator = DailyAgentInstructions()
    
    # Generate complete instructions
    success = generator.generate_complete_instructions()
    
    if success:
        print("\n✅ Daily agent instructions ready for execution!")
        print("📋 Agents can now follow the instructions to complete today's tasks.")
    else:
        print("\n❌ Failed to generate daily agent instructions!")

if __name__ == "__main__":
    main()

