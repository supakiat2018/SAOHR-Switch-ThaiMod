from PIL import Image
import numpy as np

with open(r'extracted_pc_thai_usa\font\font00.fgen.phyre', 'rb') as f:
    f.seek(342250)
    raw = f.read(7553024)

print('Raw texture length:', len(raw))

# In PhyreEngine PC D3D11:
# Let's see: Is it 2048x2048?
# 2048 * 2048 = 4194304 bytes (1 byte per pixel: L8 / A8 / R8)
# If total is 7553024, maybe there's a header or multiple mips?
# Let's try reading 2048*2048 at various offsets (0, 128, 256, 512, 1024, 2048, 4096)
for offset in [0, 64, 128, 256, 512, 1024, 2048, 4096]:
    sub = raw[offset:offset + 2048*2048]
    if len(sub) == 2048*2048:
        arr = np.frombuffer(sub, dtype=np.uint8)
        nz = np.count_nonzero(arr)
        print(f'Offset {offset}: non-zero pixels = {nz}')
        if nz > 50000:
            img = Image.frombytes('L', (2048, 2048), sub)
            img.save(f'pc_font_test_off_{offset}.png')
            print(f'Saved pc_font_test_off_{offset}.png')
            break
