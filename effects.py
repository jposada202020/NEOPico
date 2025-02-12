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
import random


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

    # TODO: expose the number of colors in the palette
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

    # TODO: Example of how to use this function
    # TODO: Work on logic to assign animations to segments

    led_list = [BLACK for _ in range(num_leds)]

    led_segments = get_led_segments(led_list, segment_length)
    assigned_segments = assign_values_to_segments(led_segments, values)
    neopixel_list = flatten_segments(assigned_segments)

    start_time = time.time()

    while time.time() - start_time < duration:
        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        time.sleep(0.1)


def segment_animated_effect(
    led_object,
    neopixel_list,
    num_leds,
    duration: int = 5,
    segment_length: int = 3,
    values: list = None,
    animation=None,
):

    # TODO: Example of how to use this function
    # TODO: Work on logic to assign animations to segments

    led_list = [BLACK for _ in range(num_leds)]

    led_segments = get_led_segments(led_list, segment_length)
    print(neopixel_list)
    random_color(led_object, neopixel_list, 3, duration)

    # assigned_segments = assign_values_to_segments(led_segments, values)
    # neopixel_list = flatten_segments(assigned_segments)

    # start_time = time.time()

    # while time.time() - start_time < duration:
    #     NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
    #     time.sleep(0.1)


def random_color(
    led_object,
    neopixel_list,
    start: int = 0,
    num_leds: int = 8,
    duration: int = 5,
):
    """
    Random color data for testing
    :param int num_leds: number of leds. Default is 8 leds
    :param int duration: duration in seconds. Default is 5 seconds
    """

    # TODO: expose the number of colors in the palette
    # TODO: expose the animation speed
    # TODO: expose the color limits

    limits = range(0, 256)

    start_time = time.time()
    print(neopixel_list)
    while time.time() - start_time < duration:

        for i in range(start, num_leds):
            neopixel_list[i] = (choice(limits), choice(limits), choice(limits))
        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        time.sleep(0.1)


def twinkle_effect(
    led_object, palette_colors, neopixel_list, num_leds, duration: int = 5
):
    """
    Dummy data for testing.
    :param int duration: duration in seconds. Default is 5 seconds
    """
    # TODO: expose the number of colors in the palette
    # TODO: expose the animation speed

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
    # TODO: expose animation speed

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


def white_wave_effect(led_object, neopixel_list, num_leds, duration: int = 5):
    """
    White wave effect.
    :param led_object: led object
    :param neopixel_list: list of neopixel colors
    :param int duration: duration in seconds. Default is 5 seconds
    """
    # TODO: expose fade value
    # TODO: expose animation speed
    # TODO: expose color values based on H.
    # TODO: verify changes in Saturation

    # Animation variables
    animation = 0
    fade_animation = 0
    # Start time
    start_time = time.time()
    while time.time() - start_time < duration:
        # Calculate fade effect using sine wave
        fade_effect = (math.sin(fade_animation) + 1) / 2
        # Set global brightness based on fade effect
        led_object.brightness = fade_effect
        for i in range(num_leds):
            # Calculate brightness for each LED using sine wave
            brightness = math.sin(animation + i * 0.3)
            brightness = (brightness + 1) / 2

            color = rgb255(hsv_to_rgb(0.0, 0.0, brightness))
            neopixel_list[i] = color

        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        # Increment animation variables
        animation += 0.08
        fade_animation += 0.08
        # Small delay to control the speed of the animation
        time.sleep(0.01)


