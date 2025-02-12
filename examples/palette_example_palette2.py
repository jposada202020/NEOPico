# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import palette
import time
from neopixel import NEOPIXEL
from machine import Pin

# Create a NeoPixel ring with 30 pixels connected to pin 15
ring = NEOPIXEL(Pin(15), 30)

# Define the colors to include in the palette
color1 = (90, 180, 27)  # Example color 1
color2 = (111, 123, 154)  # Example color 2
color3 = (231, 45, 120)  # Example color 3
base_color = (128, 0, 0)  # Example base color
stretch = 350  # Example stretch factor

# Generate the palettes
colors = palette.generate_three_color_palette(color1, color2, color3, 30)
colors_pastel = palette.generate_three_color_pastel_palette(
    color1, color2, color3, 30
)
color_palette = palette.generate_color_palette(base_color, stretch, 30)
color_palette_pastel = palette.generate_pastel_palette(base_color, stretch, 30)

# Display the palettes
ring.fill_custom(colors)
ring.fill_all(color=(0, 0, 0))
ring.fill_custom(colors_pastel)
ring.fill_all(color=(0, 0, 0))
ring.fill_custom(color_palette)
ring.fill_all(color=(0, 0, 0))
ring.fill_custom(color_palette_pastel)
ring.fill_all(color=(0, 0, 0))
