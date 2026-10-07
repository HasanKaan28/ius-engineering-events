# Project Context: IUS Engineering Events Club

## 1. Overview & Vision
- **Organization**: IUS Engineering Events Club (International University of Sarajevo)
- **Institution**: International University of Sarajevo (IUS), Faculty of Engineering and Natural Sciences (FENS)
- **Leadership**: Led by Club Captain / President with a core founding committee.
- **Language**: 100% English (Official documents, external partnerships, event communications).
- **Mission**: Bridging the gap between university engineering curriculum and real-world industrial practice via hands-on workshops, hackathons, AI/coding bootcamps, student engineering projects, and high-impact industry networking in Sarajevo and globally.

## 2. Directory Structure
```
ius-engineering-events/
├── .agents/rules/project-context.md   # Architectural snapshot & memory
├── constitution/
│   └── CONSTITUTION.md               # Official Club Constitution (English)
├── organization/
│   ├── ORGANIZATIONAL_STRUCTURE.md   # Core leadership, committees & hierarchy
│   └── ROLE_DESCRIPTIONS.md          # Duties, responsibilities & KPIs
├── roadmap/
│   ├── SEMESTER_1_ACTION_PLAN.md     # 12-week operational milestone calendar
│   └── FLAGSHIP_EVENTS.md            # Detailed blueprints for hackathons & summits
├── templates/
│   ├── ACADEMIC_ADVISOR_INVITATION.md# Formal invitation for FENS Professors
│   ├── IUS_SKS_APPLICATION_PETITION.md# SKS / Student Affairs registration form
│   └── EVENT_PROPOSAL_FORM.md        # Standard university event petition
├── graphify-out/
│   ├── graph.json                    # Interactive ecosystem graph dataset
│   └── graph.html                    # Cyberpunk Observatory Interactive Visualizer
├── GEMINI.md                         # Persistent workspace metadata
└── README.md                         # Executive project documentation
```

## 3. Core Pillars & Committees
1. **Multidisciplinary Engineering Committee**: Cross-discipline hardware/software integration (EE, ME, CS, IE).
2. **Software & Artificial Intelligence Committee**: CS/SE deep dives, modern web/cloud architecture, LLMs/GenAI, coding bootcamps.
3. **Applied Engineering Projects**: Practical student development circles, prototypes, and semester showcases.
4. **Operations & Event Logistics**: Venue reservation (IUS Amphitheater, A-Block, Labs), technical equipment, ticketing/registration.
5. **PR, Media & Corporate Relations**: Branding, social media, photography, company sponsorships, and Sarajevo tech ecosystem outreach.

