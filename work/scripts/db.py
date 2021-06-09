#!/usr/bin/env python
# coding: utf-8


from work import config
import pickle
import os


def add_colors(colors: dict):
    """Update the color table following the information from config"""
    # Old color ids
    if os.path.exists(config.path_to_db + 'Color.pkl'):
        with open(config.path_to_db + 'Color.pkl', 'rb') as f:
            color_ids = pickle.load(f)
    else:
        color_ids = set()
        with open(config.path_to_db + 'Color.pkl', 'wb') as f:
            pickle.dump(color_ids, f)

    # Add new colors
    for ID in colors.keys():
        if ID not in color_ids:
            color_ids.add(ID)

    with open(config.path_to_db + 'Color.pkl', 'wb') as f:
        pickle.dump(color_ids, f)


def add_font_ids(fonts: dict):
    """Update the font table following the information from config"""
    # Old font ids
    if os.path.exists(config.path_to_db + 'Font_ID.pkl'):
        with open(config.path_to_db + 'Font_ID.pkl', 'rb') as f:
            font_ids = pickle.load(f)
    else:
        font_ids = set()
        with open(config.path_to_db + 'Font_ID.pkl', 'wb') as f:
            pickle.dump(font_ids, f)

    # Add new fonts
    for ID in fonts.keys():
        if ID not in font_ids:
            font_ids.add(ID)
    with open(config.path_to_db + 'Font_ID.pkl', 'wb') as f:
        pickle.dump(font_ids, f)


def update_database():
    """Update the tables."""
    add_font_ids(config.fonts)
    add_colors(config.colors)


if __name__ == "__main__":
    update_database()
