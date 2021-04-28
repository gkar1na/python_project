#!/usr/bin/env python
# coding: utf-8


from pony.orm import *
from datetime import datetime
import config


db = Database()


class Font(db.Entity):
    """Font table"""
    id = PrimaryKey(str)
    family = Required(str)
    size = Required(str)
    weight = Required(str)
    slant = Required(str)
    underline = Required(str)
    overstrike = Required(str)
    date = Required(str)


class Color(db.Entity):
    """Color table."""
    id = PrimaryKey(str)
    name = Required(str)
    date = Required(str)


# Create db
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
set_sql_debug(True)
db.generate_mapping(create_tables=True)


@db_session
def add_colors(colors: dict):
    """Update the color table following the information from config"""
    # Old color ids
    old_colors_id = set(select(color.id for color in Color))

    # Add new colors
    for ID in colors.keys():
        if ID not in old_colors_id:
            Color(
                id=ID,
                name=colors[ID],
                date=datetime.now().strftime(config.date_format)
            )
            old_colors_id.add(ID)


@db_session
def add_fonts(fonts: dict):
    """Update the font table following the information from config"""
    # Old font ids
    old_fonts_id = set(select(font.id for font in Font))

    # Add new fonts
    for ID in fonts.keys():
        if ID not in old_fonts_id:
            Font(
                id=ID,
                family=fonts[ID]['family'],
                size=fonts[ID]['size'],
                weight=fonts[ID]['weight'],
                slant=fonts[ID]['slant'],
                underline=fonts[ID]['underline'],
                overstrike=fonts[ID]['overstrike'],
                date=datetime.now().strftime(config.date_format)
            )
            old_fonts_id.add(ID)


def update():
    """Update the tables."""
    add_fonts(config.fonts)
    add_colors(config.colors)
    commit()


if __name__ == "__main__":
    update()
