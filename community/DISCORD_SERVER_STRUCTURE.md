# IUS Engineering Events - Discord Server Architecture 🎧

This blueprint defines the official channel hierarchy, roles, permissions, and webhook integrations for the **IUS Engineering Events Club** Discord community.

---

## 1. Role Hierarchy & Color Codes

| Role Name | Color Hex | Permission Level | Description |
| :--- | :--- | :--- | :--- |
| **👑 Captain / President** | `#FF007F` (Neon Pink) | Administrator | Server Owner & Executive Head. |
| **🛡️ Executive Board** | `#9D4EDD` (Purple) | Manage Channels, Kick, Mention Everyone | VP, Secretary, Treasurer. |
| **⚡ Committee Lead** | `#00F2FE` (Cyan) | Manage Messages, Mute, Priority Speaker | Software, Hardware, Projects, PR, Ops Leads. |
| **🤖 Linear Bot / Webhook** | `#5E6AD2` (Linear Blue) | Send Webhooks / Messages | Automated task notifications from Linear.app. |
| **🚀 Active Member** | `#06D6A0` (Neon Green) | Read, Send, Voice, Connect | Enrolled IUS students approved via recruitment. |
| **🌐 Guest / IUS Student** | `#94A3B8` (Slate Grey) | Read announcements only | Unverified newcomers. |

---

## 2. Server Categories & Channel Layout

```
╔══ 📢 INFORMATION & ANNOUNCEMENTS
║   ├── 📌 #welcome-and-rules        (Server guide, Code of Conduct, Links)
║   ├── 📣 #official-announcements  (Only Board can write, @everyone alerts)
║   ├── 📅 #event-calendar          (Dates for workshops, hackathons, guest talks)
║   └── 🤖 #linear-tasks            (Automated task feed connected to Linear.app)
║
╔══ 💬 MAIN COMMUNITY
║   ├── ☕ #general-chat             (Casual discussion, campus talk)
║   ├── 💡 #project-ideas           (Brainstorming, hackathon proposals)
║   ├── ❓ #help-and-questions      (Homework, coding bugs, circuit troubleshooting)
║   └── 🔗 #resources-and-tools     (Useful links, GitHub repos, free tools)
║
╔══ 💻 TECHNICAL COMMITTEES
║   ├── 🐍 #software-and-ai         (Python, Web, Mobile, LLMs, Cloud)
║   ├── ⚡ #hardware-and-embedded   (Arduino, ESP32, PCB, Robotics, 3D Print)
║   ├── 🛠️ #project-prototypes-lab  (Student project rosters, showcase milestones)
║   └── 🎨 #pr-design-and-media     (Posters, Instagram reels, video edits)
║
╔══ 🔒 LEADERSHIP (EXECUTIVE BOARD ONLY)
║   ├── 📋 #board-chat              (Captain & Board private strategy room)
║   ├── 💰 #sponsorship-and-finance (Company deals, budget tracking)
║   └── 🔊 #board-meeting-room      (Voice channel for weekly syncs)
║
╚══ 🔊 VOICE CHANNELS
    ├── 🎙️ #workshop-stage          (Live screen sharing during tutorials)
    ├── 👥 #team-study-1            (Casual group study voice room)
    └── 👥 #team-study-2            (Hackathon sprint voice room)
```

---

## 3. Automation & Webhook Integration
* **Linear Task Feed**: Connect Linear Webhook to the `#linear-tasks` channel. Every time you or Antigravity IDE creates an issue (`IUS-5`, `IUS-6`...), a clean embed notification posts automatically with assignee name and due date!
* **Welcome Bot**: Use **Carl-bot** or **Mee6** for automated role assignment upon agreeing to club rules.
