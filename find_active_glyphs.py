import struct

with open(r'extracted_pc_thai_usa\font\font00.fgen.phyre', 'rb') as f:
    pc_data = f.read()

pos = pc_data.find(b'font00_usa.fgen#BitmapFont\x00')
base = pos + len(b'font00_usa.fgen#BitmapFont\x00') + 14
count = struct.unpack_from('<I', pc_data, base)[0]
start = base + 4

active_glyphs = []
for i in range(count):
    entry = pc_data[start + i*45 : start + (i+1)*45]
    char_code = struct.unpack_from('<H', entry, 7)[0]
    
    # Let's inspect float values across different byte alignments
    w = struct.unpack_from('<f', entry, 29)[0]
    h = struct.unpack_from('<f', entry, 33)[0]
    if w > 1.0 and h > 1.0:
        active_glyphs.append((i, char_code, chr(char_code) if char_code < 0x10000 else '?', w, h))

print(f'Total active glyphs with w > 1 and h > 1: {len(active_glyphs)}')
print('Sample 20 active glyphs (including CJK):')
for g in active_glyphs[100:120]:
    print(f'  entry #{g[0]:4d}: code=0x{g[1]:04x} ({g[2]}), w={g[3]:.1f}, h={g[4]:.1f}')
