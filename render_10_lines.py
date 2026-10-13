from PIL import Image
import struct
import re

atlas = Image.open('pc_thai_font_full_atlas.png')

with open(r'extracted_pc_thai_usa\font\font00.fgen.phyre', 'rb') as f:
    pc_data = f.read()

pos = pc_data.find(b'font00_usa.fgen#BitmapFont\x00')
base = pos + len(b'font00_usa.fgen#BitmapFont\x00') + 18

code_to_glyph = {}
for i in range(7527):
    entry = pc_data[base + i*45 : base + (i+1)*45]
    cid = struct.unpack_from('<H', entry, 7)[0]
    x = struct.unpack_from('<f', entry, 19)[0]
    y = struct.unpack_from('<f', entry, 23)[0]
    w = struct.unpack_from('<f', entry, 27)[0]
    h = struct.unpack_from('<f', entry, 31)[0]
    code_to_glyph[cid] = (x, y, w, h)

with open(r'extracted_pc_thai_usa\script\script\09uo', 'rb') as f:
    script_data = f.read()

# Extract UTF-8 strings
raw_strings = [s.decode('utf-8', errors='ignore') for s in re.findall(b'[\x80-\xff]{2,}|[\x20-\x7e]{3,}', script_data)]
# filter to those with CJK
cjk_strings = [s for s in raw_strings if any(0x4e00 <= ord(c) <= 0x9fff or 0x3400 <= ord(c) <= 0x4dbf for c in s)]

print(f'Total CJK strings in 09uo: {len(cjk_strings)}')

# Render 10 lines into an image
line_imgs = []
for idx, s in enumerate(cjk_strings[:10]):
    crops = []
    for ch in s:
        cid = ord(ch)
        if cid in code_to_glyph:
            x, y, w, h = code_to_glyph[cid]
            crop = atlas.crop((int(x), int(y), int(x + max(w, 1)), int(y + max(h, 1))))
            crops.append((crop, max(int(w), 3)))
        elif ch == ' ':
            space = Image.new('L', (8, 20), color=0)
            crops.append((space, 8))
    
    if crops:
        lw = sum(w + 2 for _, w in crops)
        lh = max(im.height for im, _ in crops)
        lim = Image.new('L', (lw, lh + 6), color=0)
        cx = 0
        for im, w in crops:
            lim.paste(im, (cx, 3))
            cx += w + 2
        line_imgs.append(lim)

# Combine 10 lines
max_w = max(im.width for im in line_imgs)
total_h = sum(im.height + 6 for im in line_imgs)
comb = Image.new('L', (max_w, total_h), color=0)
cy = 5
for im in line_imgs:
    comb.paste(im, (0, cy))
    cy += im.height + 6

comb.resize((max_w * 2, total_h * 2), Image.NEAREST).save('ten_thai_lines_preview.png')
print('Saved ten_thai_lines_preview.png with', len(line_imgs), 'lines!')
