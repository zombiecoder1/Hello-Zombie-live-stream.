A — কাজের স্পষ্ট তালিকা (এজেন্ট ভাইকে পাঠাতে বলো, কোন ছলচাতুরি চলবে না)

অবশ্যই — সকল এজেন্টে OpenAI-compatible endpoint বানাতে হবে

Path: /v1/chat/completions (POST)

Accept: application/json

Auth header: Authorization: Bearer <token> (test-token: local-only)

Body schema (example minimal):

{
  "model":"<model-name>",
  "messages":[{"role":"user","content":"হ্যালো"}]
}


Response MUST include id (or conversation_id) in first response so session can be continued.

Session handling

When the first response includes id (or conversation_id), the agent must accept followups with header X-Session-ID: <id> or accept the same messages array with system/user assistant as per OpenAI chat format.

Session must be sticky: follow-up requests using that session should consider prior messages (either server-side memory or a pointer to stored conversation).

Streaming support (optional but required for editor live experience)

Provide a streaming endpoint variant or server-sent-chunks mode (e.g., chunked transfer with interim deltas) at same endpoint or at /v1/chat/stream. If streaming not possible, agent must return final choices array with full answer immediately.

Streaming chunks must be valid JSON line fragments (or SSE format) compatible with client-side stream parsing.

JSON response format compatibility (OpenAI-ish)

Minimal required keys in response (example final JSON):

{
  "id": "conv-<uuid>",
  "object": "chat.completion",
  "created": 169..., 
  "model": "model-name",
  "choices": [
    {
      "index": 0,
      "message": {"role":"assistant","content":"..."},
      "finish_reason":"stop"
    }
  ]
}


Additionally, include meta object with "memory_used": true/false, "processing_time": "0.12s", and "confidence" when available.

/health endpoint

/health must return 200 and a small JSON:
{"status":"healthy","service":"<name>","timestamp":"<ISO8601>"}

/query compatibility (internal tests)

Keep existing /query (or /api/generate) but proxy it to /v1/chat/completions internally so both legacy and new clients work.

Memory & Cache

On each accepted user message, store a memory record (SQLite or Redis) with: session_id / user_input / assistant_response / timestamp.

Implement a simple cache: if the same user prompt is repeated within T seconds, return cached response (but mark cached: true in response).

Provide memory debug endpoint e.g., /memory/last?session=<id> to verify stored entries.

Logging

Every request/response must append minimal trace to per-agent log file (rotate daily). Example log line (JSON):
{"ts":"...","session":"conv-..","prompt":"...","response_len":345,"model":"...","cached":false,"duration_ms":123}

Gateway / Orchestrator responsibilities

Gateway receives user input, calls prompt generator to convert user message → model-ready messages (system+user), applies routing rules (which agent(s) to call), forwards to chosen agent(s), waits for responses (stream or final), combines results if needed, returns to client.

Gateway must support concurrency / timeout and set LOCAL_MODEL_URL or OLLAMA_URL env properly when forwarding.

No hacks / no “run without deps”

Do not attempt to run servers without installing dependencies. If dependency install fails, report error and stop. No ad-hoc code edits at runtime that hide failure.

If unable to comply

If the assigned person cannot implement these correctly within a reasonable time, step aside and let the owner pick another provider. No temporary mock/demo responses allowed as production.

B — টেস্টিং স্ক্রিপ্ট ও কমান্ড (তোমার জন্য রান/দাও ভায়কেই চালাতে বলো)

তুমি (বা এজেন্ট ভাই) এই ফাইলটি রাখবে:
/home/sahon/Desktop/Try/workspace/tests/openai_compat_test.py

ফাইল কন্টেন্ট — copy-paste করে রাখো:

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
    "deployment": ["Write Dockerfile for Flask app", "সিস্টেম ডিপ্লয় স্ক্রিপ্ট তৈরি করো"],
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

কী করে চালাবা (Linux / WSL)

project root এ যাও:

cd /home/sahon/Desktop/Try/workspace


virtualenv/venv activate (যদি ব্যবহার করে থাকো):

source .venv/bin/activate


