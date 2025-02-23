# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin
from colors import BLUE, PURPLE, BLACK
import time
from font8x8 import font8x8_basic

# Create a NeoPixel matrix with 64 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 64)
rep_between_letters = [
    [BLACK],
    [BLACK],
    [BLACK],
    [BLACK],
    [BLACK],
    [BLACK],
    [BLACK],
    [BLACK],
]


def get_bitmap_representation(letter: str):
    letter = font8x8_basic[ord(letter)]
    mask = [~element & 0xFF for element in letter]
    binary_letter = [bin(item) for item in mask]
    binary_letter_list = [
        [BLACK if bit == "1" else BLUE for bit in binary[2:]][::-1]
        for binary in binary_letter
    ]
    return binary_letter_list


def create_banner(string: str):
    scrolling_text = []
    new = [[], [], [], [], [], [], [], []]
    new_flat = [[], [], [], [], [], [], [], []]
    for element in string:
        rep_letter = get_bitmap_representation(element)
        scrolling_text.append(rep_letter)
        scrolling_text.append(rep_between_letters)

    for i, element in enumerate(scrolling_text):
        for j, row in enumerate(element):
            new[j].append(row)

    for i, element in enumerate(new):
        for subelement in element:
            for bit in subelement:
                new_flat[i].append(bit)
    return new_flat


def slice_banner(lst, pos):
    buffer_ = [[], [], [], [], [], [], [], []]
    for i, element in enumerate(lst):
        buffer_[i] = element[pos : pos + 8]
    return buffer_


my_phrase = "HP ower"
new_flat = create_banner(my_phrase)

for i in range(50):
    led_strip.fill_custom(
        [bit for sublist in slice_banner(new_flat, i) for bit in sublist]
    )
    time.sleep(0.1)
