import struct

with open(r'extracted_pc_thai_usa\font\font00.fgen.phyre', 'rb') as f:
    pc_data = f.read()

pos = pc_data.find(b'font00_usa.fgen#BitmapFont\x00')
base = pos + len(b'font00_usa.fgen#BitmapFont\x00') + 14
count = struct.unpack_from('<I', pc_data, base)[0]
start = base + 4

cjk_entries = []
for i in range(count):
    entry = pc_data[start + i*45 : start + (i+1)*45]
    char_code = struct.unpack_from('<H', entry, 6)[0]
    
    if (0x4e00 <= char_code <= 0x9fff) or (0x3400 <= char_code <= 0x4dbf):
        u = struct.unpack_from('<f', entry, 19)[0]
        v = struct.unpack_from('<f', entry, 23)[0]
        w = struct.unpack_from('<f', entry, 27)[0]
        h = struct.unpack_from('<f', entry, 31)[0]
        adv = struct.unpack_from('<f', entry, 39)[0]
        if w > 0 and h > 0:
            cjk_entries.append((i, char_code, chr(char_code), u, v, w, h, adv))

print(f'Total CJK characters with valid glyph in PC font: {len(cjk_entries)}')
print('First 20 CJK entries with glyphs:')
for g in cjk_entries[:20]:
    print(f'  entry #{g[0]:4d}: code=0x{g[1]:04x} ({g[2]}), x={g[3]:.1f}, y={g[4]:.1f}, w={g[5]:.1f}, h={g[6]:.1f}, adv={g[7]:.1f}')
