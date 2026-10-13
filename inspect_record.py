import struct

with open(r'extracted_pc_thai_usa\font\font00.fgen.phyre', 'rb') as f:
    data = f.read()

pos = data.find(b'font00_usa.fgen#BitmapFont\x00')
base = pos + len(b'font00_usa.fgen#BitmapFont\x00') + 14
start = base + 4

entry = data[start + 1*45 : start + 2*45]
print("Hex:", entry.hex())
# Byte 7-8 is character code (0x0021 = '!')
# What are bytes 0..6?
# What are bytes 9..44?
# Let's inspect float values across the entry:
for o in range(0, 45 - 4, 4):
    f_val = struct.unpack_from('<f', entry, o)[0]
    i_val = struct.unpack_from('<I', entry, o)[0]
    print(f'Offset +{o:2d}: int={i_val:10d} (0x{i_val:08x}), float={f_val:12.4f}')
