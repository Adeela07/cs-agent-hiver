import os
import json
import pickle
import re
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-3.6-flash")

with open("eval/intent_spec.md", "r", encoding="utf-8") as f:
    INTENT_SPEC = f.read()

with open("data/bm25_index.pkl", "rb") as f:
    idx = pickle.load(f)
bm25 = idx["bm25"]
corpus_texts = idx["texts"]
corpus_resolutions = idx["resolutions"]

SAFE_INTENTS = {"how_to"}

def retrieve(query, k=3):
    scores = bm25.get_scores(query.lower().split())
    top_idx = scores.argsort()[-k:][::-1]
    return [(corpus_texts[i], corpus_resolutions[i]) for i in top_idx]

def classify(message):
    prompt = f"""Given these intents:
{INTENT_SPEC}

Classify this customer message. Respond ONLY with JSON, no other text, no markdown formatting: {{"intent": "...", "confidence": 0.0}}

Message: "{message}" """
    resp = model.generate_content(prompt)
    raw = resp.text
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    return json.loads(match.group(0))

def draft_reply(message, intent, examples):
    ex_text = "\n".join([f'- Similar case: "{c}" -> Brand pattern: {r}' for c, r in examples])
    prompt = f"""You are a support agent for AppleSupport. Intent: {intent}.
Historical precedent for similar issues:
{ex_text}

Draft a reply to: "{message}"
Only follow patterns actually shown above. If nothing above applies, say you are unsure rather than inventing policy."""
    resp = model.generate_content(prompt)
    return resp.text

def route(intent, confidence, draft):
    if intent not in SAFE_INTENTS:
        return "escalate", "intent not on pre-approved auto-handle list"
    if confidence < 0.75:
        return "escalate", "low classifier confidence"
    risky_words = ["refund", "compensat", "guarantee", "promise"]
    if any(w in draft.lower() for w in risky_words):
        return "escalate", "draft contains commitment language requiring human approval"
    return "auto", "high-confidence safe intent, no risk language detected"

def handle_message(message):
    result = classify(message)
    intent = result["intent"]
    confidence = result["confidence"]
    examples = retrieve(message)
    draft = draft_reply(message, intent, examples)
    decision, reason = route(intent, confidence, draft)
    return {
        "message": message,
        "intent": intent,
        "confidence": confidence,
        "draft": draft,
        "decision": decision,
        "reason": reason,
    }

if __name__ == "__main__":
    test_msg = "My iPhone won't turn on after the update"
    result = handle_message(test_msg)
    print(json.dumps(result, indent=2))