# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

"""

`effects`
================================================================================

Create and control LED effects.

* Author: Jose D. Montoya


"""

import time
from random import choice
from colors import BLACK, YELLOW, RED, PURPLE, CYAN, ORANGE, ORANGEYELLOW, BLUE
from neopixel import NEOPIXEL
from palette import hsv_to_rgb
import math


def pacman_effect(led_object, neopixel_list, num_leds, duration: int = 15):
    """
    PACMAN ANIMATION Adapted from https://github.com/wled-dev/WLED/pull/4536 # by BobLoeffler68
    MIT LICENSE

    :param led_object: led object
    :param neopixel_list: list of neopixel colors
    :param int num_leds: number of leds.
    :param int duration: duration in seconds. Default is 15 seconds
    """

    direction = 1
    black_dir = -1
    if num_leds > 150:
        start_blinking_ghosts = num_leds // 4
    else:
        start_blinking_ghosts = num_leds // 3

    pacman = [YELLOW, 10]
    ghosts_original = [[RED, 6], [PURPLE, 4], [CYAN, 2], [ORANGE, 0]]
    ghosts = [[RED, 6], [PURPLE, 4], [CYAN, 2], [ORANGE, 0]]
    power_pellet = [ORANGEYELLOW, num_leds - 1]
    neopixel_list[power_pellet[1]] = power_pellet[0]
    NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
    ghost_timer = time.ticks_ms()
    flag = "beep"

    start_time = time.time()

    while time.time() - start_time < duration:

        delta = time.ticks_ms() - ghost_timer
        if delta > 250:
            if power_pellet[0] == ORANGEYELLOW:
                power_pellet[0] = BLACK
            else:
                power_pellet[0] = ORANGEYELLOW

            neopixel_list[power_pellet[1]] = power_pellet[0]

            ghost_timer = time.ticks_ms()

        if pacman[1] >= num_leds - 2:
            direction = direction * -1
            black_dir = black_dir * -1
            for ghost in ghosts:
                ghost[0] = BLUE

        neopixel_list[pacman[1]] = pacman[0]
        neopixel_list[pacman[1] + black_dir] = BLACK
        pacman[1] += direction

        if ghosts[3][1] <= start_blinking_ghosts and direction == -1:
            if flag == "beep":
                for i, ghost in enumerate(ghosts):
                    ghost[0] = BLACK
                flag = "bop"
            else:
                for i, ghost in enumerate(ghosts):
                    ghost[0] = ghosts_original[i][0]
                flag = "beep"

        for i, ghost in enumerate(ghosts):
            neopixel_list[ghost[1]] = ghost[0]
            neopixel_list[ghost[1] + black_dir] = BLACK
            ghost[1] += direction

        if ghosts[3][1] <= 0:
            direction = direction * -1
            black_dir = black_dir * -1
            for i, ghost in enumerate(ghosts):
                ghost[0] = ghosts_original[i][0]

        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        time.sleep(0.1)


def rainbow_cycle_effect(
    led_object,
    neopixel_list,
    num_leds,
    time_delta: float = 0.1,
    duration: int = 5,
) -> None:
    """
    Cycle through the rainbow colors.
    :param float time_delta: time delay between each color change: default 0.1 seconds
    :param int duration: duration in seconds: default 5 seconds
    :return: None
    """
    from rainbow import rainbow_colors

    rainbow_set = rainbow_colors

    start_time = time.time()
    while time.time() - start_time < duration:
        rainbow_set = rainbow_set[-1:] + rainbow_set[:-1]
        for i in range(num_leds):
            neopixel_list[i] = rainbow_set[i]
        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        time.sleep(time_delta)


def segment_effect(
    led_object,
    neopixel_list,
    num_leds,
    duration: int = 5,
    segment_length: int = 3,
    values: list = None,
):
    led_list = [BLACK for _ in range(num_leds)]

    led_segments = get_led_segments(led_list, segment_length)
    assigned_segments = assign_values_to_segments(led_segments, values)
    neopixel_list = flatten_segments(assigned_segments)

    start_time = time.time()

    while time.time() - start_time < duration:
        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        time.sleep(0.1)


def random_color(
    led_object, neopixel_list, num_leds: int = 8, duration: int = 5
):
    """
    Random color data for testing
    :param int num_leds: number of leds. Default is 8 leds
    :param int duration: duration in seconds. Default is 5 seconds
    """

    limits = range(0, 256)

    start_time = time.time()

    while time.time() - start_time < duration:
        neopixel_list = [
            (choice(limits), choice(limits), choice(limits))
            for _ in range(num_leds)
        ]
        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        time.sleep(0.1)


def twinkle_effect(
    led_object, palette_colors, neopixel_list, num_leds, duration: int = 5
):
    """
    Dummy data for testing.
    :param int duration: duration in seconds. Default is 5 seconds
    """

    start_time = time.time()

    while time.time() - start_time < duration:
        neopixel_list = [choice(palette_colors) for _ in range(num_leds)]
        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        time.sleep(0.1)


def get_led_segments(led_list, segment_length) -> list:
    segments = []
    for i in range(0, len(led_list), segment_length):
        segments.append(led_list[i : i + segment_length])
    return segments


def assign_values_to_segments(segments, values) -> list:
    assigned_segments = []
    for i, segment in enumerate(segments):
        if i < len(values):
            assigned_segment = [values[i]] * len(segment)
        else:
            assigned_segment = [BLACK] * len(segment)  # or some default value
        assigned_segments.append(assigned_segment)
    return assigned_segments


def flatten_segments(assigned_segments) -> list:
    return [led for segment in assigned_segments for led in segment]


def rgb255(color: list):
    """Set color of a specific LED.
    :param list color: RGB color values
    :return: RGB color values

    """

    return (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))


def rainbow_sine_effect(led_object, neopixel_list, num_leds, duration: int = 5):
    """
    Rainbow sine wave effect.
    :param led_object: led object
    :param neopixel_list: list of neopixel colors
    :param int duration: duration in seconds. Default is 5 seconds
    """
    animation = 0
    start_time = time.time()
    while time.time() - start_time < duration:
        for i in range(num_leds):
            hue = math.sin(animation + (i + 1) * 0.1)
            hue = (hue + 1) / 2
            color = rgb255(hsv_to_rgb(hue, 1.0, 1.0))
            neopixel_list[i] = color

        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        animation += 0.05
        time.sleep(0.05)