def white_wave_color_effect(
    led_object, neopixel_list, num_leds, duration: int = 5
):
    """
    White wave effect.
    :param led_object: led object
    :param neopixel_list: list of neopixel colors
    :param int duration: duration in seconds. Default is 5 seconds
    """
    # Animation variables
    # TODO: Expose the saturation max and min values
    # TODO: Expose the animation speed
    # TODO: Expose color values based on H.
    animation = 0

    # Start time
    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(num_leds):
            # Calculate brightness for each LED using sine wave
            saturation = math.sin(animation + i * 0.04)
            saturation = (saturation + 1) / 2
            saturation *= 255
            saturation = max(saturation, 30)
            saturation = saturation / 255

            color = rgb255(hsv_to_rgb(0.0, saturation, 1.0))
            neopixel_list[i] = color

        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        # Increment animation variables
        animation += 0.2

        # Small delay to control the speed of the animation
        time.sleep(0.01)


def lerp_effect(led_object, neopixel_list, num_leds, duration: int = 5):
    """
    Linear interpolation effect.
    :param led_object: led object
    :param neopixel_list: list of neopixel colors
    :param int duration: duration in seconds. Default is 5 seconds
    """
    from functions import lerp8by8

    # TODO: give the user the option to select the base colors or select the colors from a palette

    animation = 0
    # Start time

    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(num_leds):
            # Calculate brightness for each LED using sine wave
            interpolation = math.sin(animation + i * 0.5)
            interpolation = (interpolation + 1) / 2
            interpolation *= 255

            color1 = (255, 216, 0)
            color2 = (0, 150, 255)

            r = lerp8by8(color1[0], color2[0], int(interpolation))
            g = lerp8by8(color1[1], color2[1], int(interpolation))
            b = lerp8by8(color1[2], color2[2], int(interpolation))

            neopixel_list[i] = (r, g, b)

        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        # Increment animation variables
        animation += 0.1

        # Small delay to control the speed of the animation
        time.sleep(0.01)


def lerp_phase_effect(led_object, neopixel_list, num_leds, duration: int = 5):
    """
    Linear interpolation phase effect.
    :param led_object: led object
    :param neopixel_list: list of neopixel colors
    :param int duration: duration in seconds. Default is 5 seconds
    """
    from functions import lerp8by8

    # TODO: give the user the option to select the base colors or select the colors from a palette
    # TODO: expose the animation speed
    # TODO: choose random colors
    # TODO: expose the number of colors in the palette
    # TODO: expose the color limits

    animation = 0
    # Start time

    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(num_leds):
            # Calculate brightness for each LED using sine wave
            interpolation = math.sin(i * 0.2)
            interpolation *= 127

            phase = math.sin(animation * 1.5)

            interpolation *= phase
            interpolation += 127

            color1 = (255, 0, 0)
            color2 = (0, 0, 255)

            r = lerp8by8(color1[0], color2[0], int(interpolation))
            g = lerp8by8(color1[1], color2[1], int(interpolation))
            b = lerp8by8(color1[2], color2[2], int(interpolation))

            neopixel_list[i] = (r, g, b)

        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        # Increment animation variables
        animation += 0.1

        # Small delay to control the speed of the animation
        time.sleep(0.01)


def fadein_fadeout_random_color_effect(
    led_object, neopixel_list, num_leds, duration: int = 5
):
    """
    White wave effect.
    :param led_object: led object
    :param neopixel_list: list of neopixel colors
    :param int duration: duration in seconds. Default is 5 seconds
    """
    # Animation variables
    # TODO: Expose the saturation max and min values
    # TODO: Expose the animation speed
    # TODO: add the limits of color 2 and 1 to certain limits according to palette

    fade = 0
    color = 0
    color2 = 255

    # Start time
    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(num_leds):
            # Calculate brightness for each LED using sine wave

            brightness = math.cos(fade + math.pi)
            brightness = (brightness + 1) / 2

            brightness = int(brightness * 255)
            color_put = color, 128, brightness
            neopixel_list[i] = color_put
        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)

        if fade >= 2 * math.pi:
            fade = 0
            color = random.choice(range(0, 255))
            color2 = random.choice(range(0, 255))

        # Increment animation variables
        fade += 0.08

        # Small delay to control the speed of the animation
        time.sleep(0.01)


