#!/usr/bin/env python
# coding: utf-8

from pony.orm import *
from tkinter.font import Font
import tkinter as tk
import db, main

@db_session
def font(font_id: str):
    """Get the font id.
    Return the font from db as tkinter.font.Font object."""
    family = get(font.family for font in db.Font if font.id == font_id)
    size = get(font.size for font in db.Font if font.id == font_id)
    weight = get(font.weight for font in db.Font if font.id == font_id)
    slant = get(font.slant for font in db.Font if font.id == font_id)
    underline = get(font.underline for font in db.Font if font.id == font_id)
    overstrike = get(font.overstrike for font in db.Font if font.id == font_id)

    font_obj = Font(
        family=family,
        size=size,
        weight=weight,
        slant=slant,
        underline=underline,
        overstrike=overstrike
    )

    return font_obj
