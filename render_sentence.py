from PIL import Image
import struct

atlas = Image.open('pc_thai_font_full_atlas.png')

with open(r'extracted_pc_thai_usa\font\font00.fgen.phyre', 'rb') as f:
    pc_data = f.read()

pos = pc_data.find(b'font00_usa.fgen#BitmapFont\x00')
base = pos + len(b'font00_usa.fgen#BitmapFont\x00') + 18

# Build code -> (x, y, w, h)
code_to_glyph = {}
for i in range(7527):
    entry = pc_data[base + i*45 : base + (i+1)*45]
    cid = struct.unpack_from('<H', entry, 7)[0]
    x = struct.unpack_from('<f', entry, 19)[0]
    y = struct.unpack_from('<f', entry, 23)[0]
    w = struct.unpack_from('<f', entry, 27)[0]
    h = struct.unpack_from('<f', entry, 31)[0]
    code_to_glyph[cid] = (x, y, w, h)

test_sentence = '携攷嶬恆撥幤嶬攷抦暈挽打悴撥掀攷忰攷拷'
cropped_list = []
for ch in test_sentence:
    cid = ord(ch)
    if cid in code_to_glyph:
        x, y, w, h = code_to_glyph[cid]
        # crop with safe margin
        crop = atlas.crop((int(x), int(y), int(x + max(w, 1)), int(y + max(h, 1))))
        cropped_list.append((ch, crop, w, h))
        print(f'{ch} (0x{cid:04x}): x={x:.1f}, y={y:.1f}, w={w:.1f}, h={h:.1f}')
    else:
        print(f'{ch} (0x{cid:04x}) not found')

# Stitch together into a line
total_w = sum(max(int(w), 5) + 3 for _, _, w, _ in cropped_list)
max_h = max(int(h) for _, _, _, h in cropped_list) if cropped_list else 20
line_img = Image.new('L', (total_w, max_h + 10), color=0)

cur_x = 0
for ch, crop, w, h in cropped_list:
    line_img.paste(crop, (cur_x, 5))
    cur_x += max(int(w), 5) + 3

line_img.resize((total_w * 3, (max_h + 10) * 3), Image.NEAREST).save('sentence_1_crop.png')
print('Saved sentence_1_crop.png')
