#!/usr/bin/env python3
"""
IEEC Discord Webhook Notifier
Allows Antigravity IDE and the Captain to post announcements and task alerts
directly to the club Discord server using standard Python library (zero dependencies).
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

# Fix Windows console UTF-8 output
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CONFIG_FILE = Path(__file__).resolve().parent.parent / "config" / "discord_config.json"

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"webhook_url": os.environ.get("DISCORD_WEBHOOK_URL", "")}

def save_config(config):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def send_discord_webhook(payload):
    cfg = load_config()
    webhook_url = cfg.get("webhook_url")
    if not webhook_url:
        print("[!] Discord Webhook URL henüz tanımlanmamış.")
        print("    Lütfen Discord kanal ayarlarından bir Webhook oluşturup şu komutu çalıştırın:")
        print("    python scripts/discord_notifier.py configure <WEBHOOK_URL>")
        sys.exit(1)

    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "Antigravity-IEEC-Notifier"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status in (200, 204):
                print("[✓] Discord bildirimi başarıyla gönderildi!")
    except urllib.error.HTTPError as e:
        print(f"[!] Discord Webhook Hatası ({e.code}): {e.read().decode('utf-8')}")

def post_announcement(title, message, tag_everyone=False):
    payload = {
        "content": "@everyone" if tag_everyone else "",
        "embeds": [{
            "title": f"📢 {title}",
            "description": message,
            "color": 0x00F2FE, # Cyan Neon
            "footer": {"text": "IUS Engineering Events Club • Official Broadcast"}
        }]
    }
    send_discord_webhook(payload)

def post_task_notification(issue_key, title, assignee, url=""):
    payload = {
        "embeds": [{
            "title": f"⚡ Yeni Görev: [{issue_key}] {title}",
            "color": 0x9D4EDD, # Purple Neon
            "fields": [
                {"name": "👤 Sorumlu", "value": assignee, "inline": True},
                {"name": "📌 Platform", "value": "[Linear.app Panosunda Aç](" + url + ")" if url else "Linear", "inline": True}
            ],
            "footer": {"text": "Antigravity IDE • Task Engine"}
        }]
    }
    send_discord_webhook(payload)

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("IEEC Discord Notifier")
        print("Kullanım:")
        print("  python scripts/discord_notifier.py configure <WEBHOOK_URL>")
        print("  python scripts/discord_notifier.py announce --title <BAŞLIK> --msg <MESAJ> [--tag-everyone]")
        print("  python scripts/discord_notifier.py task-alert --key <KOD> --title <BAŞLIK> --assignee <KİŞİ> [--url <LINK>]")
        sys.exit(0)

    cmd = args[0]
    if cmd == "configure" and len(args) >= 2:
        cfg = load_config()
        cfg["webhook_url"] = args[1]
        save_config(cfg)
        print("[✓] Discord Webhook URL kaydedildi!")
    elif cmd == "announce":
        title = "Önemli Kulüp Duyurusu"
        msg = ""
        tag_everyone = "--tag-everyone" in args
        for i, a in enumerate(args):
            if a == "--title" and i + 1 < len(args): title = args[i+1]
            if a == "--msg" and i + 1 < len(args): msg = args[i+1]
        post_announcement(title, msg, tag_everyone)
    elif cmd == "task-alert":
        key = "IUS"
        title = "Görev"
        assignee = "Ekip Üyesi"
        url = ""
        for i, a in enumerate(args):
            if a == "--key" and i + 1 < len(args): key = args[i+1]
            if a == "--title" and i + 1 < len(args): title = args[i+1]
            if a == "--assignee" and i + 1 < len(args): assignee = args[i+1]
            if a == "--url" and i + 1 < len(args): url = args[i+1]
        post_task_notification(key, title, assignee, url)
