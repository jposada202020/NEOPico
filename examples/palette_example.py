# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import palette
from neopixel import NEOPIXEL
from machine import Pin
from palette import HarmonyType

# Create a NeoPixel ring with 30 pixels connected to pin 15
ring = NEOPIXEL(Pin(15), 30)

# Generate a palette of 8 colors with a neutral temperature and a complementary harmony
colors_complementary = palette.generate_palette(
    temperature="neutral", harmony_type=HarmonyType.COMPLEMENTARY, seeding=1999
)

# Generate a palette of 8 colors with a neutral temperature and a triadic harmony
colors_triadic = palette.generate_palette(
    temperature="neutral", harmony_type=HarmonyType.TRIADIC, seeding=1999
)

# Generate a palette of 8 colors with a neutral temperature and an analogous harmony
colors_analogous = palette.generate_palette(
    temperature="neutral", harmony_type=HarmonyType.ANALOGOUS, seeding=1999
)

# Blend the colors and create a list of 8 colors
blended_complementary = palette.blend_colors(colors_complementary, 30)
blended_triadic = palette.blend_colors(colors_triadic, 30)
blended_analogous = palette.blend_colors(colors_analogous, 30)

# Display the blended colors
ring.fill_custom(blended_complementary)
ring.fill_all(color=(0, 0, 0))
ring.fill_custom(blended_triadic)
ring.fill_all(color=(0, 0, 0))
ring.fill_custom(blended_analogous)
ring.fill_all(color=(0, 0, 0))
