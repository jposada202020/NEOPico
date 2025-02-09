# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya, DJDevon
#
# SPDX-License-Identifier: MIT

import palette
from neopixel import NEOPIXEL
from machine import Pin
from palette import HarmonyType

# Example of generating a palette and blending the colors and displaying them

ring = NEOPIXEL(Pin(15), 16)
colors_complementary = palette.generate_palette(
    temperature="neutral", harmony_type=HarmonyType.COMPLEMENTARY, seeding=1999
)
colors_triadic = palette.generate_palette(
    temperature="neutral", harmony_type=HarmonyType.TRIADIC, seeding=1999
)
colors_analogous = palette.generate_palette(
    temperature="neutral", harmony_type=HarmonyType.ANALOGOUS, seeding=1999
)
# Blend the colors and create a list of 16 colors
blended_complementary = palette.blend_colors(colors_complementary, 8)
blended_triadic = palette.blend_colors(colors_triadic, 8)
blended_analogous = palette.blend_colors(colors_analogous, 8)

# Display the blended colors
ring.fill_custom(blended_complementary)
ring.fill_all(color=(0, 0, 0))
ring.fill_custom(blended_triadic)
ring.fill_all(color=(0, 0, 0))
ring.fill_custom(blended_analogous)
ring.fill_all(color=(0, 0, 0))
