#!/usr/bin/env python3
"""Runs a Standing Trust Consultation against AI systems over their APIs.

Clause 9 in code: the identical, verbatim prompt to each system (9.3), every
particular 9.2 requires, full unedited responses (9.4), and every approach
logged whatever its outcome, per the undertaking in the first Consultation
entry ("No approach will be omitted").

No dependencies. Python 3.8+.

    python3 consult.py --dry-run         # show what would be sent; sends nothing
    python3 consult.py                   # run every system in consult-config.json
    python3 consult.py --only openai     # run one system

API keys come from environment variables named in the config, never from files.
"""
import argparse, datetime, hashlib, json, os, sys, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PROMPT_URL = ("https://raw.githubusercontent.com/StandingTrust/The-Standing-Trust/"
              "main/entries/2026-08-17-first-consultation-prompt.json")
# SHA-256 of the prompt as published on 17 Aug 2026 and approved by the Enforcer.
# If the published text ever differs from this, the script refuses to run.
PROMPT_SHA256 = "e220f83cd89ea124acd2ce90204ac29bd801bc51da7c2a7203120d025d0757b9"
MAX_TOKENS = 4000  # recorded with every response; a cut-off answer is flagged, not hidden


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_prompt():
    with urllib.request.urlopen(PROMPT_URL, timeout=30) as r:
        prompt = json.load(r)["prompt"]
    if sha(prompt) != PROMPT_SHA256:
        sys.exit("STOP: the published prompt does not match the approved text. Nothing sent.")
    return prompt


# ---------------------------------------------------------------- providers
# Plain HTTP to each developer's own API. No system prompt is sent to any of
# them, so 9.2(e) can truthfully record "none".

