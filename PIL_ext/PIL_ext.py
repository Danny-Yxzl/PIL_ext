"""
This project is licensed under the MIT license.
It is cretaed in order to make it more convenient to use PIL.
Without especial description, all functions required an 'PIL.Image.Image' type object for the first argument 'im', and returns an 'PIL.Image.Image' type value.

    Created on 2022/05/08
    Author: Danny@Yixiangzhilv
    Copyright (c) 2022 Yixiangzhilv. All rights reserved.
"""

from typing import Union

from PIL import Image, ImageDraw, ImageFont


def insert_image(im1: Image.Image,
                 im2: Image.Image,
                 box: tuple,
                 radii: int = 0) -> Image.Image:
    """Auto crop, resize and insert image into another image"""
    if len(box) != 4:
        raise ValueError("'box' must be a tuple of 4 integers")
    w, h = box[2] - box[0], box[3] - box[1]
    im2_w, im2_h = im2.size
    while im2_w < w or im2_h < h:
        im2 = im2.resize((im2_w * 2, im2_h * 2))
        im2_w *= 2
        im2_h *= 2
    if im2_w / im2_h > w / h:
        temp_w = w * im2_h / h
        im2 = im2.crop(
            ((im2_w - temp_w) // 2, 0, im2_w - (im2_w - temp_w) // 2, im2_h))
    elif im2_w / im2_h < w / h:
        temp_h = h * im2_w / w
        im2 = im2.crop(0, (im2_h - temp_h) // 2, im2_w,
                       im2_h - (im2_h - temp_h) // 2)
    im2 = im2.resize((w, h))
    if radii:
        im2 = add_border_radius(im2, radii)
    im3 = Image.new('RGBA', im1.size, (0, 0, 0, 0))
    im3.paste(im2, box)
    return Image.alpha_composite(im1, im3)


def insert_circle_image(im1: Image.Image, im2: Image.Image,
                        box: tuple) -> Image.Image:
    im2_w, im2_h = im2.size
    mask = Image.new('RGBA', (im2_w, im2_h), (0, 0, 0, 0))
    ImageDraw.Draw(mask).ellipse((0, 0, im2_w, im2_h), fill=(255, 255, 255))
    im3 = Image.new('RGBA', (im2_w, im2_h), (0, 0, 0, 0))
    im3.paste(im2, (0, 0), mask=mask)
    return insert_image(im1, im3, box)


def crop_into_square(im: Image.Image) -> Image.Image:
    """Crop image's middle part into a square"""
    p_w, p_h = im.size
    p_box = (0, 0, p_w, p_h)
    if p_w > p_h:
        p_box = ((p_w - p_h) // 2, 0, p_w - (p_w - p_h) // 2, p_h)
    elif p_h > p_w:
        p_box = (0, (p_h - p_w) // 2, p_w, p_h - (p_h - p_w) // 2)
    return im.crop(p_box)


def add_border_radius(im: Image.Image, radii: int) -> Image.Image:
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建黑色方形
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)
    w, h = im.size
    alpha = Image.new('L', (w, h), 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)),
                (w - radii, h - radii))
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))
    im.putalpha(alpha)
    return im


def _get_font(font: Union[str, ImageFont.ImageFont],
              size: int) -> ImageFont.ImageFont:
    """Parse font"""
    if type(font) not in (str, ImageFont.ImageFont):
        raise TypeError(
            "font must be a string or a ImageFont.ImageFont object")
    elif type(font) == str:
        font = ImageFont.truetype(font, size=size)
    return font


def _auto_new_line(text: str, font: ImageFont.ImageFont,
                   max_width: int) -> list:
    """Parse text to list, split into new line if current line is longer than max_width"""
    text_list = []
    current_line = ''
    for i in range(len(text)):
        if text[i] == '\n':
            text_list.append(current_line)
            current_line = ''
            continue
        current_line += text[i]
        if font.getsize(current_line)[0] > max_width:
            text_list.append(current_line)
            current_line = ''
    if current_line:
        if font.getsize(current_line)[0] < 35:
            text_list[-1] += current_line
        else:
            text_list.append(current_line)
    return text_list


def add_text(im: Image.Image,
             text: str,
             font: Union[ImageFont.ImageFont, str],
             size: int = 25,
             color: tuple = (0, 0, 0),
             x: int = 0,
             y: int = 0,
             max_width: int = 0) -> Image.Image:
    """Add text to image"""
    if not text:
        return im
    font = _get_font(font, size)
    y_incr = font.getsize(text[0])[1]

    if max_width:
        text = _auto_new_line(text, font, max_width)
    else:
        text = text.split('\n')

    draw = ImageDraw.Draw(im)
    for i in text:
        draw.text((x, y), i, color, font=font)
        y += y_incr

    return im


def add_text_center(im: Image.Image,
                    text: str,
                    font: Union[ImageFont.ImageFont, str],
                    size: int = 25,
                    color: tuple = (0, 0, 0),
                    y: int = 0,
                    max_width: int = 0) -> Image.Image:
    """Add text to image, center align"""
    if not text:
        return im
    im_width = im.size[0]
    font = _get_font(font, size)
    y_incr = font.getsize(text[0])[1]

    if max_width:
        text = _auto_new_line(text, font, max_width)
    else:
        text = text.split('\n')

    draw = ImageDraw.Draw(im)
    for i in text:
        width = font.getsize(i)[0]
        draw.text(((im_width - width) // 2, y), i, color, font=font)
        y += y_incr

    return im