def fadein_fadeout_fragmented_effect(
    led_object, neopixel_list, num_leds, duration: int = 5
):
    """
    White wave effect.
    :param led_object: led object
    :param neopixel_list: list of neopixel colors
    :param int duration: duration in seconds. Default is 5 seconds
    """
    # Animation variables
    # TODO: Expose the saturation max and min values
    # TODO: Expose the animation speed
    # TODO: add the limits of color 2 and 1 to certain limits according to palette
    # TODO: improve segment verification according to the number of leds

    fade = 0
    color = 0
    fragments = 1
    fragment_size = math.ceil(num_leds / fragments)

    fragment = 0

    # Start time
    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(
            fragment * fragment_size, fragment_size * (fragment + 1)
        ):
            # Calculate brightness for each LED using sine wave

            brightness = math.cos(fade + math.pi)
            brightness = (brightness + 1) / 2

            brightness = int(brightness * 255)
            color_put = color, 255, brightness
            neopixel_list[i] = color_put
        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)

        if fade >= 2 * math.pi:
            fade = 0
            color = random.choice(range(0, 255))
            fragment = fragment + 1
            fragment = fragment % fragments

        # Increment animation variables
        fade += 0.08

        # Small delay to control the speed of the animation
        time.sleep(0.01)


def fifo_fragmented_phase_effect(
    led_object, neopixel_list, num_leds, duration: int = 5
):
    """
    White wave effect.
    :param led_object: led object
    :param neopixel_list: list of neopixel colors
    :param int duration: duration in seconds. Default is 5 seconds
    """
    # Animation variables
    # TODO: Expose the saturation max and min values
    # TODO: Expose the animation speed
    # TODO: add the limits of color 2 and 1 to certain limits according to palette
    # TODO: improve segment verification according to the number of leds

    fade = 0

    fragment_amount = 1
    fragment_size = math.floor(num_leds / fragment_amount)

    # Start time
    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(fragment_amount):
            # Calculate brightness for each LED using cosine wave
            brightness = math.cos(fade + (math.pi // 2 * i))
            brightness = (brightness + 1) / 2
            brightness = int(brightness * 255)

            # Set color for each LED
            begin = i * fragment_size
            end = min(fragment_size * (i + 1), num_leds)
            for j in range(begin, end):
                neopixel_list[j] = 0, 0, brightness

        fade += 0.03

        if fade >= 20:
            fade = 0
            if fragment_amount >= 8:
                fragment_amount = 1
            fragment_amount *= 2
            fragment_size = math.ceil(num_leds / fragment_amount)

            led_object.fill_all(color=(0, 0, 0))

        # Increment animation variables
        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)

        # Small delay to control the speed of the animation
        time.sleep(0.01)


def wave_freq_shrink_and_grow_effect(
    led_object, neopixel_list, num_leds, duration: int = 5
):
    """
    White wave effect.
    :param led_object: led object
    :param neopixel_list: list of neopixel colors
    :param int duration: duration in seconds. Default is 5 seconds
    """
    # Animation variables
    # TODO: Expose the saturation max and min values
    # TODO: Expose the animation speed
    # TODO: add the limits of color 2 and 1 to certain limits according to palette
    # TODO: improve segment verification according to the number of leds
    move = 0
    freq = 0

    # Start time
    start_time = time.time()
    while time.time() - start_time < duration:
        shrinkage = math.sin(freq)
        shrinkage = (shrinkage + 1) / 2

        for i in range(num_leds):
            # Calculate brightness for each LED using sine wave
            saturation = math.sin(move + i * shrinkage)
            saturation = (saturation + 1) / 2
            saturation = int(saturation * 255)
            saturation = max(saturation, 30)
            color_put = 170, saturation, 255
            neopixel_list[i] = color_put

        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)

        move += 0.2
        freq += 0.003

        # Small delay to control the speed of the animation
        time.sleep(0.01)