## 4. Operational Infrastructure & Integrations
- **Management Team Application Form**: [https://forms.gle/v8c85MgFUmVvpzTH6](https://forms.gle/v8c85MgFUmVvpzTH6)
- **Live Google Sheet Responses**: [https://docs.google.com/spreadsheets/d/1pLeiQpBNSfDFPGa5IqLbSGoz0Z2Lm3Olu-mq3XZhzbQ/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1pLeiQpBNSfDFPGa5IqLbSGoz0Z2Lm3Olu-mq3XZhzbQ/edit?usp=sharing)
- **Spreadsheet Live Fetcher**: [`scripts/fetch_google_sheet.py`](file:///C:/Users/Kaan/.gemini/antigravity-ide/scratch/ius-engineering-events/scripts/fetch_google_sheet.py)
- **Official WhatsApp Community**: [https://chat.whatsapp.com/LKMpyfm7K5R3F0rXezcXXN](https://chat.whatsapp.com/LKMpyfm7K5R3F0rXezcXXN)
- **Task & Team Management Platform**: Linear.app (100% Free, unlimited team members, native desktop & iOS/Android apps).
- **IDE Automation Bridge**: [`scripts/linear_manager.py`](file:///C:/Users/Kaan/.gemini/antigravity-ide/scratch/ius-engineering-events/scripts/linear_manager.py) & [`scripts/linear_ops.py`](file:///C:/Users/Kaan/.gemini/antigravity-ide/scratch/ius-engineering-events/scripts/linear_ops.py) (GraphQL API integration).
- **Observatory Knowledge Graph Synchronizer**: [`scripts/sync_observatory.py`](file:///C:/Users/Kaan/.gemini/antigravity-ide/scratch/ius-engineering-events/scripts/sync_observatory.py) (Pulls live Linear tasks, Google Form responses, board member relationships, and updates `graphify-out/graph.json` and `graph.html`).
- **GitHub Repository & 7/24 Cloud Host**: [https://github.com/HasanKaan28/ius-engineering-events](https://github.com/HasanKaan28/ius-engineering-events)
- **Permanent 7/24 Live Observatory (GitHub Pages)**: [https://hasankaan28.github.io/ius-engineering-events/](https://hasankaan28.github.io/ius-engineering-events/) (Kalıcı, bilgisayar kapalıyken bile 7/24 aktif, sınırsız global CDN).
- **Interactive Cyberpunk Observatory**: [`graphify-out/graph.html`](file:///C:/Users/Kaan/.gemini/antigravity-ide/scratch/ius-engineering-events/graphify-out/graph.html) (Local `http://localhost:8085/`).
- **Founding & Member Status**: 
  - **Yönetim Kurulu (5 Kişi)**: 
    - 👑 **Asıl Kulüp Başkanı & Kurucu Lider**: Hasan Kaan (Tüm operasyonel, teknik ve idari kararların lideri, nihai karar mercii).
    - 🚀 **Asıl Başkan Yardımcısı & İdari Koordinatör**: Mahmut İhsan Avcı (Operasyonel sağ kol, üye alımları, bürokrasi ve toplantı kayıtları).
    - 🏛️ **Resmi / Göstermelik Başkan (Statutory President)**: Kaan Mete Şenyıldız (SCC mevzuatındaki "Kulüp başkanı en az 2. sınıf olmalıdır" kuralını karşılamak üzere resmi evraklardaki imza mercii ve okul nezdindeki temsilci).
    - 💰 **Sayman & Finans Lideri**: Bekir Enes Çokbekler (Bütçe yönetimi ve kurumsal sponsorluklar).
    - 📣 **PR & Media Lead**: ⚠️ **EKSİK / AÇIK POZİSYON** (Sosyal medya, tasarım ve kampüs içi lansman).
  - **Normal Üyeler (10 Kişi Hedefi)**: Formdan gelen herkes (Bilal Yusuf, Nazlıcan, Muhammed Emin, Emin Efe Duman vb.) kullanıcı özellikle PR Lead olarak atamadıkça doğrudan **Üye (Member)** statüsündedir (Şu an 4/10 kayıtlı).
  - **Okula Teslim Başvuru Dosyası (SKS / SCC Paketi)**:
    - Tüm başvuru evrakları (`templates/` ve `export_documents/`) okula sunulacak resmi **Prijedlog (Proposal)** formatındadır.
    - Hiçbir bütçe kalemi, üyelik veya izin "Onaylandı" olarak doldurulmaz; tüm kalemler **Projekcija / Planirano / Pending SCC Review** olarak işaretlenmiştir.
    - Okula teslim edilecek belgelerde iç yönetim notları (göstermelik başkan vb.) kesinlikle yer almaz; resmi unvanlar, ıslak imza satırları ve okulun değerlendirme/kaşeleme yapacağı boş SCC kutuları mevcuttur.

## 5. Key Milestones
- **M1 (Week 1–2)**: Faculty Advisor recruitment & SKS official filing.
- **M2 (Week 3–4)**: Core team onboarding, Linear workspace setup & IUS-wide Welcome Meeting / Launch Event.
- **M3 (Week 5–8)**: Bi-weekly hands-on workshops & Competition team selection.
- **M4 (Week 9–12)**: Flagship IUS Hackathon & Semester Showcase.
