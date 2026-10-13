import csv
import struct
from generate_untranslated_csv import rows, keys, sw_d, clean_ctrl

out_path = r'SAOHR_Switch_Thai_Mod\untranslated_108_thai.csv'
with open(out_path, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow([
        'ลำดับ (No.)',
        'Message_ID',
        'หมวดหมู่และบริบท (Category & Context)',
        'ข้อความภาษาอังกฤษต้นฉบับ (Target English)',
        'คำแปลภาษาไทย (Thai Translation)',
        'อ้างอิง: ประโยคก่อนหน้า (Prev Line)',
        'อ้างอิง: ประโยคถัดไป (Next Line)'
    ])
    for no, mid, cat, en, th in rows:
        idx = keys.index(mid)
        p_id = keys[idx-1] if idx > 0 else None
        n_id = keys[idx+1] if idx + 1 < len(keys) else None
        p_str = f"[{p_id}] {clean_ctrl(sw_d.get(p_id, ''))}" if p_id else ""
        n_str = f"[{n_id}] {clean_ctrl(sw_d.get(n_id, ''))}" if n_id else ""
        w.writerow([no, mid, cat, en, th, p_str, n_str])

print('Reordered CSV columns successfully:', out_path)
