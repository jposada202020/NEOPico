import time
import math


def RGBW32(r: int, g: int, b: int, w: int) -> int:
    """Pack RGBW color components into a 32-bit integer.
    :param int r: Red component (0-255)
    :param int g: Green component (0-255)
    :param int b: Blue component (0-255)
    :param int w: White component (0-255)
    :return: 32-bit integer containing packed RGBW color
    :rtype: int
    """
    return (
        ((w & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)
    )


def red_component(color: int) -> int:
    """Extract red component from packed 32-bit RGBW color.
    :param int color: 32-bit packed RGBW color
    :return: Red component (0-255)
    :rtype: int
    """
    return (color >> 16) & 0xFF


def green_component(color: int) -> int:
    """Extract green component from packed 32-bit RGBW color.
    :param int color: 32-bit packed RGBW color
    :return: Green component (0-255)
    :rtype: int
    """
    return (color >> 8) & 0xFF


def blue_component(color: int) -> int:
    """Extract blue component from packed 32-bit RGBW color.
    :param int color: 32-bit packed RGBW color
    :return: Blue component (0-255)
    :rtype: int
    """
    return color & 0xFF


def white_component(color: int) -> int:
    """Extract white component from packed 32-bit RGBW color.
    :param int color: 32-bit packed RGBW color
    :return: White component (0-255)
    :rtype: int
    """
    return (color >> 24) & 0xFF


def fade_out(segment, color: int, rate: int) -> int:
    """Fade out a color by reducing its brightness.
    :param int color: 32-bit packed RGBW color
    :param int rate: Fade rate (0-255)
    :return: Faded color
    :rtype: int
    """
    rate = (255 - rate) >> 1
    mapped_rate = 1.0 / (float(rate) + 1.1)

    w2 = white_component(color)
    r2 = red_component(color)
    g2 = green_component(color)
    b2 = blue_component(color)

    for x in range(segment.length):
        color_buf = segment.pixel_object[x]

        if color == color_buf:
            continue  # already at target color

        w1 = white_component(color_buf)
        r1 = red_component(color_buf)
        g1 = green_component(color_buf)
        b1 = blue_component(color_buf)

        w_delta = int((w2 - w1) * mapped_rate)
        r_delta = int((r2 - r1) * mapped_rate)
        g_delta = int((g2 - g1) * mapped_rate)
        b_delta = int((b2 - b1) * mapped_rate)

        # if fade isn't complete, make sure delta is at least 1 (fixes rounding issues)
        w_delta += 0 if w2 == w1 else 1 if w2 > w1 else -1
        r_delta += 0 if r2 == r1 else 1 if r2 > r1 else -1
        g_delta += 0 if g2 == g1 else 1 if g2 > g1 else -1
        b_delta += 0 if b2 == b1 else 1 if b2 > b1 else -1

        total = RGBW32(r1 + r_delta, g1 + g_delta, b1 + b_delta, w1 + w_delta)

        segment.pixel_object[x] = total

        time.sleep(0.1)


def lerp8by8(a, b, frac):
    """
    Linearly interpolate between two 8-bit values by an 8-bit fraction.

    :param a: The start value (0-255)
    :param b: The end value (0-255)
    :param frac: The fraction (0-255)
    :return: The interpolated value (0-255)
    """
    if b > a:
        delta = b - a
        scaled = scale8(delta, frac)
        result = a + scaled
    else:
        delta = a - b
        scaled = scale8(delta, frac)
        result = a - scaled
    return result


def scale8(value, scale):
    """Scale an 8-bit value by an 8-bit scale factor."""
    return (value * scale) // 256


def rgb255(color: list):
    """Set color of a specific LED.
    :param list color: RGB color values
    :return: RGB color values

    """

    return (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))


def hsv_to_rgb(
    hue: float, sat: float, val: float
) -> Tuple[float, float, float]:
    """Converts HSV to RGB values

    :param float hue: The hue of the color to convert
    :param float sat: The saturation of the color to convert
    :param float val: The value (or brightness) of the color to convert
    :return: RGB values
    :rtype: Tuple[float, float, float]
    """
    if sat == 0.0:
        return val, val, val
    i = int(hue * 6.0)  # assume int() truncates!
    hue1 = (hue * 6.0) - i
    chroma1 = val * (1.0 - sat)
    chroma2 = val * (1.0 - sat * hue1)
    chroma3 = val * (1.0 - sat * (1.0 - hue1))
    i = i % 6
    if i == 0:
        return val, chroma3, chroma1
    if i == 1:
        return chroma2, val, chroma1
    if i == 2:
        return chroma1, val, chroma3
    if i == 3:
        return chroma1, chroma2, val
    if i == 4:
        return chroma3, chroma1, val
    if i == 5:
        return val, chroma1, chroma2


def colorwheel(color_value: int) -> tuple:
    """
    Author(s): Kattni Rembor, Carter Nelson
    A colorwheel. ``0`` and ``255`` are red, ``85`` is green, and ``170`` is blue, with the values
    between being the rest of the rainbow.

    :param int color_value: 0-255 of color value to return
    :return: tuple of RGB values
    """
    color_value = int(color_value)
    if color_value < 0 or color_value > 255:
        red = 0
        green = 0
        blue = 0
    elif color_value < 85:
        red = int(255 - color_value * 3)
        green = int(color_value * 3)
        blue = 0
    elif color_value < 170:
        color_value -= 85
        red = 0
        green = int(255 - color_value * 3)
        blue = int(color_value * 3)
    else:
        color_value -= 170
        red = int(color_value * 3)
        green = 0
        blue = int(255 - color_value * 3)
    return (red, green, blue)
