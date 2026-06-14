#!/usr/bin/env python3
"""Check reminders.json for due items, send via Telegram, clean up sent ones."""

import json
import os
import urllib.request
import urllib.parse
from datetime import datetime, timezone

REMINDERS_FILE = "reminders.json"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    print("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID env vars")
    exit(1)

# Read reminders
with open(REMINDERS_FILE) as f:
    data = json.load(f)

now = datetime.now(timezone.utc)
sent_count = 0
remaining = []

for r in data.get("reminders", []):
    try:
        remind_time = datetime.fromisoformat(r["time"])
    except (ValueError, KeyError):
        continue

    if remind_time <= now:
        # Send Telegram
        msg = f"REMINDER\n\n{r['message']}\n\n- Joyce"
        payload = urllib.parse.urlencode({
            "chat_id": CHAT_ID,
            "text": msg.encode("utf-8")
        }).encode()
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        try:
            req = urllib.request.Request(url, data=payload)
            resp = urllib.request.urlopen(req)
            result = json.loads(resp.read())
            if result.get("ok"):
                print(f"Sent: {r['id']} - {r['message'][:60]}")
                sent_count += 1
            else:
                print(f"Telegram API error for {r['id']}: {result.get('description', 'unknown')}")
                remaining.append(r)  # keep it, will retry next cycle
        except Exception as e:
            print(f"Failed to send {r['id']}: {e}")
            remaining.append(r)  # keep for retry
    else:
        remaining.append(r)

# Write back (only if something changed)
if sent_count > 0:
    data["reminders"] = remaining
    with open(REMINDERS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Updated reminders.json ({sent_count} sent)")

print(f"Done. {sent_count} sent, {len(remaining)} pending.")
