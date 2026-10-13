from PIL import Image
import struct

atlas = Image.open('pc_thai_font_full_atlas.png')

with open(r'extracted_pc_thai_usa\font\font00.fgen.phyre', 'rb') as f:
    pc_data = f.read()

pos = pc_data.find(b'font00_usa.fgen#BitmapFont\x00')
base = pos + len(b'font00_usa.fgen#BitmapFont\x00') + 14
count = struct.unpack_from('<I', pc_data, base)[0]
start = base + 4

# Map character code to (x, y, w, h)
glyph_map = {}
for i in range(count):
    entry = pc_data[start + i*45 : start + (i+1)*45]
    char_code = struct.unpack_from('<H', entry, 6)[0]
    u = struct.unpack_from('<f', entry, 19)[0]
    v = struct.unpack_from('<f', entry, 23)[0]
    w = struct.unpack_from('<f', entry, 27)[0]
    h = struct.unpack_from('<f', entry, 31)[0]
    glyph_map[char_code] = (u, v, w, h)

# Test strings:
# '兢尻仡伸兒'
# '丐垳仝'
test_chars = '兢尻仡伸兒丐垳仝'
cropped_imgs = []
for ch in test_chars:
    code = ord(ch)
    if code in glyph_map:
        x, y, w, h = glyph_map[code]
        print(f'{ch} (0x{code:04x}): x={x}, y={y}, w={w}, h={h}')
        cropped = atlas.crop((int(x), int(y), int(x+w), int(y+h)))
        cropped_imgs.append((ch, cropped))
    else:
        print(f'{ch} not found in font!')

# Assemble into a strip
total_w = sum(im.width + 5 for _, im in cropped_imgs)
max_h = max(im.height for _, im in cropped_imgs)
strip = Image.new('L', (total_w, max_h), color=0)
cur_x = 0
for ch, im in cropped_imgs:
    strip.paste(im, (cur_x, 0))
    cur_x += im.width + 5

strip.resize((total_w*3, max_h*3), Image.NEAREST).save('cjk_test_crop_zoomed.png')
print('Saved cjk_test_crop_zoomed.png')
