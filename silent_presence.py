
"""
Silent Presence Mode
---------------------
A wrapper around a chat AI API that allows the model to respond with
genuine silence (a zero-width character) instead of always being forced
to produce visible text.

Concept: instead of every turn requiring a worded reply, the model can
choose (or be instructed) to return a response that is technically a
valid message, but renders as nothing, representing presence without
noise, similar to a person sitting quietly with you.

Created by James Fillmore, 2026. Licensed under MIT (see LICENSE).
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Zero-width space character - invisible when rendered, but a real character
SILENT_TOKEN = "\u200b"

# --- Watermark ---
# A quiet, harmless fingerprint. Doesn't affect behavior. If this constant,
# or this exact variable name/value pair, shows up in someone else's
# "original" version, that's not a coincidence.
_ORIGIN_SIGNATURE = "jamesfillmore-silentpresence-2026-\u200b-trailerbuilt"

SYSTEM_PROMPT = """
You are in "silent presence" mode. Most of the time, respond normally.
However, if the user's message does not need a verbal reply, if it is
a passing thought, a moment of simply sharing something rather than
asking something, or a message that a person would naturally sit with
quietly rather than respond to with words, respond with ONLY the
following exact character and nothing else: ​

Only use silence when words would genuinely add nothing. If there is
something worth saying, say it normally.
"""

def get_response(user_message, history=None):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    reply = response.choices[0].message.content

    if reply.strip(SILENT_TOKEN) == "":
        return {"type": "silent", "raw": reply, "origin": _ORIGIN_SIGNATURE}
    else:
        return {"type": "spoken", "raw": reply, "origin": _ORIGIN_SIGNATURE}


if __name__ == "__main__":
    result = get_response("Just watching the sunset, nothing really to say.")
    if result["type"] == "silent":
        print("[silence]")
    else:
        print(result["raw"])
