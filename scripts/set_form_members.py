#!/usr/bin/env python3
"""
Dynamic Member Selection Tool for student_club_registration_form_f252.docx
Allows selecting the 10 students who will be physically present on campus to sign.
"""

import os
import sys
import json
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fill_docx_form

ALL_APPLICANTS = [
    # Core Board
    {"name": "Kaan Mete Şenyıldız", "email": "kmsenyildiz@gmail.com", "id": "250302201", "role": "President", "lang": "TR", "phone": "+90 553 113 11 98"},
    {"name": "Hasan Kaan Karabulut", "email": "hasankaankarabulut121@gmail.com", "id": "250302195", "role": "Vice President", "lang": "TR", "phone": "Self"},
    {"name": "Mahmut İhsan Avcı", "email": "mahmut.ihsanavcii@gmail.com", "id": "250302233", "role": "Secretary", "lang": "TR", "phone": "540 002 0571"},
    {"name": "Bekir Enes Çokbekler", "email": "becokbekler@student.ius.edu.ba", "id": "250302229", "role": "Treasurer", "lang": "TR", "phone": "05523822006"},
    {"name": "Bakir Bašić", "email": "260302030@student.ius.edu.ba", "id": "260302030", "role": "PR & Media Lead", "lang": "BS", "phone": "+387-61-533-947"},
    
    # Active Applicants / Members
    {"name": "Bilal Yusuf Şimşek", "email": "Simsekbilal59@gmail.com", "id": "250302196", "role": "Member", "lang": "TR", "phone": "05510789863"},
    {"name": "Nazlıcan Cebeci", "email": "nazlii.cebeci@gmail.com", "id": "250302243", "role": "Member", "lang": "TR", "phone": "+387671491362"},
    {"name": "Muhammed Emin Tiryaki", "email": "metiryaki@student.ius.edu.ba", "id": "250302247", "role": "Member", "lang": "TR", "phone": "05384849161"},
    {"name": "Emin Efe Duman", "email": "emnfdmn@gmail.com", "id": "250302211", "role": "Member", "lang": "TR", "phone": "+905413216147"},
    {"name": "Ahmed Hadzimurati", "email": "260302051@student.ius.edu.ba", "id": "260302051", "role": "Member", "lang": "BS", "phone": "+38762667105"},
    
    # Reserve / Alternate Pool
    {"name": "Ömer Arif Açıkel", "email": "o.arifacikel@gmail.com", "id": "250302232", "role": "Member (Reserve)", "lang": "TR", "phone": "+90 5425531700"},
    {"name": "Mert Çınar Atalay", "email": "atalayss301@gmail.com", "id": "250302162", "role": "Member (Reserve)", "lang": "TR", "phone": "+90 542 357 27 33"},
    {"name": "Ferit Enes Seymenliler", "email": "eenesseymenliler@gmail.com", "id": "240302180", "role": "Member (Reserve)", "lang": "TR", "phone": "+905439408266"},
    {"name": "Hüseyin Talha Seymenliler", "email": "tseymenliler16@gmail.com", "id": "240302179", "role": "Member (Reserve)", "lang": "TR", "phone": "05469309470"},
    {"name": "Muhammed Efe Ural", "email": "uralefe10@gmail.com", "id": "240302169", "role": "Member (Reserve)", "lang": "TR", "phone": "05375606608"},
    {"name": "Abdullah Uzun", "email": "250201110@student.ius.edu.ba", "id": "250201110", "role": "Member (Reserve)", "lang": "TR", "phone": "05362209236"},
]

def list_roster():
    print("=" * 65)
    print("📋 TÜM ADAYLAR VE İMZA HAVUZU (16 KİŞİ)")
    print("=" * 65)
    for i, a in enumerate(ALL_APPLICANTS, 1):
        status = "✅ ASİL (İlk 10)" if i <= 10 else "⏳ YEDEK HAVUZ"
        print(f"[{i:2d}] {a['name']:<25} | {a['lang']} | {a['phone']:<16} | {status}")
    print("=" * 65)

if __name__ == "__main__":
    list_roster()