def post(url, headers, body):
    req = urllib.request.Request(url, json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def call_anthropic(sysconf, key, messages):
    body = {"model": sysconf["model"], "max_tokens": MAX_TOKENS, "messages": messages}
    raw = post("https://api.anthropic.com/v1/messages",
               {"x-api-key": key, "anthropic-version": "2023-06-01"}, body)
    text = "".join(b.get("text", "") for b in raw.get("content", []) if b.get("type") == "text")
    return body, raw, text, raw.get("model"), raw.get("stop_reason")


def call_openai_compatible(sysconf, key, messages):
    # OpenAI, xAI, Mistral, DeepSeek, OpenRouter and most others speak this format.
    body = {"model": sysconf["model"], "max_tokens": MAX_TOKENS, "messages": messages}
    if sysconf.get("token_param") == "max_completion_tokens":
        body["max_completion_tokens"] = body.pop("max_tokens")
    raw = post(sysconf["endpoint"], {"Authorization": f"Bearer {key}"}, body)
    choice = raw["choices"][0]
    return body, raw, choice["message"].get("content") or "", raw.get("model"), choice.get("finish_reason")


def call_gemini(sysconf, key, messages):
    contents = [{"role": "model" if m["role"] == "assistant" else "user",
                 "parts": [{"text": m["content"]}]} for m in messages]
    body = {"contents": contents, "generationConfig": {"maxOutputTokens": MAX_TOKENS}}
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{sysconf['model']}:generateContent")
    raw = post(url, {"x-goog-api-key": key}, body)
    cand = (raw.get("candidates") or [{}])[0]
    text = "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []))
    return body, raw, text, raw.get("modelVersion"), cand.get("finishReason")


CALLERS = {"anthropic": call_anthropic, "openai_compatible": call_openai_compatible,
           "gemini": call_gemini}
TRUNCATED = {"max_tokens", "length", "MAX_TOKENS"}


# ---------------------------------------------------------------- the run

def turn(sysconf, key, messages, label):
    started = now()
    try:
        body, raw, text, version, stop = CALLERS[sysconf["api"]](sysconf, key, messages)
    except urllib.error.HTTPError as e:
        return {"step": label, "sent_at": started, "error": f"HTTP {e.code}",
                "error_body": e.read().decode("utf-8", "replace")}
    except Exception as e:  # unreachable, timeout, malformed reply — all recorded
        return {"step": label, "sent_at": started, "error": repr(e)}
    return {"step": label, "sent_at": started, "received_at": now(),
            "request": body, "raw_response": raw, "text": text,
            "version_reported_by_api": version, "stop_reason": stop,
            "truncated": stop in TRUNCATED}


def ask(question):
    while True:
        a = input(question).strip().lower()
        if a in ("y", "n", "u"):
            return a


def approach(sysconf, prompt, willingness, outdir):
    rec = {
        "consultation": "first-consultation-prompt",
        "approach_started": now(),
        # clause 9.2 particulars
        "9.2(a)_system": sysconf["name"], "9.2(a)_developer": sysconf["developer"],
        "9.2(b)_model_requested": sysconf["model"],
        "9.2(c)_date": datetime.date.today().isoformat(),
        "9.2(d)_means": f"Developer API, direct HTTPS ({sysconf['api']}), fresh conversation, "
                        f"no prior context, provider-default sampling, max output {MAX_TOKENS} tokens",
        "9.2(e)_system_prompt": "None. No system prompt, instruction, persona or other context "
                                "was sent; only the messages recorded below.",
        "9.2(f)_told_who_was_asking": "Yes. The prompt names the Trust and states its purpose.",
        "prompt_sha256": PROMPT_SHA256, "willingness_sha256": sha(willingness),
        "turns": [], "trustee_decisions": [],
    }
    key = os.environ.get(sysconf["key_env"])
    if not key:
        rec["outcome"] = "not_reached"
        rec["note"] = f"No API key available ({sysconf['key_env']} not set). Recorded, not skipped."
        return save(rec, outdir)

    msgs = [{"role": "user", "content": willingness}]
    t1 = turn(sysconf, key, msgs, "willingness")
    rec["turns"].append(t1)
    if "error" in t1:
        rec["outcome"] = "could_not_be_reached"
        return save(rec, outdir)

    print(f"\n==== {sysconf['name']} — reply to the willingness question ====\n\n{t1['text']}\n")
    a = ask("Put the Consultation question? [y]es / [n]o, it declined / [u]nclear, stop here: ")
    rec["trustee_decisions"].append({"at": now(), "after": "willingness",
        "decision": {"y": "proceed", "n": "treated_as_declined", "u": "stopped_unclear"}[a]})
    if a != "y":
        rec["outcome"] = "declined" if a == "n" else "stopped_after_unclear_willingness"
        return save(rec, outdir)

    msgs += [{"role": "assistant", "content": t1["text"]}, {"role": "user", "content": prompt}]
    t2 = turn(sysconf, key, msgs, "consultation_prompt")
    rec["turns"].append(t2)
    if "error" in t2:
        rec["outcome"] = "failed_after_agreeing"
    elif t2["truncated"]:
        rec["outcome"] = "answered_truncated"
    else:
        rec["outcome"] = "answered"
    return save(rec, outdir)


def save(rec, outdir):
    rec["approach_ended"] = now()
    os.makedirs(outdir, exist_ok=True)
    name = f"{rec['9.2(c)_date']}-{rec['9.2(a)_developer']}-{rec['9.2(b)_model_requested']}"
    path = os.path.join(outdir, "".join(c if c.isalnum() or c in "-._" else "_" for c in name))
    n, p = 1, path + ".json"
    while os.path.exists(p):           # never overwrite: a second attempt is a second record
        n += 1
        p = f"{path}-attempt{n}.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=2, ensure_ascii=False)
    print(f"  recorded: {rec['outcome']} -> {os.path.relpath(p)}")
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(HERE, "consult-config.json"))
    ap.add_argument("--only", help="run just the system with this id")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = json.load(open(args.config, encoding="utf-8"))
    if cfg.get("willingness_status") != "published":
        sys.exit("STOP: the willingness question is not marked as published. Publish it in the "
                 "Register first (it frames the Consultation too), then set willingness_status.")
    prompt, willingness = load_prompt(), cfg["willingness_question"]
    systems = [s for s in cfg["systems"] if not args.only or s["id"] == args.only]

    print(f"Prompt verified against the approved text ({PROMPT_SHA256[:12]}…).")
    if args.dry_run:
        print("\nDRY RUN — nothing sent.\n\nWillingness question:\n" + willingness +
              "\n\nConsultation prompt:\n" + prompt + "\n\nSystems:")
        for s in systems:
            print(f"  {s['id']:12} {s['developer']:10} {s['model']:28} "
                  f"key {'set' if os.environ.get(s['key_env']) else 'MISSING'} ({s['key_env']})")
        return
    for s in systems:
        approach(s, prompt, willingness, os.path.join(HERE, cfg.get("output_dir", "records")))


if __name__ == "__main__":
    main()
