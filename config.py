#!/usr/bin/env python
# coding: utf-8

from tkinter.font import Font, ROMAN


default_font = 'Helvetica.12.n.r.0.0'
default_foreground_color = '#000000'
default_background_color = '#ffffff'

families = {
    'Helvetica',
    'Arial',
    'Calibri'
}

sizes = [
    '10',
    '12',
    '14',
    '18',
    '24',
    '28',
    '30',
    '34',
    '48',
    '54',
    '60',
    '74'
]

weights = {
    'normal',
    'bold'
}

slants = {
    'roman',
    'italic'
}


underlines = {
    '0',
    '1'
}

overstrikes = {
    '0',
    '1'
}

colors = {
    '#ff0000',
    '#00ff00',
    '#0000ff',
    '#000000',
    '#ffffff'
}

fonts = {
}

for family in families:
    for size in sizes:
        for weight in weights:
            for slant in slants:
                for underline in underlines:
                    for overstrike in overstrikes:
                        fonts.update([(
                            f'{family}.{size}.{weight[0]}.{slant[0]}.{underline}.{overstrike}',
                            {
                                'family': family,
                                'size': size,
                                'weight': weight,
                                'slant': slant,
                                'underline': underline,
                                'overstrike': overstrike,
                            }
                        )])
