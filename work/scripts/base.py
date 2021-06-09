#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
from work.scripts import change, db, create, files
from work import config
from work.scripts.right_menu import RightMenu
import pickle
import os


class Frame(tk.Frame):
    def __init__(self, root: tk.Tk, *args, **kwargs):
        """Create a toolbar, the text field and the scrollbar.
        Configure the text field."""
        tk.Frame.__init__(self, root, *args, **kwargs)

        # Detach the window root
        self.root = root

        # Create and pack the toolbar
        self.toolbar = tk.Frame(self.root, bg="#eee")
        self.toolbar.pack(side="top", fill="x")

        # Create the text field into the window
        self.text_field = tk.Text(root)

        # Configure the text field
        # Configure default font from config
        self.text_field.configure(font=create.font(config.default_font))

        # Configure font tags from db
        # Font ids
        if not os.path.exists(config.path_to_db + 'Font_ID.pkl'):
            db.update_database()

        with open(config.path_to_db + 'Font_ID.pkl', 'rb') as file:
            font_ids = pickle.load(file)

        for font_id in font_ids:
            self.text_field.tag_configure(f'{font_id}', font=create.font(font_id))

        # Configure color tags from db
        # Color ids
        if os.path.exists(config.path_to_db + 'Color.pkl'):
            with open(config.path_to_db + 'Color.pkl', 'rb') as file:
                color_ids = pickle.load(file)
        else:
            color_ids = set()
            with open(config.path_to_db + 'Color.pkl', 'wb') as file:
                pickle.dump(color_ids, file)
        for color in color_ids:
            self.text_field.tag_configure(f'{color}_fore', foreground=color)
            self.text_field.tag_configure(f'{color}_back', background=color)

        # Give focus to the text field
        self.text_field.focus()

        # Create a scrollbar and associate it with the text field
        self.scrollbar_obj = tk.Scrollbar(root, command=self.text_field.yview)
        self.scrollbar_obj.pack(side="right", fill='y')
        self.text_field['yscrollcommand'] = self.scrollbar_obj.set

        self.text_field.pack(fill="both", expand=True)

        # Create a menu on the window
        self.main_menu = tk.Menu(self.toolbar)

        # Configure the window with an indication of the menu for it
        self.root.config(menu=self.main_menu)

        # Create a menu items and place it on the main menu
        # First item - work with files and windows
        self.menu_item_file = tk.Menu(self.main_menu)
        self.main_menu.add_cascade(label="Файл", menu=self.menu_item_file)

        self.menu_item_file.add_command(label="Открыть...", command=self.open_window)
        self.menu_item_file.add_command(label="Сохранить...", command=self.save_to_file)
        self.menu_item_file.add_command(label="Создать", command=self.new_window)

        self.menu_item_file.add_separator()

        self.menu_item_file.add_command(label="Выход", command=self.close_window)

        # Second item - text type (weight and slant)
        self.menu_item_type = tk.Menu(self.main_menu)
        self.main_menu.add_cascade(label="Начертание", menu=self.menu_item_type)

        self.menu_item_type.add_command(label="Жирный", command=lambda: change.font(self.text_field, change.weight))
        self.menu_item_type.add_command(label="Курсив", command=lambda: change.font(self.text_field, change.slant))
        self.menu_item_type.add_command(label="Подчеркнутый", command=lambda: change.font(self.text_field,
                                                                                          change.underline))
        self.menu_item_type.add_command(label="Перебор", command=lambda: change.font(self.text_field,
                                                                                     change.overstrike))

        # Third item - text family
        self.menu_item_family = tk.Menu(self.main_menu)
        self.main_menu.add_cascade(label="Шрифт", menu=self.menu_item_family)

        self.menu_item_family.add_command(label='Arial', command=lambda: change.font(self.text_field, change.family,
                                                                                     'Arial'))
        self.menu_item_family.add_command(label='Calibri', command=lambda: change.font(self.text_field, change.family,
                                                                                       'Calibri'))
        self.menu_item_family.add_command(label='Helvetica', command=lambda: change.font(self.text_field, change.family,
                                                                                         'Helvetica'))

        # Forth item - text size
        self.menu_item_size = tk.Menu(self.main_menu)
        self.main_menu.add_cascade(label="Размер", menu=self.menu_item_size)

        self.menu_item_size.add_command(label='10', command=lambda: change.font(self.text_field, change.size, '10'))
        self.menu_item_size.add_command(label='12', command=lambda: change.font(self.text_field, change.size, '12'))
        self.menu_item_size.add_command(label='14', command=lambda: change.font(self.text_field, change.size, '14'))
        self.menu_item_size.add_command(label='18', command=lambda: change.font(self.text_field, change.size, '18'))
        self.menu_item_size.add_command(label='24', command=lambda: change.font(self.text_field, change.size, '24'))
        self.menu_item_size.add_command(label='28', command=lambda: change.font(self.text_field, change.size, '28'))
        self.menu_item_size.add_command(label='30', command=lambda: change.font(self.text_field, change.size, '30'))
        self.menu_item_size.add_command(label='34', command=lambda: change.font(self.text_field, change.size, '34'))
        self.menu_item_size.add_command(label='48', command=lambda: change.font(self.text_field, change.size, '48'))
        self.menu_item_size.add_command(label='54', command=lambda: change.font(self.text_field, change.size, '54'))
        self.menu_item_size.add_command(label='60', command=lambda: change.font(self.text_field, change.size, '60'))
        self.menu_item_size.add_command(label='74', command=lambda: change.font(self.text_field, change.size, '74'))

        # Fifth item - foreground color
        self.menu_item_fg = tk.Menu(self.main_menu)
        self.main_menu.add_cascade(label='Цвет текста', menu=self.menu_item_fg)

        self.menu_item_fg.add_command(label='Красный', command=lambda: change.font(self.text_field, change.color,
                                                                                   '#ff0000', 'fore'))
        self.menu_item_fg.add_command(label='Зеленый', command=lambda: change.font(self.text_field, change.color,
                                                                                   '#00ff00', 'fore'))
        self.menu_item_fg.add_command(label='Синий', command=lambda: change.font(self.text_field, change.color,
                                                                                 '#0000ff', 'fore'))
        self.menu_item_fg.add_command(label='Белый', command=lambda: change.font(self.text_field, change.color,
                                                                                 '#ffffff', 'fore'))
        self.menu_item_fg.add_command(label='Черный', command=lambda: change.font(self.text_field, change.color,
                                                                                  '#000000', 'fore'))

        # Sixth item - background color
        self.menu_item_bg = tk.Menu(self.main_menu)
        self.main_menu.add_cascade(label='Цвет фона', menu=self.menu_item_bg)

        self.menu_item_bg.add_command(label='Красный', command=lambda: change.font(self.text_field, change.color,
                                                                                   '#ff0000', 'back'))
        self.menu_item_bg.add_command(label='Зеленый', command=lambda: change.font(self.text_field, change.color,
                                                                                   '#00ff00', 'back'))
        self.menu_item_bg.add_command(label='Синий', command=lambda: change.font(self.text_field, change.color,
                                                                                 '#0000ff', 'back'))
        self.menu_item_bg.add_command(label='Белый', command=lambda: change.font(self.text_field, change.color,
                                                                                 '#ffffff', 'back'))
        self.menu_item_bg.add_command(label='Черный', command=lambda: change.font(self.text_field, change.color,
                                                                                  '#000000', 'back'))

        # Last item - help
        self.menu_item_help = tk.Menu(self.main_menu)
        self.main_menu.add_cascade(label="Помощь", menu=self.menu_item_help)

        self.menu_item_help.add_command(label="О программе", command=self.about)

        # Right Menu initialization
        self.right_menu = RightMenu(self.root, self.text_field)

        self.file = files.FileOperator(self)

    def open_window(self):
        pass

    def save_to_file(self):
        pass

    def new_window(self):
        pass

    def close_window(self):
        pass

    def about(self):
        pass
