import os
import re

pc_dir = r"extracted_pc_thai_usa"
sw_dir = r"extracted_switch_usa"

script_dir = os.path.join(pc_dir, "script", "script")
dialogues = []

# Scan every file in script/script
for fn in sorted(os.listdir(script_dir)):
    pc_path = os.path.join(script_dir, fn)
    sw_path = os.path.join(sw_dir, "script", "script", fn)
    if not os.path.isfile(pc_path) or not os.path.isfile(sw_path):
        continue
    
    with open(pc_path, "rb") as f1, open(sw_path, "rb") as f2:
        pc_raw = f1.read()
        sw_raw = f2.read()
    
    # Dialogue pattern in SAOHR script files:
    # \d+_\d+_\d+_\d+\x00<text>\x00
    # or tags followed by null-terminated string
    matches = re.findall(rb'(\d+_\d+_\d+_\d+)\x00([^\x00]+)\x00', pc_raw)
    for tag, txt in matches:
        try:
            s = txt.decode("utf-8")
        except:
            continue
        
        # Check if text contains CJK (which indicates it has been translated to Thai in SAOHR)
        has_cjk = any('\u4e00' <= c <= '\u9fff' for c in s)
        # Check if text contains English
        has_en = any('a' <= c <= 'z' or 'A' <= c <= 'Z' for c in s)
        
        if not has_cjk and has_en:
            # Also verify if this exact text exists in Switch original
            tag_str = tag.decode()
            dialogues.append({
                "file": fn,
                "tag": tag_str,
                "text": s.strip(),
                "len": len(s.strip())
            })

print(f"Total script files checked: {len(os.listdir(script_dir))}")
print(f"Total untranslated dialogue entries: {len(dialogues)}")

print("\n--- Listing ALL untranslated entries ---")
for i, d in enumerate(dialogues, 1):
    print(f"{i:2d}. [{d['file']} | {d['tag']}] {repr(d['text'])}")

# Check if there are any other scripts or files with English text in extracted_pc_thai_usa
print("\n--- Checking other subdirectories in extracted_pc_thai_usa ---")
other_candidates = []
for root, dirs, files in os.walk(pc_dir):
    rel = os.path.relpath(root, pc_dir)
    if rel == os.path.join("script", "script") or rel == "msg":
        continue
    for f in files:
        if f.endswith((".phyre", ".gtx", ".dds", ".png")):
            continue
        fp = os.path.join(root, f)
        sw_fp = os.path.join(sw_dir, rel, f)
        if not os.path.isfile(sw_fp):
            continue
        with open(fp, "rb") as f1, open(sw_fp, "rb") as f2:
            c1 = f1.read()
            c2 = f2.read()
        # Find dialogue pattern
        m2 = re.findall(rb'(\d+_\d+_\d+_\d+)\x00([^\x00]+)\x00', c1)
        for tag, txt in m2:
            try:
                s = txt.decode("utf-8")
                if not any('\u4e00' <= c <= '\u9fff' for c in s) and any('a' <= c <= 'z' for c in s):
                    other_candidates.append((os.path.join(rel, f), tag.decode(), s))
            except:
                pass

print(f"Other subdirectories untranslated: {len(other_candidates)}")
for item in other_candidates:
    print(" ", item)
