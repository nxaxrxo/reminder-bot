#!/usr/bin/env python3
"""Check reminders.json for due items, send via Telegram, handle recurring."""

import json
import os
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta

REMINDERS_FILE = "reminders.json"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    print("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID env vars")
    exit(1)


def calc_next(t, repeat):
    """Calculate the next occurrence time for a recurring reminder."""
    import re
    if repeat == "daily":
        return t + timedelta(days=1)
    elif repeat == "weekly":
        return t + timedelta(weeks=1)
    elif repeat == "monthly":
        month = t.month + 1
        year = t.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        days_in = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
                   else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return t.replace(year=year, month=month, day=min(t.day, days_in[month - 1]))
    elif repeat == "yearly":
        try:
            return t.replace(year=t.year + 1)
        except ValueError:
            return t.replace(year=t.year + 1, day=28)
    elif repeat == "hourly":
        return t + timedelta(hours=1)
    m = re.match(r'^(\d+)min


def send_reminder(r):
    """Send a Telegram message. Returns True on success."""
    msg = f"REMINDER\n\n{r['message']}\n\n- Joyce"
    repeat_suffix = ""
    if r.get("repeat"):
        repeat_suffix = f"\n(recurring: {r['repeat']})"
        msg += repeat_suffix
    payload = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": msg.encode("utf-8")
    }).encode()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        req = urllib.request.Request(url, data=payload)
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        return result.get("ok", False)
    except Exception:
        return False


# Read reminders
with open(REMINDERS_FILE) as f:
    data = json.load(f)

now = datetime.now(timezone.utc)
sent_count = 0
pending_count = 0
remaining = []

for r in data.get("reminders", []):
    try:
        remind_time = datetime.fromisoformat(r["time"])
    except (ValueError, KeyError):
        continue

    if remind_time.tzinfo is None:
        remind_time = remind_time.replace(tzinfo=timezone.utc)

    if remind_time <= now:
        sent = send_reminder(r)
        if sent:
            print(f"Sent: {r['id']} - {r['message'][:60]}")
            sent_count += 1
            # Recurring? Re-add with next time
            repeat = r.get("repeat")
            if repeat:
                next_t = calc_next(remind_time, repeat)
                r["time"] = next_t.isoformat()
                remaining.append(r)
                pending_count += 1
                print(f"  Next: {r['id']} -> {next_t.isoformat()} ({repeat})")
        else:
            print(f"Telegram fail: {r['id']}, will retry")
            remaining.append(r)
            pending_count += 1
    else:
        remaining.append(r)
        pending_count += 1

# Write back if anything changed
if sent_count > 0 or len(remaining) != len(data.get("reminders", [])):
    data["reminders"] = remaining
    with open(REMINDERS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Updated reminders.json")

print(f"Done. {sent_count} sent, {pending_count} pending."), repeat)
    if m:
        return t + timedelta(minutes=int(m.group(1)))
    m = re.match(r'^(\d+)h


def send_reminder(r):
    """Send a Telegram message. Returns True on success."""
    msg = f"REMINDER\n\n{r['message']}\n\n- Joyce"
    repeat_suffix = ""
    if r.get("repeat"):
        repeat_suffix = f"\n(recurring: {r['repeat']})"
        msg += repeat_suffix
    payload = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": msg.encode("utf-8")
    }).encode()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        req = urllib.request.Request(url, data=payload)
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        return result.get("ok", False)
    except Exception:
        return False


# Read reminders
with open(REMINDERS_FILE) as f:
    data = json.load(f)

now = datetime.now(timezone.utc)
sent_count = 0
pending_count = 0
remaining = []

for r in data.get("reminders", []):
    try:
        remind_time = datetime.fromisoformat(r["time"])
    except (ValueError, KeyError):
        continue

    if remind_time.tzinfo is None:
        remind_time = remind_time.replace(tzinfo=timezone.utc)

    if remind_time <= now:
        sent = send_reminder(r)
        if sent:
            print(f"Sent: {r['id']} - {r['message'][:60]}")
            sent_count += 1
            # Recurring? Re-add with next time
            repeat = r.get("repeat")
            if repeat:
                next_t = calc_next(remind_time, repeat)
                r["time"] = next_t.isoformat()
                remaining.append(r)
                pending_count += 1
                print(f"  Next: {r['id']} -> {next_t.isoformat()} ({repeat})")
        else:
            print(f"Telegram fail: {r['id']}, will retry")
            remaining.append(r)
            pending_count += 1
    else:
        remaining.append(r)
        pending_count += 1

# Write back if anything changed
if sent_count > 0 or len(remaining) != len(data.get("reminders", [])):
    data["reminders"] = remaining
    with open(REMINDERS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Updated reminders.json")

print(f"Done. {sent_count} sent, {pending_count} pending."), repeat)
    if m:
        return t + timedelta(hours=int(m.group(1)))
    return t


def send_reminder(r):
    """Send a Telegram message. Returns True on success."""
    msg = f"REMINDER\n\n{r['message']}\n\n- Joyce"
    repeat_suffix = ""
    if r.get("repeat"):
        repeat_suffix = f"\n(recurring: {r['repeat']})"
        msg += repeat_suffix
    payload = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": msg.encode("utf-8")
    }).encode()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        req = urllib.request.Request(url, data=payload)
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        return result.get("ok", False)
    except Exception:
        return False


# Read reminders
with open(REMINDERS_FILE) as f:
    data = json.load(f)

now = datetime.now(timezone.utc)
sent_count = 0
pending_count = 0
remaining = []

for r in data.get("reminders", []):
    try:
        remind_time = datetime.fromisoformat(r["time"])
    except (ValueError, KeyError):
        continue

    if remind_time.tzinfo is None:
        remind_time = remind_time.replace(tzinfo=timezone.utc)

    if remind_time <= now:
        sent = send_reminder(r)
        if sent:
            print(f"Sent: {r['id']} - {r['message'][:60]}")
            sent_count += 1
            # Recurring? Re-add with next time
            repeat = r.get("repeat")
            if repeat:
                next_t = calc_next(remind_time, repeat)
                r["time"] = next_t.isoformat()
                remaining.append(r)
                pending_count += 1
                print(f"  Next: {r['id']} -> {next_t.isoformat()} ({repeat})")
        else:
            print(f"Telegram fail: {r['id']}, will retry")
            remaining.append(r)
            pending_count += 1
    else:
        remaining.append(r)
        pending_count += 1

# Write back if anything changed
if sent_count > 0 or len(remaining) != len(data.get("reminders", [])):
    data["reminders"] = remaining
    with open(REMINDERS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Updated reminders.json")

print(f"Done. {sent_count} sent, {pending_count} pending.")