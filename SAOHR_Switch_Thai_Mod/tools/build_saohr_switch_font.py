"""
SAOHR Switch Font Generator
Builds Nintendo Switch compatible font00.fgen.phyre with Thai language support.
"""

import os
import sys
import struct
import numpy as np
from PIL import Image

sys.path.append(os.path.dirname(__file__))
from tegra_swizzle import swizzle_tegra

def build_switch_font00():
    base_dir = r"C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp"
    sw_template_path = os.path.join(base_dir, r"extracted_switch_usa\font\font00.fgen.phyre")
    pc_thai_path = os.path.join(base_dir, r"extracted_pc_thai_usa\font\font00.fgen.phyre")
    atlas_path = os.path.join(base_dir, "pc_thai_font_full_atlas.png")
    
    out_dir = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\romfs\pkg_patch\usa\font")
    os.makedirs(out_dir, exist_ok=True)
    out_font_path = os.path.join(out_dir, "font00.fgen.phyre")

    print("Loading Switch template font...")
    with open(sw_template_path, "rb") as f:
        sw_data = bytearray(f.read())

    print("Loading PC Thai font...")
    with open(pc_thai_path, "rb") as f:
        pc_data = f.read()

    # Find glyph table in both
    tag = b"font00_usa.fgen#BitmapFont\x00"
    pos_sw = sw_data.find(tag) + len(tag) + 18
    pos_pc = pc_data.find(tag) + len(tag) + 18

    # Update glyph table: copy all modified glyph entries (full 45 bytes) from PC to Switch
    updated_count = 0
    for i in range(7527):
        pc_entry = pc_data[pos_pc + i*45 : pos_pc + (i+1)*45]
        sw_entry = sw_data[pos_sw + i*45 : pos_sw + (i+1)*45]
        if pc_entry != sw_entry:
            # Copy complete 45-byte glyph entry (metrics, UVs, advance, and flags)
            sw_data[pos_sw + i*45 : pos_sw + (i+1)*45] = pc_entry
            updated_count += 1

    print(f"Updated {updated_count} full Thai glyph entries in Switch font table.")

    # Load atlas
    print("Loading texture atlas...")
    atlas = Image.open(atlas_path).convert("L")
    w, h = atlas.size
    print(f"Atlas size: {w} x {h}")

    # Swizzle texture for Switch Tegra NVN
    print("Swizzling texture to Tegra Block Linear format (2048 x 3688)...")
    swizzled_bytes = swizzle_tegra(atlas.tobytes(), w, h, block_height=16)
    print(f"Swizzled texture data size: {len(swizzled_bytes)} bytes.")

    # In Switch template, replace old texture data with new swizzled texture
    # Old Switch texture was 6,029,312 bytes at end of file
    old_tex_len = 6029312
    header_part = sw_data[: len(sw_data) - old_tex_len]
    
    # Update texture height and size in NVN texture descriptor
    # Width is 2048 (0x800), Height is 3688 (0xE68), Size is 7,602,176
    new_tex_size = len(swizzled_bytes)
    struct.pack_into("<I", header_part, 76, new_tex_size)
    struct.pack_into("<H", header_part, 342343, h)
    struct.pack_into("<I", header_part, 342351, new_tex_size)
    print(f"Updated NVN texture descriptor: height={h}, size={new_tex_size}")
    
    # Write output
    with open(out_font_path, "wb") as f:
        f.write(header_part)
        f.write(swizzled_bytes)

    print(f"Successfully generated Switch Thai font: {out_font_path}")
    print(f"Output file size: {os.path.getsize(out_font_path)} bytes.")
    return out_font_path

if __name__ == "__main__":
    build_switch_font00()
