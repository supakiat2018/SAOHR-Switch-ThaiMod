"""
Injects 32 newly translated dialogue entries into SAOHR event script files (script/script/*)
and verifies bytecode pointers and CJK encoding with 0 missing clusters.
"""

import os
import shutil
import struct
import csv
from datetime import datetime

base_dir = r"C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp"
script_dir = os.path.join(base_dir, r"extracted_pc_thai_usa\script\script")
backup_base = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\backups")
csv_path = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\untranslated_scripts_32.csv")

# Load cluster mapping from inject_108_translations
with open(os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\tools\inject_108_translations.py"), encoding="utf-8") as f:
    code = f.read().split("# Verify 100%")[0]

ns = {}
exec(code, ns)
cluster_map = ns["cluster_to_cjk"]
cluster_map["ไม"] = chr(0x5D1F)
cluster_map["ทำ"] = chr(0x522A)
cluster_map["เดี่"] = chr(0x5854)
cluster_map["ก่"] = chr(0x4E98)
cluster_map["เปิ"] = chr(0x5902)
cluster_map["นั่"] = chr(0x5275)
cluster_map["ดื่"] = chr(0x518F)
cluster_map["ฝึ"] = chr(0x5353)
cluster_map["เก็"] = chr(0x5759)
cluster_map["ฝั"] = chr(0x534D)
cluster_map["ลึ"] = chr(0x54E5)
cluster_map["เที"] = chr(0x58B2)
cluster_map["ยู"] = chr(0x5442)

split_saohr_thai = ns["split_saohr_thai"]

def encode_thai_to_cjk(th_str):
    clusters = split_saohr_thai(th_str)
    out = []
    for cl in clusters:
        if any('\u0e00' <= c <= '\u0e7f' for c in cl):
            if cl not in cluster_map:
                raise ValueError(f"Unmapped Thai cluster: {cl!r} in {th_str!r}")
            out.append(cluster_map[cl])
        else:
            out.append(cl)
    return "".join(out)

translations = [
    (1, '9iuq', '40_4090_054_0', "I think perhaps he we out to be working\nTOGETHER, don't you? Seeing this through\nto the bitter end...", 'ฉันคิดว่าบางทีพวกเราน่าจะร่วมมือกัน\nทำไปด้วยกันนะ จริงไหม? สู้ไปด้วยกัน\nจนถึงที่สุดไปเลย...'),
    (2, 'c7ji', '40_1010_008_0', 'SAO...', 'SAO...'),
    (3, 'c9ic', '40_3020_009_0', "I dunno, my experience probably can't\ntrump a part of fourteen plus...", 'ไม่รู้สิ ประสบการณ์ของฉันคงเทียบกับ\nปาร์ตี้ตั้ง 14 คนขึ้นไปไม่ได้หรอกนะ...'),
    (4, 'c9ic', '40_3020_049_0', "Wait a sec--What did I just say?! How is\nhe not super dead?! You needed a part of\nfourteen just to scrape by!", 'เดี่ยวก่อนนะ--เมื่อกี้ฉันพูดอะไรออกไปนะ?!\nทำไมหมอนั่นถึงยังไม่ตายสนิทอีกล่ะ?!\nต้องมีปาร์ตี้ตั้ง 14 คนถึงจะเอาตัวรอดมาได้นะ!'),
    (5, 'f890', '50_0000_061_0', "Yes... YES! That's perfect! We could go\ndown to the river at sunset and have a\ndeep discussion and exchange jabs!", 'ใช่... ใช่แล้ว! ยอดเยี่ยมไปเลย! พวกเราไปที่ริมแม่น้ำ\nตอนตะวันตกดิน แล้วเปิดใจคุยกันอย่างจริงจัง\nพร้อมกับแลกหมัดกันเลยเป็นไง!'),
    (6, 'f8ou', '50_0510_006_0', "That... Is a really idea! But not mine!\nWhat do you think of Sado? That's right,\nget some tea ceremony going!", 'นั่น... เป็นความคิดที่ดีจริง ๆ! แต่ไม่ใช่ของฉันนะ!\nเธอคิดยังไงกับพิธีชงชาล่ะ? ใช่แล้ว มาจัดพิธีชงชา\nกันดีกว่า!'),
    (7, 'f8ou', '50_0510_007_0', "I've already got all out club activities\nlined up. We start with making delicious\ntea and then we drink said tea.", 'ฉันเตรียมกิจกรรมชมรมทั้งหมดไว้เรียบร้อยแล้วล่ะ\nเราเริ่มจากชงชาอร่อย ๆ แล้วก็ดื่มชานั้นกัน'),
    (8, 'faak', '50_2100_068_0', "Then just keep climbing and down look\nback!", 'ถ้าอย่างนั้นก็ขึ้นไปเรื่อย ๆ แล้วอย่าหันกลับมานะ!'),
    (9, 'fado', '50_2200_124_0', "I should log though. I could still do with\na few hours of real world training.", 'ฉันควรออกจากระบบแล้วล่ะ ยังมีเวลาฝึกฝน\nในชีวิตจริงอีกสักสองสามชั่วโมง'),
    (10, 'fbd0', '50_3200_076_0', "That was really though...", 'นั่นยากจริง ๆ เลยนะ...'),
    (11, 'fbj8', '50_3400_039_0', "Leads head right there.", 'ตรงไปทางนั้นกันเลย'),
    (12, 'fdbg', '50_5200_076_0', "However... This important and slightly\nout-of-place looking stature. Bingo!", 'แต่ว่า... รูปสลักสำคัญที่ดูไม่ค่อยเข้าพวกอันนี้\nใช่เลย!'),
    (13, 'fdho', '50_5400_071_0', "So, the most likely path of events was for\nus to collect the sword and then use it in\nbattle against the false kind.", 'ดังนั้น ทางที่เป็นไปได้ที่สุดก็คือพวกเรา\nต้องไปเก็บดาบเล่มนั้น แล้วนำมาใช้ต่อสู้\nกับราชาตัวปลอมสินะ'),
    (14, 'fe7k', '50_6100_053_0', "My only salvation is the use of one\nancient spell. An incantation of\npathfinding that returns me to my came.", 'หนทางรอดเดียวของฉันคือการใช้คาถาโบราณ\nบทหนึ่ง คาถานำทางที่จะพาฉันกลับไปยังค่าย'),
    (15, 'feds', '50_6300_090_0', "We've got her back.", 'พวกเราจะคอยช่วยเธอเอง'),
    (16, 'fek4', '50_6500_009_0', "Your optimism proves infections. I'll\nfollow your lead.", 'การมองในด้านดีของเธอทำให้ฉันมีพลังตามไปด้วย\nฉันจะตามเธอไปนะ'),
    (17, 'fg30', '50_8000_023_0', "Ah! Hey there, sis!", 'อ๊ะ! หวัดดี พี่สาว!'),
    (18, 'fg30', '50_8000_061_0', "What a worrywart! C'mon sis! Can we?", 'กังวลเกินไปแล้ว! น่านะพี่สาว! ได้ไหมล่ะ?'),
    (19, 'fg3a', '50_8010_043_0', "...Hey sis?", '...นี่ พี่สาว?'),
    (20, 'fg3u', '50_8030_131_0', "Yeah! I think I can see how it would work!\nThis is all thanks to you, sis!", 'ใช่แล้ว! ฉันคิดว่าพอมองเห็นภาพแล้วล่ะ!\nทั้งหมดนี้ต้องขอบคุณพี่สาวเลยนะ!'),
    (21, 'fgjd', '50_8520_028_0', "Eugeo! Switch off!", 'ยูจิโอ! สลับตัว!'),
    (22, 'fk34', '51_2100_055_0', "Maybe... Y'know... there's a little chance\nthat this is what--*ahem*--modestly-sized\ngirls dream of?", 'บางที... ก็รู้นี่นา... อาจมีโอกาสนิดหน่อยที่นี่คือสิ่งที่\nสาวตัวน้อยต้องการกันก็ได้นะ?'),
    (23, 'fk68', '51_2200_113_0', "*gaps* M-My hammer! It's glowing!", '*อ๊ะ* ค-ค้อนของฉัน! มันกำลังส่องแสง!'),
    (24, 'fkv8', '51_3000_100_0', "It is really wet though so don't hit it\ntoo..", 'แต่มันมีน้ำอยู่มากเลยนะ เพราะฉะนั้นอย่าไปตีมันแรง...'),
    (25, 'fmkc', '51_4700_041_0', "Did... Did you just jump down her on\npurpose?", 'เธอ... เธอตั้งใจลงมาที่นี่จริง ๆ เหรอ?'),
    (26, 'fs6g', '52_0400_001_0', "I-It is kinda weird to be started at like\nthis... Just a bit.", 'ม-มันรู้สึกแปลก ๆ นิดหน่อยนะที่ถูกจ้องมอง\nแบบนี้... นิดหน่อยน่ะ'),
    (27, 'fti8', '52_1800_009_0', "More importantly, you shouldn't push\nyourself. It's important to get a good\nnights sleep. Go, log and rest. Got it?", 'ที่สำคัญกว่านั้น เธอไม่ควรหักโหมนะ\nการนอนหลับพักผ่อนเป็นเรื่องสำคัญมาก\nออกจากระบบแล้วไปพักผ่อนซะ เข้าใจไหม?'),
    (28, 'fuqs', '52_3100_003_0', "Hehehe... And I'm willing to be you have\nan exaggerated view of my talents.", 'ฮิฮิฮิ... และฉันว่าเธอคงมองความสามารถของฉัน\nเกินจริงไปหน่อยแล้วล่ะ'),
    (29, 'g350', '52_7520_037_0', "Um, your...ch--", 'เอ่อ... หน-หน้า--'),
    (30, 'g350', '52_7520_038_0', "My ch...?", 'หน้า... ของฉัน?'),
    (31, 'g350', '52_7520_039_0', "...est.", '...อกน่ะ'),
    (32, 'g350', '52_7520_040_0', "...est?", '...อกเหรอ?')
]

# Verify all translations encode with 0 missing clusters
print("Verifying Thai CJK encoding for all 32 translations...")
encoded_list = []
for no, fn, tag, en, th in translations:
    cjk = encode_thai_to_cjk(th)
    encoded_list.append((no, fn, tag, en, th, cjk))
print("100% verified! All 32 translations cleanly encoded.\n")

# Create backup folder
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = os.path.join(backup_base, f"scripts_{ts}")
os.makedirs(backup_dir, exist_ok=True)
print(f"Created backup folder: {backup_dir}")

# Group translations by file
by_file = {}
for item in encoded_list:
    by_file.setdefault(item[1], []).append(item)

# Process each script file
modified_files = 0
pristine_backup = os.path.join(backup_base, "scripts_20261013_170200")
for fn, items in by_file.items():
    fp = os.path.join(script_dir, fn)
    # Restore from pristine backup if available
    pristine_file = os.path.join(pristine_backup, fn)
    if os.path.exists(pristine_file):
        shutil.copy2(pristine_file, fp)
    
    with open(fp, "rb") as f:
        data = bytearray(f.read())
    
    str_start, str_len = struct.unpack_from("<II", data, 8)
    
    for no, _, tag, en, th, cjk in items:
        en_bytes = en.encode("utf-8")
        pos = data.find(en_bytes, str_start)
        if pos == -1:
            raise RuntimeError(f"Target English string not found in {fn}: {en!r}")
        
        rel_off = pos - str_start
        
        # Find bytecode pointer pointing to this relative offset
        ptr_found = None
        for i in range(0, str_start - 3, 2):
            if struct.unpack_from("<I", data, i)[0] == rel_off:
                ptr_found = i
                break
        
        if ptr_found is None:
            raise RuntimeError(f"Pointer to offset 0x{rel_off:X} not found in {fn}!")
        
        # Encode CJK string + null terminator
        cjk_bytes = cjk.encode("utf-8") + b"\x00"
        
        # Append to end of file
        new_rel_off = len(data) - str_start
        data.extend(cjk_bytes)
        
        # Update pointer in bytecode
        struct.pack_into("<I", data, ptr_found, new_rel_off)
    
    # Pad file to 4-byte alignment if needed
    pad = (4 - (len(data) % 4)) % 4
    if pad:
        data.extend(b"\x00" * pad)
    
    # Update string table length in header at offset 0x0C
    new_str_len = len(data) - str_start
    struct.pack_into("<I", data, 12, new_str_len)
    
    with open(fp, "wb") as f:
        f.write(data)
    
    modified_files += 1
    print(f"Patched {fn}: injected {len(items)} strings (new size: {len(data):,} bytes)")

print(f"\nSuccessfully patched all {modified_files} script files!")

# Update untranslated_scripts_32.csv with Thai translations
with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ลำดับ (No.)", "ไฟล์สคริปต์ (Script File)", "รหัสบทพูด (Tag)", "ข้อความอังกฤษต้นฉบับ (Target English)", "คำแปลภาษาไทย (Thai Translation)"])
    for no, fn, tag, en, th in translations:
        w.writerow([no, fn, tag, en, th])
print(f"Updated CSV file: {csv_path}")
