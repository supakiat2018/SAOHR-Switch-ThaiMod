import struct

with open(r'extracted_pc_thai_usa\font\font00.fgen.phyre', 'rb') as f:
    pc_data = f.read()
with open(r'extracted_switch_usa\font\font00.fgen.phyre', 'rb') as f:
    sw_data = f.read()

pos = pc_data.find(b'font00_usa.fgen#BitmapFont\x00')
base = pos + len(b'font00_usa.fgen#BitmapFont\x00') + 14
count = struct.unpack_from('<I', pc_data, base)[0]
start = base + 4

sw_pos = sw_data.find(b'font00_usa.fgen#BitmapFont\x00')
sw_base = sw_pos + len(b'font00_usa.fgen#BitmapFont\x00') + 14
sw_start = sw_base + 4

cjk_glyphs = []
for i in range(count):
    pc_entry = pc_data[start + i*45 : start + (i+1)*45]
    sw_entry = sw_data[sw_start + i*45 : sw_start + (i+1)*45]
    
    char_code = struct.unpack_from('<H', pc_entry, 7)[0]
    
    # Check if character code is in CJK range (0x4E00 - 0x9FFF or 0x3400 - 0x4DBF)
    is_cjk = (0x4e00 <= char_code <= 0x9fff) or (0x3400 <= char_code <= 0x4dbf)
    if is_cjk and pc_entry != sw_entry:
        u = struct.unpack_from('<f', pc_entry, 21)[0]
        v = struct.unpack_from('<f', pc_entry, 25)[0]
        w = struct.unpack_from('<f', pc_entry, 29)[0]
        h = struct.unpack_from('<f', pc_entry, 33)[0]
        adv = struct.unpack_from('<f', pc_entry, 41)[0]
        cjk_glyphs.append((i, char_code, chr(char_code), u, v, w, h, adv))

print(f'Total CJK modified entries in font: {len(cjk_glyphs)}')
print('First 15 CJK modified entries:')
for g in cjk_glyphs[:15]:
    print(f'  entry #{g[0]:4d}: code=0x{g[1]:04x} ({g[2]}), u={g[3]:.1f}, v={g[4]:.1f}, w={g[5]:.1f}, h={g[6]:.1f}, adv={g[7]:.1f}')
