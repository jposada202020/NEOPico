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
