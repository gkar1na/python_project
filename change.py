#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
import config
from datetime import datetime


def family(text_field: tk.Text, family: str, size: str, weight: str, slant: str, underline: str, overstrike: str, new_family: str, *args):
    """Get all the old parameters and the new family.
    Change the family to a new one.
    Return new parameters."""
    family = new_family
    print('LOGGING: change family')
    return family, size, weight, slant, underline, overstrike


def size(text_field: tk.Text, family: str, size: str, weight: str, slant: str, underline: str, overstrike: str, new_size: str, *args):
    """Get all the old parameters and the new size.
    Resize to a new one.
    Return new parameters."""
    size = new_size
    print('LOGGING: change size')
    return family, size, weight, slant, underline, overstrike


def weight(text_field: tk.Text, family: str, size: str, weight: str, slant: str, underline: str, overstrike: str, *args):
    """Get all the old parameters.
    Change the weight condition.
    Return new parameters."""
    weight = 'bold' if weight == 'normal' else 'normal'
    print('LOGGING: change weight')
    return family, size, weight, slant, underline, overstrike


def slant(text_field: tk.Text, family: str, size: str, weight: str, slant: str, underline: str, overstrike: str, *args):
    """Get all the old parameters.
    Change the slant condition.
    Return new parameters."""
    slant = 'roman' if slant == 'italic' else 'italic'
    return family, size, weight, slant, underline, overstrike


def underline(text_field: tk.Text, family: str, size: str, weight: str, slant: str, underline: str, overstrike: str, *args):
    """Get all the old parameters.
    Change the underline condition.
    Return new parameters."""
    underline = '1' if underline == '0' else '0'
    return family, size, weight, slant, underline, overstrike


def overstrike(text_field: tk.Text, family: str, size: str, weight: str, slant: str, underline: str, overstrike: str, *args):
    """Get all the old parameters.
    Change the overstrike condition.
    Return new parameters."""
    overstrike = '1' if overstrike == '0' else '0'
    return family, size, weight, slant, underline, overstrike


def color(text_field: tk.Text, family: str, size: str, weight: str, slant: str, underline: str, overstrike: str, new_color: str, index: str, ground: str, *args):
    """Get all the old parameters, the new color, the symbol index and the characteristic of the color change place.
    Remove the fore/back ground color tag if it is possible
    and add new fore/back ground color text tag
    (for one symbol).
    Return new parameters."""
    # Try to remove the fore/back ground color tag
    try:
        tags = text_field.tag_names(index)
        tag = None
        for i in range(len(tags)):
            if tags[i].find(f'_{ground}') != -1 and tags[i].find('#') != -1:
                tag = tags[i]
                break
        if tag:
            text_field.tag_remove(tag, index)

    except Exception as e:
        with open(config.path_to_errors, 'a') as f:
            print(f'{datetime.now()} - change.py - cant remove the {ground}ground color tag in color() from change.py - "{e}"', file=f)

    # Add a tag in order to change the fore/back ground color
    else:
        text_field.tag_add(f'{new_color}_{ground}', index)

    print('LOGGING: change color')
    # Return new parameters
    return family, size, weight, slant, underline, overstrike


def font(text_field: tk.Text, func, new_value=None, ground=None):
    """Get the text field, function
    (optionally the new value and the characteristic of the color change place).
    Remove the font tag if it is possible
    and add new font tag
    (for selected symbols)."""
    try:
        index = text_field.index(f"{tk.SEL_FIRST}")
        while text_field.compare(index, '<', tk.SEL_LAST):
            tags = list(text_field.tag_names(index))
            try:
                tag = None
                for i in range(len(tags)):
                    if tags[i].find('.') != -1:
                        tag = tags[i]
                        break
                if tag:
                    text_field.tag_remove(tag, index)
                else:
                    tag = config.default_font
            except:
                tag = config.default_font
            family, size, weight, slant, underline, overstrike = func(text_field, *map(str, tag.split('.')), new_value, index, ground)
            tag = f'{family}.{size}.{weight}.{slant}.{underline}.{overstrike}'
            text_field.tag_add(tag, index)
            index = text_field.index(f"{index}+1c")
    except tk.TclError:
        pass

