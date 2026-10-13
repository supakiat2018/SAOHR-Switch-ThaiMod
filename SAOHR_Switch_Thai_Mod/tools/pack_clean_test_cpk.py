"""
Pack Clean Test CPK
Builds usa.cpk with 100% clean Switch base files, NO font modifications,
and ONLY patches 'New Game' and its hover description with 'HAGKDSl' for testing.
"""

import os
import shutil
import subprocess

def main():
    base_dir = r"C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp"
    switch_orig = os.path.join(base_dir, "extracted_switch_usa")
    staging_dir = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\build_staging\usa")
    final_dir = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\atmosphere\contents\0100EC400D54E000\romfs\pkg")
    os.makedirs(final_dir, exist_ok=True)
    final_cpk = os.path.join(final_dir, "usa.cpk")
    ryujinx_cpk = r"C:\Users\Supakiat\AppData\Roaming\Ryujinx\mods\contents\0100ec400d54e000\MODTH\0100EC400D54E000\romfs\pkg\usa.cpk"
    ryujinx_data_cpk = r"C:\Users\Supakiat\AppData\Roaming\Ryujinx\mods\contents\0100ec400d54e000\MODTH\0100EC400D54E000\romfs\pkg\data.cpk"

    print("Step 1: Preparing staging from 100% CLEAN Switch files...")
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir)

    shutil.copytree(switch_orig, staging_dir)
    print("Copied clean Switch files to staging.")

    print("\nStep 2: Patching only the test string HAGKDSl...")
    msg_path = os.path.join(staging_dir, "msg", "localize_msg.dat")
    with open(msg_path, "rb") as f:
        data = bytearray(f.read())

    # 1. Menu item itself (12 bytes)
    # Original: b'New Game\x00\x00\x00\x00'
    assert data[461220:461232] == b"New Game\x00\x00\x00\x00"
    data[461220:461232] = b"HAGKDSl\x00\x00\x00\x00\x00"

    # 2. Hover description when pointing to New Game (20 bytes)
    # Original: b'Start a new game.\x00\x00\x00'
    assert data[461288:461308] == b"Start a new game.\x00\x00\x00"
    data[461288:461308] = b"New Game - HAGKDSl\x00\x00"

    with open(msg_path, "wb") as f:
        f.write(data)
    print("Patched both New Game button and hover description successfully!")

    print("\nStep 3: Packing clean test usa.cpk...")
    ps_cmd = [
        r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe",
        "-ExecutionPolicy", "Bypass",
        "-File", os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\tools\build_switch_cpk_direct.ps1")
    ]
    subprocess.run(ps_cmd, check=True)

    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir)

    print("\nStep 4: Deploying to Ryujinx...")
    os.makedirs(os.path.dirname(ryujinx_cpk), exist_ok=True)
    shutil.copy2(final_cpk, ryujinx_cpk)
    print(f"Copied usa.cpk ({os.path.getsize(ryujinx_cpk):,} bytes) to Ryujinx!")

    if os.path.exists(ryujinx_data_cpk):
        os.remove(ryujinx_data_cpk)
        print("Removed leftover data.cpk from Ryujinx to prevent conflicts.")

    print("\nSUCCESS! Clean test environment ready.")

if __name__ == "__main__":
    main()
