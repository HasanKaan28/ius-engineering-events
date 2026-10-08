import os, sys, shutil, zipfile, xml.etree.ElementTree as ET

def fill_docx():
    src_docx = r'C:\Users\Kaan\Desktop\student_club_registration_form_f252.docx'
    if not os.path.exists(src_docx):
        print(f"File not found: {src_docx}")
        return

    # Extract all files
    extract_dir = r'C:\Users\Kaan\.gemini\antigravity-ide\scratch\ius-engineering-events\data\docx_temp'
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(src_docx, 'r') as z:
        z.extractall(extract_dir)

    doc_xml_path = os.path.join(extract_dir, 'word', 'document.xml')
    tree = ET.parse(doc_xml_path)
    root = tree.getroot()

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    ET.register_namespace('w', ns['w'])

    def set_cell_text(tc, text):
        p = tc.find('w:p', ns)
        if p is None:
            p = ET.SubElement(tc, f"{{{ns['w']}}}p")
        # Remove existing r
        for r in p.findall('w:r', ns):
            p.remove(r)
        new_r = ET.SubElement(p, f"{{{ns['w']}}}r")
        rPr = ET.SubElement(new_r, f"{{{ns['w']}}}rPr")
        rFonts = ET.SubElement(rPr, f"{{{ns['w']}}}rFonts")
        rFonts.set(f"{{{ns['w']}}}ascii", "Calibri")
        sz = ET.SubElement(rPr, f"{{{ns['w']}}}sz")
        sz.set(f"{{{ns['w']}}}val", "22")
        new_t = ET.SubElement(new_r, f"{{{ns['w']}}}t")
        new_t.text = text

    tbls = root.findall('.//w:tbl', ns)

    # TABLE 0: Basic info
    # Row 1: Club name
    # Row 2: Status
    # Row 3: Academic Year
    if len(tbls) > 0:
        rows = tbls[0].findall('w:tr', ns)
        if len(rows) > 1:
            tcs = rows[1].findall('w:tc', ns)
            if len(tcs) > 0:
                set_cell_text(tcs[0], "IUS Engineering Events Club (IEEC)")
        if len(rows) > 2:
            tcs = rows[2].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "[ X ] NEW")
        if len(rows) > 3:
            tcs = rows[3].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "2026 / 2027")

    # TABLE 1: Purpose & Board
    # Row 1: Purpose
    # Row 5: Advisor -> Prof. Dr. Leila Miller
    # Row 6: President -> Kaan Mete Şenyıldız
    # Row 7: Vice President -> Mahmut İhsan Avcı
    # Row 8: Secretary -> Mahmut İhsan Avcı
    # Row 9: Treasurer -> Bekir Enes Çokbekler
    # Row 10: PR -> [In Appointment Process / Open Position]
    if len(tbls) > 1:
        rows = tbls[1].findall('w:tr', ns)
        if len(rows) > 1:
            tcs = rows[1].findall('w:tc', ns)
            if len(tcs) > 0:
                purpose_text = "The IUS Engineering Events Club (IEEC) is established as an Academic and Educational Club (AEC) under the Faculty of Engineering and Natural Sciences (FENS) to bridge university engineering education with real-world industrial practice through technical workshops, AI bootcamps, multidisciplinary student engineering project teams, and tech industry networking."
                set_cell_text(tcs[0], purpose_text)
        if len(rows) > 5:
            tcs = rows[5].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "Prof. Dr. Leila Miller")
        if len(rows) > 6:
            tcs = rows[6].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "Kaan Mete Şenyıldız")
        if len(rows) > 7:
            tcs = rows[7].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "Mahmut İhsan Avcı")
        if len(rows) > 8:
            tcs = rows[8].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "Mahmut İhsan Avcı")
        if len(rows) > 9:
            tcs = rows[9].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "Bekir Enes Çokbekler")
        if len(rows) > 10:
            tcs = rows[10].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "[In Appointment Process / Open Position]")

    # TABLE 2: Contact Information
    # Row 2: President Name -> Kaan Mete Şenyıldız
    # Row 3: President Phone -> +90 553 113 11 98
    # Row 4: President Email -> kmsenyildiz@gmail.com
    # Row 6: Advisor Name -> Prof. Dr. Leila Miller (Full Professor Dr.)
    # Row 7: Advisor Phone -> 033 957 -
    # Row 8: Advisor Email -> lmiller@ius.edu.ba (Assistant: itarhanis-papic@ius.edu.ba)
    if len(tbls) > 2:
        rows = tbls[2].findall('w:tr', ns)
        if len(rows) > 2:
            tcs = rows[2].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "Kaan Mete Şenyıldız")
        if len(rows) > 3:
            tcs = rows[3].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "+90 553 113 11 98")
        if len(rows) > 4:
            tcs = rows[4].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "kmsenyildiz@gmail.com")
        if len(rows) > 6:
            tcs = rows[6].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "Prof. Dr. Leila Miller (Full Professor Dr.)")
        if len(rows) > 7:
            tcs = rows[7].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "033 957 -")
        if len(rows) > 8:
            tcs = rows[8].findall('w:tc', ns)
            if len(tcs) > 1:
                set_cell_text(tcs[1], "lmiller@ius.edu.ba (Assistant: itarhanis-papic@ius.edu.ba)")

    # TABLE 3: Member list (Rows 3..17)
    members_data = [
        ("Kaan Mete Şenyıldız", "kmsenyildiz@gmail.com", "250302201"),
        ("Hasan Kaan", "ufukkarabulut35@gmail.com", "250302195"),
        ("Mahmut İhsan Avcı", "mahmut.ihsanavcii@gmail.com", "250302233"),
        ("Bekir Enes Çokbekler", "46bekir70@gmail.com", "250302229"),
        ("Bilal Yusuf Şimşek", "Simsekbilal59@gmail.com", "250302196"),
        ("Nazlıcan Cebeci", "nazlii.cebeci@gmail.com", "250302243"),
        ("Muhammed Emin", "duduck6107@gmail.com", "250302247"),
        ("Emin Efe Duman", "emnfdmn@gmail.com", "250302211"),
        ("Bakir", "260302030@student.ius.edu.ba", "260302030"),
        ("Ömer Arif Açıkel", "o.arifacikel@gmail.com", "250302232"),
        ("Mert Çınar Atalay", "atalayss301@gmail.com", "250302162"),
        ("Ferit Enes Seymenliler", "eenesseymenliler@gmail.com", "240302180"),
        ("Hüseyin Talha Seymenliler", "tseymenliler16@gmail.com", "240302179"),
        ("Muhammed Efe Ural", "uralefe10@gmail.com", "240302169"),
        ("Abdullah Uzun", "250201110@student.ius.edu.ba", "250201110"),
    ]

    if len(tbls) > 3:
        rows = tbls[3].findall('w:tr', ns)
        # rows[0] is header title, rows[1] is note, rows[2] is table columns No | Name | Email | Student ID | Signature
        for i, m in enumerate(members_data):
            row_idx = 3 + i
            if row_idx < len(rows):
                tcs = rows[row_idx].findall('w:tc', ns)
                if len(tcs) > 3:
                    set_cell_text(tcs[0], str(i + 1))
                    set_cell_text(tcs[1], m[0])
                    set_cell_text(tcs[2], m[1])
                    set_cell_text(tcs[3], m[2])

    tree.write(doc_xml_path, encoding='utf-8', xml_declaration=True)

    # Rezip into target files
    out_desktop_filled = r'C:\Users\Kaan\Desktop\student_club_registration_form_f252_DOLDURULMUS.docx'
    out_export_filled = r'C:\Users\Kaan\.gemini\antigravity-ide\scratch\ius-engineering-events\export_documents\student_club_registration_form_f252_FILLED.docx'

    def make_zip(out_path):
        with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zip_out:
            for foldername, subfolders, filenames in os.walk(extract_dir):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    arcname = os.path.relpath(filepath, extract_dir)
                    zip_out.write(filepath, arcname)

    make_zip(out_desktop_filled)
    make_zip(out_export_filled)
    # Also overwrite desktop original after backing up
    orig_bak = r'C:\Users\Kaan\Desktop\student_club_registration_form_f252_ORIGINAL_BACKUP.docx'
    if not os.path.exists(orig_bak):
        shutil.copy2(src_docx, orig_bak)
    shutil.copy2(out_desktop_filled, src_docx)

    shutil.rmtree(extract_dir)
    print("SUCCESS: Docx filled with Prof. Dr. Leila Miller and all club data!")
    print(f"Generated: {out_desktop_filled}")
    print(f"Generated: {out_export_filled}")
    print(f"Updated: {src_docx}")

if __name__ == '__main__':
    fill_docx()
