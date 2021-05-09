#!/usr/bin/env python
# coding: utf-8

import tkinter.font


def font(font_id: str):
    """Get the font id.
    Return the font from db as tkinter.font.Font object."""

    family, size, weight, slant, underline, overstrike = map(str, font_id.split('.'))

    font_obj = tkinter.font.Font(
        family=family,
        size=size,
        weight=weight,
        slant=slant,
        underline=underline,
        overstrike=overstrike
    )

    print(f'LOGGING: create new font: {font_id}')

    return font_obj
