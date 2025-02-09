# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya, DJDevon
#
# SPDX-License-Identifier: MIT

import palette
import time
from neopixel import NEOPIXEL
from machine import Pin

# Example of generating a palette and blending the colors and displaying them

ring = NEOPIXEL(Pin(15), 8)
color1 = (90, 180, 27)  # Example color 1
color2 = (111, 123, 154)  # Example color 2
color3 = (231, 45, 120)  # Example color 3
base_color = (128, 0, 0)  # Example base color
stretch = 350  # Example stretch factor


colors = palette.generate_three_color_palette(color1, color2, color3, 8)
colors_pastel = palette.generate_three_color_pastel_palette(
    color1, color2, color3, 8
)
color_palette = palette.generate_color_palette(base_color, stretch)
color_palette_pastel = palette.generate_pastel_palette(base_color, stretch)
ring.fill_custom(colors)
ring.fill_all(color=(0, 0, 0))
ring.fill_custom(colors_pastel)
ring.fill_all(color=(0, 0, 0))
ring.fill_custom(color_palette)
ring.fill_all(color=(0, 0, 0))
ring.fill_custom(color_palette_pastel)
ring.fill_all(color=(0, 0, 0))
