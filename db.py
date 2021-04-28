#!/usr/bin/env python
# coding: utf-8

# !/usr/bin/env python
# coding: utf-8


from pony.orm import *
from datetime import datetime
from config import fonts, colors

date_format = '%d.%m.%y %H:%M:%S'

db = Database()


class Font(db.Entity):
    id = PrimaryKey(str)
    family = Required(str)
    size = Required(str)
    weight = Required(str)
    slant = Required(str)
    underline = Required(str)
    overstrike = Required(str)
    date = Required(str)

class Color(db.Entity):
    id = PrimaryKey(str)
    name = Required(str)
    date = Required(str)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
set_sql_debug(True)
db.generate_mapping(create_tables=True)


@db_session
def add_colors(colors: dict):
    old_colors_id = set(select(color.id for color in Color))

    for ID in colors.keys():
        if ID not in old_colors_id:
            Color(
                id=ID,
                name=colors[ID],
                date=datetime.now().strftime(date_format)
            )


@db_session
def add_fonts(fonts: dict):
    old_fonts_id = set(select(font.id for font in Font))

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
                date=datetime.now().strftime(date_format)
            )
            old_fonts_id.add(ID)


add_fonts(fonts)
add_colors(colors)

commit()
