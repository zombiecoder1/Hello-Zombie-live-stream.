#!/usr/bin/env python3
# tests/openai_compat_test.py
import requests, time, json, os
from uuid import uuid4

# AGENTS map: name -> base url (gateway or direct agent)
AGENTS = {
    "bengali_nlp": "http://127.0.0.1:8002",
    "code_generation": "http://127.0.0.1:8003",
    "code_review": "http://127.0.0.1:8004",
    "documentation": "http://127.0.0.1:8005",
    "testing": "http://127.0.0.1:8006",
    "deployment": "http://127.0.0.1:8007",
    "voice_processor": "http://127.0.0.1:8014"
}

HEADERS = {"Content-Type": "application/json", "Authorization": "Bearer local-only"}

# Test prompts (Bn + En) per agent (two each)
TEST_PROMPTS = {
    "bengali_nlp": ["বাংলায় একটি ছোট গল্প লেখো", "Write a Bengali proverb with meaning"],
    "code_generation": ["Write a Python function to add two numbers", "পাইথনে ফাইলে লেখা পড়ার কোড লিখো"],
    "code_review": ["Review: def foo(x): return x+1", "Check security issues in this code sample"],
    "documentation": ["Generate API docs for login", "লগইন এন্ডপয়েন্টের ডক লিখো"],
    "testing": ["Write pytest for add(x,y)", "একটি ইউনিট টেস্ট উদাহরণ লিখো"],
    "deployment": ["Write Dockerfile for Flask app", "সিস্টেম ডিপ্লয় স্ক্রিপ্ট তৈরি করো"],
    "voice_processor": ["Convert to speech: Hello world", "বাংলায় টেক্সট-টু-স্পিচ তৈরি করো"]
}

REPORT = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "agents": {}}

def post_chat_completions(base, payload, timeout=10):
    url = base.rstrip('/') + "/v1/chat/completions"
    start = time.time()
    r = requests.post(url, headers=HEADERS, json=payload, timeout=timeout)
    elapsed = (time.time() - start) * 1000.0
    return r, elapsed

def safe_json(r):
    try:
        return r.json()
    except Exception:
        return {"raw": r.text}

def check_agent(name, base):
    agent_report = {"health": None, "session_ok": False, "streaming_ok": False, "mem_ok": False, "questions": [], "logs_tail": []}
    # health
    try:
        h = requests.get(base.rstrip('/') + "/health", timeout=5).json()
        agent_report["health"] = h
    except Exception as e:
        agent_report["health"] = {"error": str(e)}
        return agent_report

    # first request -> expect id in response
    prompts = TEST_PROMPTS.get(name, ["Hello"])
    first = prompts[0]
    payload = {"model":"local-model", "messages":[{"role":"user","content": first}]}
    r, t = post_chat_completions(base, payload)
    jr = safe_json(r)
    q = {"prompt": first, "status_code": r.status_code, "latency_ms": round(t,2), "response": jr}
    agent_report["questions"].append(q)

    # check session id
    session_id = None
    if isinstance(jr, dict):
        session_id = jr.get("id") or jr.get("conversation_id") or jr.get("session_id")
    agent_report["session_ok"] = bool(session_id)

    # follow-up with session header if session id present
    if session_id:
        follow = prompts[1] if len(prompts)>1 else "thanks"
        payload2 = {"model":"local-model","messages":[{"role":"user","content": follow}]}
        headers2 = HEADERS.copy()
        headers2["X-Session-ID"] = session_id
        start = time.time()
        r2 = requests.post(base.rstrip('/') + "/v1/chat/completions", headers=headers2, json=payload2, timeout=10)
        elapsed2 = (time.time()-start)*1000.0
        jr2 = safe_json(r2)
        agent_report["questions"].append({"prompt": follow, "status_code": r2.status_code, "latency_ms": round(elapsed2,2), "response": jr2})
        # simple memory check heuristic: if jr2 contains reference to first prompt or same final, mark mem_ok
        agent_report["mem_ok"] = (str(jr2).find(first[:20])!=-1) or (jr.get("choices") and jr2.get("choices") and jr2["choices"]!=jr["choices"])

    # optional: streaming check (try connecting to /v1/chat/stream)
    try:
        s_url = base.rstrip('/') + "/v1/chat/stream"
        # small non-blocking attempt with short timeout
        rs = requests.post(s_url, headers=HEADERS, json=payload, timeout=3)
        agent_report["streaming_ok"] = rs.status_code in (200, 204)
    except Exception:
        agent_report["streaming_ok"] = False

    # tail logs if file path known (agent must expose logs or we check file path in repo)
    # try reading standard log path
    lf = f"/var/log/zombie/{name}.log"
    if os.path.exists(lf):
        try:
            with open(lf,'r',encoding='utf-8',errors='ignore') as f:
                agent_report["logs_tail"] = f.readlines()[-10:]
        except Exception as e:
            agent_report["logs_tail"] = [f"err reading log: {e}"]
    else:
        agent_report["logs_tail"] = [f"no log at {lf}"]
    return agent_report

if __name__ == "__main__":
    for name, base in AGENTS.items():
        print(f"--- Checking {name} @ {base} ---")
        try:
            r = check_agent(name, base)
        except Exception as e:
            r = {"error": str(e)}
        REPORT["agents"][name] = r
        print(json.dumps(r, indent=2, ensure_ascii=False))
    out = "openai_compat_report.json"
    with open(out,"w",encoding="utf-8") as f:
        json.dump(REPORT,f,indent=2,ensure_ascii=False)
    print("Saved report ->", out)