from PIL import Image

atlas = Image.open('pc_thai_font_full_atlas.png')

# 携 (0x643a): x=1410, y=3670, w=15, h=14
x, y, w, h = 1410, 3670, 15, 14
glyph = atlas.crop((x, y, x + w, y + h))
glyph.resize((w * 6, h * 6), Image.NEAREST).save('glyph_643a_zoomed.png')
print('Saved glyph_643a_zoomed.png')
