import struct

with open(r'extracted_pc_thai_usa\font\font00.fgen.phyre', 'rb') as f:
    pc_data = f.read()

pos = pc_data.find(b'font00_usa.fgen#BitmapFont\x00')
base = pos + len(b'font00_usa.fgen#BitmapFont\x00') + 14
count = struct.unpack_from('<I', pc_data, base)[0]
start = base + 4

# Find 'A' (char code 0x0041 = 65)
for i in range(count):
    entry = pc_data[start + i*45 : start + (i+1)*45]
    char_code = struct.unpack_from('<H', entry, 7)[0]
    if char_code == ord('A'):
        print(f"Found 'A' at entry #{i}:")
        print("Hex:", entry.hex())
        # Print all possible 4-byte float values at each byte offset 0..41
        for o in range(42):
            f_val = struct.unpack_from('<f', entry, o)[0]
            if 0.5 <= abs(f_val) <= 4096.0:
                print(f"  byte offset +{o:2d}: float = {f_val}")
        break