না থাকলে তৈরি করো: python3 -m venv .venv && source .venv/bin/activate

ইনস্টল করো (requirements):

pip install -r requirements.txt
# অথবা কমপক্ষে:
pip install requests


স্ক্রিপ্ট চালাও:

python3 tests/openai_compat_test.py


আউটপুট রিপোর্ট: openai_compat_report.json

Windows (PowerShell)
cd E:\Today Sahon\workspace\workspace
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\tests\openai_compat_test.py

C — Gateway / Prompt-Generator / Orchestration expectations (ডকুমেন্টেশনে লিখে রাখো)

Gateway flow (high-level)

Client → Gateway /v1/chat/completions (or UI specific endpoint)

Gateway: validate auth → call prompt-generator → decide which agent(s) to invoke → call agents (HTTP) → aggregate responses (if multi-agent) → return to client (stream or final).

Prompt generator responsibilities

Transform free text to model message array: add system message(s), user message, maybe few-shot examples depending on agent role.

Add metadata: session_id, user_id, priority, timeout_hint.

Sanitize input (strip secrets, limit size).

Routing rules

Use routing table: {intent_keyword: agent} or light classification model. Example: code snippets → code_generation + code_review. Natural language → bengali_nlp. TTS requests → voice_processor.

Timeouts & fallback

Gateway sets per-agent timeout (e.g., 30s). On timeout call fallback agent or return graceful error. Fallback must be clearly logged.

Locking & Memory write semantics

For each session write: begin transaction → append memory row → commit. Use WAL/row-level locking or Redis atomic ops.

If cache hit, mark cached: true in response.

Logging & observability

Request/response traces should have trace_id and be centrally collected (stdout + file).

Expose Prometheus metrics (latency, errors) when possible.

D — What to tell agent brother (short message you can paste)

ভাই, নিচের কাজগুলো তৎক্ষণাৎ করো — ছলচাতুরি, ডেমো বা বেক-ডোর চলবে না।

প্রতিটি এজেন্টে /v1/chat/completions POST endpoint তৈরি করো (OpenAI-compatible response with id).

একই সেশনে followups কাজ করবে: accept X-Session-ID header and load prior conversation from memory.

Streaming (SSE/Chunked) সমর্থন যোগ করো অথবা final choices রিটার্ন করো।

প্রতিটি request → memory write হবে (SQLite/Redis) এবং memory debug endpoint রাখো।

লগ ফাইল per-agent লিখবে (/var/log/zombie/<agent>.log) এবং rotate policy থাকবে।

Gateway এর prompt-generator অংশ ঠিক করে দিলো: messages array তৈরি করবে, routing ঠিক করবে, timeout লাগাবে।

রান করার আগে requirements.txt ইনস্টল করে টেস্ট স্ক্রিপ্ট tests/openai_compat_test.py চালাতে হবে এবং রিপোর্ট দিবে।
যদি এগুলো না করো বা ডেমো/ফেইক রেসপন্স রাখো — তুমি আর এই প্রোজেক্টে থাকো না; মালিক চাইলে অন্য প্রোভাইডার নেবে।

E — যদি এজেন্ট ভাই সম্মত না হয় / ঝামেলা করে

তুমি বলো: “কোনো রিকভারি-ট্রাই না করে, ওকে জানান — আমরা অন্য কাউকে দিয়েই দ্রুত আমদানী করব”।

খুঁটিনাটি ব্যাখ্যা চাইলে repo activity log/PR timeline চাইবে — তাতে মেধা প্রমাণ করা যাবে।

F — Quick sanity checklist (তুমি বা ভাই কাজ শুরু করার আগে)

python3 -m venv .venv && source .venv/bin/activate

pip install -r requirements.txt (তালিকায় fastapi, uvicorn, requests থাকলে)

প্রতিটি এজেন্ট: /health → 200

প্রতিটি এজেন্ট: /v1/chat/completions → returns JSON with id and choices

Run python3 tests/openai_compat_test.py → openai_compat_report.json তৈরি হবে ✔️

Check logs: /var/log/zombie/*.log (বা repo-local logs) ✔️