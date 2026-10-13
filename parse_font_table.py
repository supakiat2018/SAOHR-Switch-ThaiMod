import struct

with open(r'extracted_pc_thai_usa\font\font00.fgen.phyre', 'rb') as f:
    data = f.read()

pos = data.find(b'font00_usa.fgen#BitmapFont\x00')
base = pos + len(b'font00_usa.fgen#BitmapFont\x00') + 14
count = struct.unpack_from('<I', data, base)[0]
start = base + 4

print(f'Total character entries: {count}')
for i in range(1, 20):
    entry = data[start + i*45 : start + (i+1)*45]
    # Check all possible offsets for char code
    u16_0 = struct.unpack_from('<H', entry, 0)[0]
    u16_6 = struct.unpack_from('<H', entry, 6)[0]
    u16_7 = struct.unpack_from('<H', entry, 7)[0]
    print(f'Entry {i:2d}: @0=0x{u16_0:04x}, @6=0x{u16_6:04x} ({chr(u16_6) if u16_6 < 128 else "?"}), @7=0x{u16_7:04x} ({chr(u16_7) if u16_7 < 128 else "?"})')
