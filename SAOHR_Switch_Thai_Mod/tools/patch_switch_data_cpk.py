"""
Patches Switch data.cpk with the new font01.fgen.phyre (50px Thai UI font).
"""

import os
import shutil
import struct

def patch_data_cpk():
    base_dir = r"C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp"
    orig_data_cpk = os.path.join(base_dir, r"romfs\pkg\data.cpk")
    new_font01 = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\romfs\pkg_patch\data\font\font01.fgen.phyre")
    
    out_dir = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\atmosphere\contents\0100EC400D54E000\romfs\pkg")
    os.makedirs(out_dir, exist_ok=True)
    target_data_cpk = os.path.join(out_dir, "data.cpk")

    print(f"Step 1: Reading new font01 size from {new_font01}...")
    with open(new_font01, "rb") as f:
        font_bytes = f.read()
    new_size = len(font_bytes)
    print(f"New font01 size: {new_size:,} bytes")

    print(f"\nStep 2: Copying clean base data.cpk (13.18 GB) to Atmosphere LayeredFS folder...")
    print(f"Source: {orig_data_cpk}")
    print(f"Target: {target_data_cpk}")
    if os.path.exists(target_data_cpk):
        print("Existing target found, removing old file...")
        os.remove(target_data_cpk)
        
    shutil.copy2(orig_data_cpk, target_data_cpk)
    print("Copy completed successfully.")

    print("\nStep 3: Appending new font01 to target data.cpk...")
    with open(target_data_cpk, "r+b") as f:
        # Seek to end
        f.seek(0, os.SEEK_END)
        cur_end = f.tell()
        # Align to 2048
        align = 2048
        pad = (align - (cur_end % align)) % align
        if pad > 0:
            f.write(b"\x00" * pad)
            cur_end += pad
        
        append_offset = cur_end
        f.write(font_bytes)
        print(f"Appended font01 at offset: {append_offset:,} (0x{append_offset:x})")

        # Step 4: Update TOC entry in target data.cpk
        # Row 1599 for font/font01.fgen.phyre is at byte 46,907 in data.cpk
        # Row structure:
        # +0: DirName (4B)
        # +4: FileName (4B)
        # +8: FileSize (4B BE uint32)
        # +12: ExtractSize (4B BE uint32)
        # +16: FileOffset (8B BE uint64)
        # +24: ID (4B BE uint32)
        toc_row_pos = 46907
        f.seek(toc_row_pos + 8)
        # Write new FileSize (uint32 BE), ExtractSize (uint32 BE), FileOffset (uint64 BE)
        new_row_data = struct.pack(">IIQ", new_size, new_size, append_offset)
        f.write(new_row_data)
        print(f"Updated TOC Row 1599 at byte {toc_row_pos}: FileSize={new_size:,}, Offset={append_offset:,}")

    print("\nStep 5: Verifying patched data.cpk...")
    final_size = os.path.getsize(target_data_cpk)
    print(f"Patched data.cpk size: {final_size:,} bytes")
    print(f"SUCCESS! Created fully patched data.cpk for Atmosphere LayeredFS at:")
    print(f"  {target_data_cpk}")

if __name__ == "__main__":
    patch_data_cpk()
