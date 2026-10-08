#!/usr/bin/env python3
"""
IEEC Deep Space Observatory Synchronizer
Fetches live Linear tasks and Google Form members, builds a comprehensive
ecosystem knowledge graph, and synchronizes graphify-out/graph.json and graph.html.
"""

import os
import sys
import json
import csv
import re
import urllib.request
from pathlib import Path
from datetime import datetime

# Fix Windows console UTF-8 output
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "scripts"))

from linear_ops import get_issues, graphql
from fetch_google_sheet import fetch_responses, CSV_FILE

GRAPH_DIR = WORKSPACE_ROOT / "graphify-out"
GRAPH_JSON_FILE = GRAPH_DIR / "graph.json"
GRAPH_HTML_FILE = GRAPH_DIR / "graph.html"

# Management Board Static Canonical Metadata
BOARD_MEMBERS = {
    "hasan_kaan": {
        "id": "board_hasan_kaan",
        "name": "Hasan Kaan",
        "role": "👑 Asıl Başkan & Kurucu Lider (Executive President)",
        "student_id": "250302195",
        "dept": "FENS / CSE (1. Sınıf)",
        "email": "ufukkarabulut35@gmail.com",
        "duties": "Kulübün ASIL BAŞKANI, kurucusu ve nihai karar mercii. Kulübün tüm vizyonunu, teknik ve idari yapılanmasını, Linear sprintlerini, yapay zeka atölyelerini, bütçe onaylarını ve DevHack 2027'yi yönetir.",
        "tools": ["Linear.app Task Hub", "Antigravity IDE & Python Automation", "WhatsApp Community Hub", "AI/LLM Workshop Stacks", "Tüm Stratejik Kararlar"],
        "collaborates": ["Mahmut İhsan (Asıl Bşk. Yrd.)", "Kaan Mete (Resmi Temsilci)", "Bekir Enes (Sayman)", "Komiteler & Takımlar"],
        "isGodNode": True,
        "aliases": ["hasan kaan", "hasankaan", "hasan"]
    },
    "mahmut_ihsan": {
        "id": "board_mahmut_ihsan",
        "name": "Mahmut İhsan Avcı",
        "role": "🚀 Asıl Başkan Yardımcısı & İdari Koordinatör (Vice President)",
        "student_id": "250302233",
        "dept": "FENS (1. Sınıf)",
        "phone": "540 002 0571",
        "email": "mahmut.ihsanavcii@gmail.com",
        "duties": "Kulübün ASIL BAŞKAN YARDIMCISI ve operasyonel sağ kolu. Üye alımları, bürokrasi, toplantı tutanakları ve idari/lojistik operasyonların yöneticisi. Hasan Kaan ile birlikte kulübü fiilen yönetir.",
        "tools": ["Google Sheets Live Ingestion", "WhatsApp Community Hub", "Resmi Toplantı Tutanakları", "SCC 10-Üye Resmi Listesi"],
        "collaborates": ["Hasan Kaan (Asıl Başkan)", "Kaan Mete (Resmi Temsilci)", "Bekir Enes (Sayman)", "Kurucu Üyeler"],
        "isGodNode": True,
        "aliases": ["mahmut ihsan avcı", "mahmut ihsan", "mahmut.ihsanavcii"]
    },
    "kaan_mete": {
        "id": "board_kaan_mete",
        "name": "Kaan Mete Şenyıldız",
        "role": "🏛️ Resmi / Göstermelik Başkan (SCC 2. Sınıf Temsilcisi)",
        "student_id": "250302201",
        "dept": "FENS / CSE (2. Sınıf)",
        "phone": "+90 553 113 11 98",
        "duties": "SCC mevzuatındaki 'Kulüp başkanı en az 2. sınıf olmalıdır' kuralını karşılamak üzere resmi evraklardaki imza mercii ve üniversite nezdindeki biçimsel temsilci. Fiili kulüp yönetimi ve kararlar Hasan Kaan ve Mahmut İhsan tarafından yürütülür.",
        "tools": ["Resmi Dilekçe İmzaları", "SCC Temsilcilik Evrakları", "Town Hall Katılımı"],
        "collaborates": ["Hasan Kaan (Asıl Başkan)", "Mahmut İhsan (Asıl Bşk. Yrd.)", "FENS Academic Advisor"],
        "isGodNode": True,
        "aliases": ["kaan mete", "kaan mete şenyıldız", "kaan"]
    },
    "bekir_enes": {
        "id": "board_bekir_enes",
        "name": "Bekir Enes Çokbekler",
        "role": "💰 Sayman & Finans Lideri (Treasurer & Finance)",
        "student_id": "250302229",
        "dept": "Makine Mühendisliği (1. Sınıf)",
        "phone": "05523822006",
        "email": "46bekir70@gmail.com",
        "duties": "Bütçe ve sponsorluk yöneticisi. SCC 1.300 KM taslak bütçe ve 5.000 KM kurumsal sponsorluk paketini hazırlar. Saraybosna teknoloji ekosistemi şirketleriyle sponsorluk görüşmeleri yürütür. Hasan Kaan ve Mahmut İhsan'a rapor verir.",
        "tools": ["Corporate Sponsorship Package", "1.300 KM Taslak Bütçe Tablosu", "Promotion Day Afiş & Roll-up Materyalleri"],
        "collaborates": ["Hasan Kaan (Asıl Başkan)", "Mahmut İhsan (Asıl Bşk. Yrd.)", "Saraybosna Şirketleri", "PR Lead"],
        "isGodNode": True,
        "aliases": ["bekir enes çokbekler", "bekir enes", "46bekir70"]
    },
    "pr_lead": {
        "id": "board_pr_lead",
        "name": "PR & Communications Lead [AÇIK POZİSYON]",
        "role": "PR & Media Lead (Basın & Tanıtım)",
        "student_id": "Bekleniyor",
        "dept": "Aday Bekleniyor",
        "duties": "5. Yönetim Kurulu pozisyonu (Açık). Sosyal medya hesapları (Instagram, LinkedIn), afiş/broşür görsel tasarımları, etkinlik tanıtımı ve kampüs içi marka görünürlüğü.",
        "tools": ["Canva / Figma", "Instagram & LinkedIn", "Promosyon & Etkinlik Afişleri"],
        "collaborates": ["Bekir Enes (Promotion Day)", "Hasan Kaan (Tech-Talk Duyuruları)", "Mahmut İhsan (İdari Duyurular)"],
        "isGodNode": False,
        "aliases": ["pr lead", "pr", "açık pozisyon"]
    }
}

