#!/usr/bin/env python
# coding: utf-8

date_format = '%d.%m.%y %H:%M:%S'

path_to_db = '../work/data/'

file_format = ('Python project file', '*.ppf*')
open_file_name = None
save_file_name = None

default_font = 'Calibri.12.normal.roman.0.0'
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
    '#ff0000': 'red',
    '#00ff00': 'green',
    '#0000ff': 'blue',
    '#000000': 'black',
    '#ffffff': 'white'
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
                            f'{family}.{size}.{weight}.{slant}.{underline}.{overstrike}',
                            {
                                'family': family,
                                'size': size,
                                'weight': weight,
                                'slant': slant,
                                'underline': underline,
                                'overstrike': overstrike,
                            }
                        )])
