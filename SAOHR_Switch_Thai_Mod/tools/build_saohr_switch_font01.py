"""
Builds Switch font01.fgen.phyre for SAOHR main menu UI.
"""

import os
import sys
import struct
from PIL import Image

sys.path.append(os.path.dirname(__file__))
from tegra_swizzle import swizzle_tegra

def build_switch_font01():
    base_dir = r"C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp"
    sw_template_path = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\extracted_switch_data\font\font01.fgen.phyre")
    pc_thai_path = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\extracted_pc_data\font\font01.fgen.phyre")
    atlas_path = os.path.join(base_dir, "pc_thai_font01_atlas.png")
    
    out_dir = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\romfs\pkg_patch\data\font")
    os.makedirs(out_dir, exist_ok=True)
    out_font_path = os.path.join(out_dir, "font01.fgen.phyre")

    print("Loading Switch template font01...")
    with open(sw_template_path, "rb") as f:
        sw_data = bytearray(f.read())

    print("Loading PC Thai font01...")
    with open(pc_thai_path, "rb") as f:
        pc_data = f.read()

    # Load 512x3560 texture
    print("Loading 512x3560 texture atlas for font01...")
    atlas = Image.open(atlas_path).convert("L")
    w, h = atlas.size
    print(f"Atlas size: {w} x {h}")

    print("Swizzling font01 texture to Tegra Block Linear...")
    swizzled_bytes = swizzle_tegra(atlas.tobytes(), w, h, block_height=16)
    print(f"Swizzled texture size: {len(swizzled_bytes)} bytes")

    # Read PC 2,796 glyph entries
    pc_table_start = 3439
    total_glyphs = 2796
    pc_entries = pc_data[pc_table_start : pc_table_start + total_glyphs * 45]

    # In Switch template:
    # 0..3594: header up to count
    # offset 3594: uint16 count (currently 199) -> change to 2796
    # offset 3598: old 199 entries (8,955 bytes) -> replace with 2,796 entries (125,820 bytes)
    sw_head = sw_data[:3594]
    
    # Update count in head
    count_bytes = struct.pack("<I", total_glyphs)

    # Let's see what is after the old 199 entries in Switch template:
    old_table_end = 3598 + 199 * 45 # = 12553
    # Texture starts at end of file minus 196608
    old_tex_size = 196608
    sw_middle = sw_data[old_table_end : len(sw_data) - old_tex_size]

    # Assemble new font01
    new_font_data = bytearray()
    new_font_data.extend(sw_head)
    new_font_data.extend(count_bytes)
    new_font_data.extend(pc_entries)
    new_font_data.extend(sw_middle)
    new_font_data.extend(swizzled_bytes)

    # Update header sizes:
    # Offset 56 (0x38): Array size
    array_size = total_glyphs * 45 + 95
    struct.pack_into("<I", new_font_data, 56, array_size)
    # Offset 76 (0x4c): Texture buffer size
    new_tex_size = len(swizzled_bytes)
    struct.pack_into("<I", new_font_data, 76, new_tex_size)
    
    # Update NVN texture descriptor in new_font_data
    tex_desc_sig = bytes([0x00, 0x09, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00])
    desc_idx = new_font_data.find(tex_desc_sig)
    if desc_idx != -1:
        struct.pack_into("<H", new_font_data, desc_idx + 13, h)
        struct.pack_into("<I", new_font_data, desc_idx + 23, new_tex_size)
        print(f"Updated font01 NVN descriptor at {desc_idx}: height={h}, size={new_tex_size}")

    with open(out_font_path, "wb") as f:
        f.write(new_font_data)

    print(f"Successfully generated Switch font01: {out_font_path}")
    print(f"Output file size: {len(new_font_data)} bytes")
    return out_font_path

if __name__ == "__main__":
    build_switch_font01()
