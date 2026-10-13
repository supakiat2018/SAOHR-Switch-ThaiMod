"""
SAOHR Switch Thai Font Builder
Converts and builds font00.fgen.phyre and font01.fgen.phyre for Nintendo Switch.
"""

import os
import struct
import numpy as np
from PIL import Image

def get_gob_offset(x, y):
    """Tegra X1 Block Linear GOB address mapping (per NVIDIA Tegra X1 TRM)."""
    return (
        (x & 0x0F) |
        ((y & 1) << 4) |
        (((x >> 4) & 1) << 5) |
        (((y >> 1) & 1) << 6) |
        (((y >> 2) & 1) << 7) |
        (((x >> 5) & 1) << 8)
    )

def swizzle_tegra(linear_image_bytes, width, height, block_height=16):
    """
    Swizzles a linear 1-byte-per-pixel (L8 / R8) image into Tegra X1 Block Linear format.
    """
    gob_w = 64
    gob_h = 8
    gob_size = 512
    block_h = gob_h * block_height
    block_size = gob_size * block_height
    
    width_in_gobs = (width + gob_w - 1) // gob_w
    height_in_blocks = (height + block_h - 1) // block_h
    
    linear = np.frombuffer(linear_image_bytes, dtype=np.uint8).reshape((height, width))
    swizzled = bytearray(width_in_gobs * height_in_blocks * block_size)
    
    # Precompute GOB mapping
    gob_lut = np.zeros((8, 64), dtype=np.int32)
    for gy in range(8):
        for gx in range(64):
            gob_lut[gy, gx] = get_gob_offset(gx, gy)
            
    for by in range(height_in_blocks):
        for bx in range(width_in_gobs):
            for gy in range(block_height):
                block_start = (by * width_in_gobs + bx) * block_size + gy * gob_size
                y_base = by * block_h + gy * gob_h
                x_base = bx * gob_w
                
                for y_in_gob in range(8):
                    target_y = y_base + y_in_gob
                    if target_y >= height:
                        continue
                    line = np.zeros(64, dtype=np.uint8)
                    w_copy = min(gob_w, width - x_base)
                    if w_copy > 0:
                        line[:w_copy] = linear[target_y, x_base : x_base + w_copy]
                    indices = gob_lut[y_in_gob, :]
                    for i in range(64):
                        swizzled[block_start + indices[i]] = line[i]
                        
    return bytes(swizzled)

print("Tegra swizzle function loaded successfully.")
