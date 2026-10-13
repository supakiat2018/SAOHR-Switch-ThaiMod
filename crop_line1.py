from PIL import Image
import struct

atlas = Image.open('pc_thai_font_full_atlas.png')

with open(r'extracted_pc_thai_usa\font\font00.fgen.phyre', 'rb') as f:
    pc_data = f.read()

pos = pc_data.find(b'font00_usa.fgen#BitmapFont\x00')
base = pos + len(b'font00_usa.fgen#BitmapFont\x00') + 18

line1 = '嬖峪伶仰伸冦伸乏'
for i, ch in enumerate(line1):
    cid = ord(ch)
    # find entry for cid
    for idx in range(7527):
        entry = pc_data[base + idx*45 : base + (idx+1)*45]
        code = struct.unpack_from('<H', entry, 7)[0]
        if code == cid:
            x = struct.unpack_from('<f', entry, 19)[0]
            y = struct.unpack_from('<f', entry, 23)[0]
            w = struct.unpack_from('<f', entry, 27)[0]
            h = struct.unpack_from('<f', entry, 31)[0]
            crop = atlas.crop((int(x), int(y), int(x+w), int(y+h)))
            crop.resize((int(w)*4, int(h)*4), Image.NEAREST).save(f'char_{i}_{hex(cid)}.png')
            print(f'char {i}: {ch} (0x{cid:04x}) -> x={x:.1f}, y={y:.1f}, w={w:.1f}, h={h:.1f}')
            break