# SECTOR COORDINATES MAP (Clean Spatial Architecture)
SECTOR_POSITIONS = {
    # 👑 CENTER: LEADERSHIP NEXUS
    "board_hasan_kaan": {"x": 0, "y": 0},
    "board_mahmut_ihsan": {"x": -280, "y": 0},
    "board_kaan_mete": {"x": 280, "y": 0},
    "board_bekir_enes": {"x": -140, "y": 180},
    "board_pr_lead": {"x": 140, "y": 180},
    "platform_linear": {"x": 0, "y": -220},
    "tool_ide": {"x": -260, "y": -220},

    # 🏛️ LEFT FLANK: GOVERNANCE & ACADEMICS
    "advisor": {"x": -740, "y": -200},
    "sks": {"x": -740, "y": 50},

    # 🛠️ LEFT-MID: TECHNICAL COMMITTEES
    "comm_software": {"x": -510, "y": -90},
    "comm_multi": {"x": -510, "y": 100},
    "comm_ops": {"x": -510, "y": 270},

    # 📄 BOTTOM SHELF: ŞABLONLAR & RESMİ BELGELER (TEMPLATES ARCHIVE)
    "doc_advisor_letter": {"x": -680, "y": 520},
    "doc_constitution": {"x": -410, "y": 550},
    "doc_founding": {"x": -140, "y": 570},
    "doc_annual_plan": {"x": 140, "y": 570},
    "doc_budget": {"x": 410, "y": 550},
    "doc_sponsorship": {"x": 680, "y": 520},

    # 👥 RIGHT FLANK: COMMUNITY & DATA INGESTION
    "sheet_responses": {"x": 520, "y": -60},
    "fetch_tool": {"x": 750, "y": -60},
    "comm_whatsapp": {"x": 520, "y": 110},

    # 🚀 TOP-RIGHT: EVENTS & INDUSTRY ECOSYSTEM
    "event_launch": {"x": 750, "y": -250},
    "event_hackathon": {"x": 980, "y": -290},
    "ext_industry": {"x": 980, "y": -120},
}

