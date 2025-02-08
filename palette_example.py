import palette
from neopixel import NEOPIXEL
from machine import Pin

# Example of generating a palette and blending the colors and displaying them

ring = NEOPIXEL(Pin(15), 16)
colors = palette.generate_palette(seeding=100000)

# Blend the colors and create a list of 16 colors
blended = palette.blend_colors(colors, 16)

# Display the blended colors
ring.fill_custom(blended)
ring.fill_all(color=(0, 0, 0))
