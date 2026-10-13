"""
Prepares staging folder and packs usa.cpk for Nintendo Switch Atmosphere LayeredFS.
"""

import os
import shutil
import subprocess

def main():
    base_dir = r"C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp"
    switch_orig = os.path.join(base_dir, "extracted_switch_usa")
    pc_thai = os.path.join(base_dir, "extracted_pc_thai_usa")
    new_font = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\romfs\pkg_patch\usa\font\font00.fgen.phyre")
    
    # We name staging folder 'usa' so YACpkTool produces 'usa.cpk' directly!
    staging_dir = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\build_staging\usa")
    expected_cpk = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\build_staging\usa.cpk")
    
    yacpk_tool = os.path.join(base_dir, r"YACpkTool\YACpkTool.exe")
    
    final_dir = os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\atmosphere\contents\0100EC400D54E000\romfs\pkg")
    os.makedirs(final_dir, exist_ok=True)
    final_cpk = os.path.join(final_dir, "usa.cpk")

    print("Step 1: Preparing staging folder...")
    if os.path.exists(staging_dir):
        print("Cleaning previous staging folder...")
        shutil.rmtree(staging_dir)
        
    print(f"Copying base Switch files from {switch_orig} to staging...")
    shutil.copytree(switch_orig, staging_dir)

    print(f"Overlaying Thai translations from {pc_thai}...")
    overlaid = 0
    for root, dirs, files in os.walk(pc_thai):
        for f in files:
            # Skip old PC font if encountered
            if f == "font00.fgen.phyre":
                continue
            src_file = os.path.join(root, f)
            rel_path = os.path.relpath(src_file, pc_thai)
            dst_file = os.path.join(staging_dir, rel_path)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)
            overlaid += 1
    print(f"Overlaid {overlaid} Thai translation files into staging.")

    print(f"Injecting new Switch Thai font: {new_font}...")
    target_font = os.path.join(staging_dir, "font", "font00.fgen.phyre")
    os.makedirs(os.path.dirname(target_font), exist_ok=True)
    shutil.copy2(new_font, target_font)
    print("Font injected successfully.")

    # Count files in staging
    total_files = sum(len(files) for _, _, files in os.walk(staging_dir))
    print(f"Total files ready in staging: {total_files}")

    print("\nStep 2: Building usa.cpk using native CriCpkMaker...")
    ps_cmd = [
        r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe",
        "-ExecutionPolicy", "Bypass",
        "-File", os.path.join(base_dir, r"SAOHR_Switch_Thai_Mod\tools\build_switch_cpk_direct.ps1")
    ]
    subprocess.run(ps_cmd, check=True)
    
    # Clean staging after successful build
    if os.path.exists(staging_dir):
        print("Cleaning staging folder to save space...")
        shutil.rmtree(staging_dir)
        
    print(f"\nSUCCESS! Rebuilt LayeredFS usa.cpk at: {final_cpk}")
    print(f"Size: {os.path.getsize(final_cpk):,} bytes")

if __name__ == "__main__":
    main()