def resolve_assignee_id(assignee_name):
    if not assignee_name:
        return "board_hasan_kaan" # default fallback
    name_lower = assignee_name.lower().strip()
    for key, data in BOARD_MEMBERS.items():
        for alias in data["aliases"]:
            if alias in name_lower:
                return data["id"]
    return "board_hasan_kaan"

def build_observatory_graph():
    print("[*] 1/3 Canlı Linear Görevleri Çekiliyor...")
    # Fetch issues with URLs
    issues_query = """
    query {
      issues {
        nodes {
          id
          identifier
          title
          description
          priority
          dueDate
          url
          state { id name }
          assignee { id name email }
        }
      }
    }
    """
    raw_issues = graphql(issues_query).get("issues", {}).get("nodes", [])
    print(f"    [✓] {len(raw_issues)} Linear görevi başarıyla alındı.")

    print("[*] 2/3 Canlı Google Sheets Yanıtları Çekiliyor...")
    sheet_rows = fetch_responses()
    print(f"    [✓] {len(sheet_rows)} form yanıtı işleniyor.")

    # Filter normal members (non-board) from sheet rows upfront
    normal_member_rows = []
    for r in sheet_rows:
        if len(r) < 5:
            continue
        m_name = r[1].strip()
        m_id = r[4].strip()
        is_board = False
        for b in BOARD_MEMBERS.values():
            if b["student_id"] == m_id or any(al in m_name.lower() for al in b["aliases"]):
                is_board = True
                break
        if not is_board:
            normal_member_rows.append(r)

    nodes = []
    edges = []

    # Helper function to append node with coordinates
    def add_node(node_dict):
        nid = node_dict["id"]
        if nid in SECTOR_POSITIONS:
            node_dict["x"] = SECTOR_POSITIONS[nid]["x"]
            node_dict["y"] = SECTOR_POSITIONS[nid]["y"]
        nodes.append(node_dict)

    # 1. CORE PLATFORM & INFRASTRUCTURE NODES
    add_node({
        "id": "platform_linear",
        "label": "Linear.app Task Hub",
        "cluster": "Infrastructure",
        "isGodNode": True,
        "type": "Software",
        "file": "scripts/linear_manager.py",
        "url": "https://linear.app/ius-engineering-events",
        "details": f"Merkezi görev ve sprint motoru. Antigravity IDE ile çift yönlü GraphQL API senkronizasyonu ({len(raw_issues)} aktif görev kayıtlı)."
    })

    add_node({
        "id": "tool_ide",
        "label": "Antigravity IDE & Automation",
        "cluster": "Infrastructure",
        "isGodNode": False,
        "type": "Engine",
        "file": "scripts/sync_observatory.py",
        "details": "Google DeepMind Antigravity IDE ortamı. Canlı veri çekiciler, Python otomasyonları ve Observatory harita jeneratörü."
    })

    add_node({
        "id": "sheet_responses",
        "label": f"Google Sheets ({len(sheet_rows)} Kayıt / {len(normal_member_rows)} Normal Üye)",
        "cluster": "Data",
        "isGodNode": False,
        "type": "Dataset",
        "file": "data/form_responses.csv",
        "url": "https://docs.google.com/spreadsheets/d/1pLeiQpBNSfDFPGa5IqLbSGoz0Z2Lm3Olu-mq3XZhzbQ/edit?usp=sharing",
        "details": f"Canlı Google Form yanıt tablosu. Mahmut İhsan ve scriptler tarafından izlenir. {len(normal_member_rows)} onaylı normal üye kayıtlı."
    })

    add_node({
        "id": "fetch_tool",
        "label": "Google Sheet Live Fetcher",
        "cluster": "Infrastructure",
        "isGodNode": False,
        "type": "Script",
        "file": "scripts/fetch_google_sheet.py",
        "details": "CSV formatında canlı tabloyu IDE içerisine indiren otomatik köprü."
    })

    edges.append({"source": "fetch_tool", "target": "sheet_responses", "relation": "SYNCS_CSV_FROM"})

    # 2. GOVERNANCE & ACADEMIC NODES
    add_node({
        "id": "advisor",
        "label": "FENS Academic Advisor",
        "cluster": "Governance",
        "isGodNode": True,
        "type": "Academic",
        "file": "templates/ACADEMIC_ADVISOR_INVITATION.md",
        "details": "FENS Fakültesinden resmi kulüp danışmanı profesör. Rektörlük ve dekanlık ile kurumsal bağ sağlar."
    })

    add_node({
        "id": "sks",
        "label": "IUS Student Affairs (SKS / SCC)",
        "cluster": "Governance",
        "isGodNode": False,
        "type": "University",
        "file": "templates/IUS_SKS_APPLICATION_PETITION.md",
        "details": "Kulüp resmiyetini onaylayan, amfi ve stant izinlerini veren IUS Öğrenci Kulüpleri Komisyonu."
    })

    # 3. COMMITTEES
    add_node({
        "id": "comm_software",
        "label": "Software & AI Committee",
        "cluster": "Committees",
        "isGodNode": True,
        "type": "Committee",
        "file": "organization/ORGANIZATIONAL_STRUCTURE.md",
        "details": "Yapay zeka atölyeleri, Cursor/Copilot pratikleri, modern web mimarisi ve kodlama kampları yürütücüsü."
    })

    add_node({
        "id": "comm_multi",
        "label": "Multidisciplinary Eng Committee",
        "cluster": "Committees",
        "isGodNode": False,
        "type": "Committee",
        "file": "organization/ORGANIZATIONAL_STRUCTURE.md",
        "details": "Bilgisayar, Elektrik-Elektronik, Makine ve Endüstri mühendisliğini donanım/IoT projelerinde birleştirir."
    })

    add_node({
        "id": "comm_ops",
        "label": "Event Ops & Logistics",
        "cluster": "Committees",
        "isGodNode": False,
        "type": "Committee",
        "file": "organization/ROLE_DESCRIPTIONS.md",
        "details": "Amfi rezervasyonları, mikrofon/projeksiyon ses sistemleri, akış kontrolü ve ikram lojistiği."
    })

    # 4. COMMUNITY
    add_node({
        "id": "comm_whatsapp",
        "label": "WhatsApp Official Community",
        "cluster": "Community",
        "isGodNode": False,
        "type": "Platform",
        "file": "community/WHATSAPP_TELEGRAM_COMMUNITY_GUIDE.md",
        "url": "https://chat.whatsapp.com/LKMpyfm7K5R3F0rXezcXXN",
        "details": "Üye koordinasyonu ve hızlı anlık duyurular için resmi WhatsApp grubu."
    })

    # 5. DOCUMENTS & TEMPLATES (DEDICATED SHELF: RESMİ ŞABLONLAR)
    add_node({
        "id": "doc_constitution",
        "label": "📄 IEEC Kulüp Tüzüğü",
        "cluster": "Documents",
        "isGodNode": True,
        "type": "Doc",
        "file": "constitution/CONSTITUTION.md",
        "details": "Resmi kulüp anayasası ve tüzüğü (İngilizce). 9 Bölüm, seçim kuralları ve komite ilkeleri."
    })

    add_node({
        "id": "doc_founding",
        "label": f"📄 SCC 10 Kurucu Üye Listesi ({len(normal_member_rows)}/10)",
        "cluster": "Documents",
        "isGodNode": True,
        "type": "Doc",
        "file": "templates/SCC_FOUNDING_10_MEMBERS.md",
        "details": f"Resmi kuruluş evrağı: 4 Yönetim Kurulu Onaylı + 1 PR Lead Açık | {len(normal_member_rows)} Normal Üye Onaylı + {max(0, 10 - len(normal_member_rows))} Üye Bekleniyor."
    })

    add_node({
        "id": "doc_annual_plan",
        "label": "📄 SCC Yıllık Faaliyet Planı",
        "cluster": "Documents",
        "isGodNode": False,
        "type": "Doc",
        "file": "templates/SCC_ANNUAL_ACTIVITY_PLAN.md",
        "details": "4 Temel Sütun: Haftalık AI Atölyeleri, Kampüs Konuşmacıları, Online Tech-Talks ve DevHack 2027."
    })

    add_node({
        "id": "doc_budget",
        "label": "📄 SCC Taslak Bütçe (1.300 KM)",
        "cluster": "Documents",
        "isGodNode": False,
        "type": "Doc",
        "file": "templates/SCC_DRAFT_BUDGET.md",
        "details": "Okuldan para talep etmeyen, yerel şirket sponsorluğu ile dengelenmiş güvenli bütçe tablosu."
    })

    add_node({
        "id": "doc_sponsorship",
        "label": "📄 Kurumsal Sponsorluk Paketi",
        "cluster": "Documents",
        "isGodNode": False,
        "type": "Doc",
        "file": "sponsorship/SPONSORSHIP_PACKAGE.md",
        "details": "Saraybosna yazılım firmalarına sunulan sponsorluk paketi (Platin, Altın, Gümüş, Bronz)."
    })

    add_node({
        "id": "doc_advisor_letter",
        "label": "📄 Danışman Davet Mektubu",
        "cluster": "Documents",
        "isGodNode": False,
        "type": "Doc",
        "file": "templates/ACADEMIC_ADVISOR_INVITATION.md",
        "details": "FENS Profesörlerine takdim edilen resmi kulüp vizyonu ve danışmanlık davet mektubu."
    })

    # 6. FLAGSHIP EVENTS & EXTERNAL
    add_node({
        "id": "event_launch",
        "label": "Welcome Meeting & Launch",
        "cluster": "Events",
        "isGodNode": False,
        "type": "Milestone",
        "file": "roadmap/SEMESTER_1_ACTION_PLAN.md",
        "details": "A-Block Amfisinde resmi kulüp lansmanı, üye alımı ve dönem açılış sunumu."
    })

    add_node({
        "id": "event_hackathon",
        "label": "IUS DevHack 2026/2027 (24h)",
        "cluster": "Events",
        "isGodNode": True,
        "type": "Flagship",
        "file": "roadmap/FLAGSHIP_EVENTS.md",
        "details": "24 saatlik büyük IUS yazılım ve inovasyon maratonu. Nakit ödüller ve şirket mentörleri."
    })

    add_node({
        "id": "ext_industry",
        "label": "Sarajevo Tech Ecosystem",
        "cluster": "External",
        "isGodNode": False,
        "type": "Partner",
        "file": "roadmap/FLAGSHIP_EVENTS.md",
        "details": "Bit Alliance ve Saraybosna yazılım şirketleri (Sponsorluk ve konuşmacı havuzu)."
    })

    # 7. MANAGEMENT BOARD NODES
    for member_key, b in BOARD_MEMBERS.items():
        node_id = b["id"]
        add_node({
            "id": node_id,
            "label": f"{b['name']} ({b['role'].split('(')[0].strip()})",
            "cluster": "Leadership",
            "isGodNode": b["isGodNode"],
            "type": "BoardMember",
            "file": "organization/ROLE_DESCRIPTIONS.md",
            "role_title": b["role"],
            "student_id": b.get("student_id", ""),
            "dept": b.get("dept", ""),
            "duties": b["duties"],
            "tools": b["tools"],
            "collaborates": b["collaborates"],
            "details": f"[{b['role']}] {b.get('dept', '')} - No: {b.get('student_id', '')}\nGörevler: {b['duties']}"
        })

    # Board Internal & Core Edges (Gerçek Yönetim ve Resmi Hiyerarşi)
    edges.append({"source": "board_hasan_kaan", "target": "board_mahmut_ihsan", "relation": "ASIL_BASKAN_YARDIMCISI"})
    edges.append({"source": "board_mahmut_ihsan", "target": "board_hasan_kaan", "relation": "REPORTS_TO_ASIL_BASKAN"})
    edges.append({"source": "board_hasan_kaan", "target": "board_kaan_mete", "relation": "GOREVLENDIRIR_RESMI_TEMSILCI"})
    edges.append({"source": "board_kaan_mete", "target": "board_hasan_kaan", "relation": "RAPORLAR_ASIL_BASKANA"})
    edges.append({"source": "board_bekir_enes", "target": "board_hasan_kaan", "relation": "REPORTS_FINANCE_TO"})

    edges.append({"source": "board_kaan_mete", "target": "sks", "relation": "SCC_2_SINIF_RESMI_IMZACI"})
    edges.append({"source": "board_kaan_mete", "target": "advisor", "relation": "RESMI_OGRENCI_TEMSILCISI"})
    edges.append({"source": "board_kaan_mete", "target": "doc_constitution", "relation": "RESMI_EVRAKTA_IMZACI"})
    edges.append({"source": "board_hasan_kaan", "target": "event_launch", "relation": "LIDERLIK_EDER"})

    edges.append({"source": "board_hasan_kaan", "target": "platform_linear", "relation": "ORCHESTRATES_TASKS"})
    edges.append({"source": "board_hasan_kaan", "target": "tool_ide", "relation": "AUTOMATES_WITH"})
    edges.append({"source": "board_hasan_kaan", "target": "comm_software", "relation": "DIRECTS_COMMITTEE"})
    edges.append({"source": "board_hasan_kaan", "target": "comm_multi", "relation": "DIRECTS_COMMITTEE"})

    edges.append({"source": "board_mahmut_ihsan", "target": "sheet_responses", "relation": "MONITORS_FORM"})
    edges.append({"source": "board_mahmut_ihsan", "target": "comm_whatsapp", "relation": "MODERATES_COMMUNITY"})
    edges.append({"source": "board_mahmut_ihsan", "target": "doc_founding", "relation": "COMPILES_10_MEMBERS"})

    edges.append({"source": "board_bekir_enes", "target": "board_mahmut_ihsan", "relation": "KOORDINE_OLUR"})
    edges.append({"source": "board_bekir_enes", "target": "doc_sponsorship", "relation": "AUTHORS_PACKAGE"})
    edges.append({"source": "board_bekir_enes", "target": "doc_budget", "relation": "MANAGES_1300KM_BUDGET"})
    edges.append({"source": "board_bekir_enes", "target": "ext_industry", "relation": "PITCHES_SPONSORSHIPS"})

    edges.append({"source": "board_pr_lead", "target": "board_bekir_enes", "relation": "COLLABORATES_ON_PROMO"})
    edges.append({"source": "board_pr_lead", "target": "board_hasan_kaan", "relation": "COORDINATES_MEDIA"})

    # Committee / Event / External Edges
    edges.append({"source": "comm_software", "target": "event_hackathon", "relation": "LEADS_TECHNICAL"})
    edges.append({"source": "ext_industry", "target": "event_hackathon", "relation": "SPONSORS"})
    edges.append({"source": "doc_founding", "target": "sks", "relation": "SUBMITTED_TO"})
    edges.append({"source": "comm_whatsapp", "target": "sheet_responses", "relation": "FUNNELS_REGISTRATIONS"})

    # 8. LINEAR TASK NODES & EDGES (LIVE)
    def get_ident_num(x):
        m = re.search(r'\d+', x.get("identifier", ""))
        return int(m.group()) if m else 999
    
    sorted_issues = sorted(raw_issues, key=get_ident_num)
    total_tasks = len(sorted_issues)

    CLEAN_TASK_TITLES = {
        "IUS-5": "Danışman Resmi Daveti",
        "IUS-6": "SCC Faaliyet Planı & Bütçe",
        "IUS-7": "Yönetim Kurulu Kadrosu",
        "IUS-8": "10 Üye Birebir Kayıt (2/10)",
        "IUS-9": "Kampüs Standı & Afişler",
        "IUS-10": "AI & Prompt Atölyeleri",
        "IUS-11": "Haftalık Online Tech-Talks",
        "IUS-12": "Kampüs Konuşmacıları",
        "IUS-13": "DevHack 2027 Hackathonu",
    }

    for idx, issue in enumerate(sorted_issues):
        ident = issue.get("identifier", "")
        title = issue.get("title", "")
        state_name = issue.get("state", {}).get("name", "Backlog")
        assignee_name = issue.get("assignee", {}).get("name", "Unassigned")
        priority_val = issue.get("priority", 0)
        url = issue.get("url", "")
        desc = issue.get("description", "") or ""

        task_node_id = f"linear_task_{ident}"

        # Determine isGodNode for top urgent active tasks
        is_god = state_name in ("In Progress", "Todo") and priority_val in (1, 2)

        # Coordinate calculation along the top horizontal celestial arc
        # Spans from -760 to +760, arched slightly at y: -500 to -550
        if total_tasks > 1:
            task_x = -760 + idx * (1520 / (total_tasks - 1))
            center_norm = abs(idx - (total_tasks - 1) / 2) / ((total_tasks - 1) / 2)
            task_y = -550 + int(center_norm * 45)
        else:
            task_x = 0
            task_y = -520

        # Concise clean title
        task_clean_title = CLEAN_TASK_TITLES.get(ident)
        if not task_clean_title:
            task_clean_title = re.sub(r'^[^\w\s]+', '', title).strip()
            task_clean_title = re.sub(r'\[.*?\]', '', task_clean_title).strip()
            if len(task_clean_title) > 28:
                task_clean_title = task_clean_title[:26] + ".."

        node_label = f"[{ident}] {task_clean_title}"

        nodes.append({
            "id": task_node_id,
            "label": node_label,
            "cluster": "Linear Tasks",
            "isGodNode": is_god,
            "type": "LinearTask",
            "task_ident": ident,
            "task_state": state_name,
            "task_priority": priority_val,
            "task_assignee": assignee_name,
            "url": url,
            "file": "scripts/linear_ops.py",
            "x": int(task_x),
            "y": int(task_y),
            "details": f"[{ident}] {title}\nDurum: {state_name} | Sorumlu: {assignee_name}\nÖncelik: {priority_val}\nURL: {url}\n\nÖzet: {desc[:280]}..."
        })

        # Connect Task -> Linear Platform
        edges.append({
            "source": task_node_id,
            "target": "platform_linear",
            "relation": "TRACKED_IN"
        })

        # Connect Board Assignee -> Task
        board_assignee_id = resolve_assignee_id(assignee_name)
        edges.append({
            "source": board_assignee_id,
            "target": task_node_id,
            "relation": f"LEADS_{state_name.upper().replace(' ', '_')}"
        })

        # Domain Specific Semantic Connections for Known Tasks
        if "5" in ident:
            edges.append({"source": task_node_id, "target": "advisor", "relation": "TARGETS_PROFESSOR"})
            edges.append({"source": task_node_id, "target": "doc_advisor_letter", "relation": "USES_OFFICIAL_LETTER"})
        elif "6" in ident:
            edges.append({"source": task_node_id, "target": "doc_annual_plan", "relation": "DELIVERS_PLAN"})
            edges.append({"source": task_node_id, "target": "doc_budget", "relation": "DELIVERS_BUDGET"})
            edges.append({"source": task_node_id, "target": "sks", "relation": "SUBMITS_TO"})
        elif "7" in ident:
            edges.append({"source": task_node_id, "target": "board_pr_lead", "relation": "RECRUITS_FOR"})
            edges.append({"source": task_node_id, "target": "doc_founding", "relation": "COMPLETES_BOARD"})
        elif "8" in ident:
            edges.append({"source": task_node_id, "target": "sheet_responses", "relation": "INGESTS_RECORDS"})
            edges.append({"source": task_node_id, "target": "doc_founding", "relation": "POPULATES_10_MEMBERS"})
            edges.append({"source": task_node_id, "target": "comm_whatsapp", "relation": "INVITES_CONFIDENTIAL"})
        elif "9" in ident:
            edges.append({"source": task_node_id, "target": "event_launch", "relation": "PREPARES_STAND"})
            edges.append({"source": task_node_id, "target": "board_pr_lead", "relation": "DELEGATES_PROMO"})
        elif "10" in ident:
            edges.append({"source": task_node_id, "target": "comm_software", "relation": "CURATES_CURRICULUM"})
        elif "11" in ident:
            edges.append({"source": task_node_id, "target": "comm_whatsapp", "relation": "ANNOUNCES_ON"})
            edges.append({"source": task_node_id, "target": "comm_software", "relation": "HOSTED_BY"})
        elif "12" in ident:
            edges.append({"source": task_node_id, "target": "ext_industry", "relation": "INVITES_SPEAKERS"})
            edges.append({"source": task_node_id, "target": "event_launch", "relation": "HOSTS_IN_AMPHI"})
        elif "13" in ident:
            edges.append({"source": task_node_id, "target": "event_hackathon", "relation": "PLANS_HACKATHON"})
            edges.append({"source": task_node_id, "target": "doc_sponsorship", "relation": "SEEKS_SPONSORS"})

    # 9. NORMAL MEMBER NODES (From Google Sheet Responses)
    for member_idx, r in enumerate(normal_member_rows, 1):
        m_name = r[1].strip()
        m_id = r[4].strip()
        m_dept = r[5].strip() if len(r) > 5 else ""
        m_year = r[6].strip() if len(r) > 6 else ""

        member_node_id = f"member_{re.sub(r'[^a-zA-Z0-9]', '_', m_name.lower())}_{m_id}"
        member_x = 750
        member_y = 60 + (member_idx - 1) * 75

        nodes.append({
            "id": member_node_id,
            "label": f"👤 {m_name} (Member #{member_idx})",
            "cluster": "Members",
            "isGodNode": False,
            "type": "Member",
            "file": "data/form_responses.csv",
            "student_id": m_id,
            "dept": f"{m_dept} ({m_year}. Sınıf)",
            "x": int(member_x),
            "y": int(member_y),
            "details": f"Onaylı Normal Üye #{member_idx}\nÖğrenci No: {m_id}\nBölüm: {m_dept} ({m_year}. Sınıf)\nDurum: Aktif Kayıtlı Üye (Tüzük 10-Üye Kotası: {len(normal_member_rows)}/10)."
        })

        edges.append({"source": "sheet_responses", "target": member_node_id, "relation": "REGISTERED_VIA"})
        edges.append({"source": member_node_id, "target": "comm_whatsapp", "relation": "MEMBER_OF"})
        edges.append({"source": member_node_id, "target": "doc_founding", "relation": "RECORDED_IN"})
        if "computer" in m_dept.lower() or "cse" in m_dept.lower() or "yazılım" in m_dept.lower():
            edges.append({"source": member_node_id, "target": "comm_software", "relation": "JOINS_COMMITTEE"})
        else:
            edges.append({"source": member_node_id, "target": "comm_multi", "relation": "JOINS_COMMITTEE"})

    graph_data = {
        "project": "IUS Engineering Events Club",
        "generated_at": datetime.now().isoformat(),
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "linear_tasks": len(raw_issues),
            "registered_members": len(normal_member_rows),
            "board_members": 5
        },
        "nodes": nodes,
        "edges": edges
    }

    # Save to graph.json
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    with open(GRAPH_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    # Also save to root graph.json for root HTTP server
    with open(WORKSPACE_ROOT / "graph.json", "w", encoding="utf-8") as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    print(f"[✓] graph.json güncellendi: {GRAPH_JSON_FILE} ({len(nodes)} Düğüm, {len(edges)} Bağlantı)")

    # Inject embedded data into graph.html for offline/file:// support
    if GRAPH_HTML_FILE.exists():
        try:
            with open(GRAPH_HTML_FILE, "r", encoding="utf-8") as f:
                html_content = f.read()
            
            embedded_script = f"<script>window.EMBEDDED_GRAPH_DATA = {json.dumps(graph_data, ensure_ascii=False)};</script>\n"
            
            # Remove old embedded script if exists
            html_content = re.sub(r'<script>window\.EMBEDDED_GRAPH_DATA = .*?;</script>\n?', '', html_content)
            
            # Insert before </head>
            if "</head>" in html_content:
                html_content = html_content.replace("</head>", f"{embedded_script}</head>")
                with open(GRAPH_HTML_FILE, "w", encoding="utf-8") as f:
                    f.write(html_content)
                # Mirror to root index.html and graphify-out/index.html
                with open(WORKSPACE_ROOT / "index.html", "w", encoding="utf-8") as f:
                    f.write(html_content)
                with open(GRAPH_DIR / "index.html", "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"[✓] graph.html ve index.html güncellendi (gömülü veri ve aynalar senkronize edildi).")
        except Exception as e:
            print(f"[!] graph.html gömme hatası: {e}")

    if "--push" in sys.argv:
        try:
            import subprocess
            subprocess.run(["git", "add", "index.html", "graph.json", "graphify-out/"], check=False, cwd=str(WORKSPACE_ROOT))
            subprocess.run(["git", "commit", "-m", "chore: sync observatory ecosystem updates"], check=False, cwd=str(WORKSPACE_ROOT))
            push_res = subprocess.run(["git", "push", "origin", "main"], check=False, cwd=str(WORKSPACE_ROOT))
            if push_res.returncode == 0:
                print("[✓] GitHub Pages için güncellemeler başarıyla pushlandı (https://hasankaan28.github.io/ius-engineering-events/).")
            else:
                print("[!] Git push uyarısı.")
        except Exception as e:
            print(f"[!] Git push hatası: {e}")

    return graph_data

if __name__ == "__main__":
    data = build_observatory_graph()
    print("[*] Observatory senkronizasyonu tamamlandı.")

