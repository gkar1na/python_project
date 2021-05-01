#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
from tkinter.font import Font
from pony.orm import *
import config, db, change, create
from datetime import datetime
from right_menu import RightMenu

@db_session
class Pad(tk.Frame):
    def __init__(self, root: tk.Tk, *args, **kwargs):
        """Create a toolbar, the text field and the scrollbar.
        Configure the text field."""
        tk.Frame.__init__(self, root, *args, **kwargs)

        # Detach the window root
        self.root = root

        # Create and pack the toolbar
        self.toolbar = tk.Frame(self, bg="#eee")
        self.toolbar.pack(side="top", fill="x")

        # Create the text field into the window
        self.text_field = tk.Text(self)

        # Configure the text field
        # Configure default font from config
        self.text_field.configure(font=create.font(config.default_font))
        self.text_field.insert("end", "Test text\nqwertyuiop\nasdfghjkl\nzxcvbnm")

        # Configure font tags from db
        for font_id in set(select(font.id for font in db.Font)):
            self.text_field.tag_configure(font_id, font=create.font(font_id))

        # Configure color tags from db
        for color in set(select(color.id for color in db.Color)):
            self.text_field.tag_configure(f'{color}_fore', foreground=color)
            self.text_field.tag_configure(f'{color}_back', background=color)

        # Give focus to the text field
        self.text_field.focus()

        # Create a scrollbar and associate it with the text field
        self.scrollbar_obj = tk.Scrollbar(master=root, command=self.text_field.yview)
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
        self.menu_item_file.add_command(label="Создать", command=create_window)
        self.menu_item_file.add_command(label="Сохранить...", command=self.save_to_file)

        self.menu_item_file.add_separator()

        self.menu_item_file.add_command(label="Выход", command=self.close_window)

        # Second item - text type (weight and slant)
        self.menu_item_type = tk.Menu(self.main_menu)
        self.main_menu.add_cascade(label="Начертание", menu=self.menu_item_type)

        self.menu_item_type.add_command(label="Жирный", command=lambda: change.font(self.text_field, change.weight))
        self.menu_item_type.add_command(label="Курсив", command=lambda: change.font(self.text_field, change.slant))
        self.menu_item_type.add_command(label="Подчеркнутый", command=lambda: change.font(self.text_field, change.underline))
        self.menu_item_type.add_command(label="Перебор", command=lambda: change.font(self.text_field, change.overstrike))

        # Third item - text family
        self.menu_item_family = tk.Menu(self.main_menu)
        self.main_menu.add_cascade(label="Шрифт", menu=self.menu_item_family)

        self.menu_item_family.add_command(label='Arial', command=lambda: change.font(self.text_field, change.family, 'Arial'))
        self.menu_item_family.add_command(label='Calibri', command=lambda: change.font(self.text_field, change.family, 'Calibri'))
        self.menu_item_family.add_command(label='Helvetica', command=lambda: change.font(self.text_field, change.family, 'Helvetica'))

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

        self.menu_item_fg.add_command(label='Красный', command=lambda: change.font(self.text_field, change.color, '#ff0000', 'fore'))
        self.menu_item_fg.add_command(label='Зеленый', command=lambda: change.font(self.text_field, change.color, '#00ff00', 'fore'))
        self.menu_item_fg.add_command(label='Синий', command=lambda: change.font(self.text_field, change.color, '#0000ff', 'fore'))
        self.menu_item_fg.add_command(label='Белый', command=lambda: change.font(self.text_field, change.color, '#ffffff', 'fore'))
        self.menu_item_fg.add_command(label='Черный', command=lambda: change.font(self.text_field, change.color, '#000000', 'fore'))

        # Sixth item - background color
        self.menu_item_bg = tk.Menu(self.main_menu)
        self.main_menu.add_cascade(label='Цвет фона', menu=self.menu_item_bg)

        self.menu_item_bg.add_command(label='Красный', command=lambda: change.font(self.text_field, change.color, '#ff0000', 'back'))
        self.menu_item_bg.add_command(label='Зеленый', command=lambda: change.font(self.text_field, change.color, '#00ff00', 'back'))
        self.menu_item_bg.add_command(label='Синий', command=lambda: change.font(self.text_field, change.color, '#0000ff', 'back'))
        self.menu_item_bg.add_command(label='Белый', command=lambda: change.font(self.text_field, change.color, '#ffffff', 'back'))
        self.menu_item_bg.add_command(label='Черный', command=lambda: change.font(self.text_field, change.color, '#000000', 'back'))

        # Last item - help
        self.menu_item_help = tk.Menu(self.main_menu)
        self.main_menu.add_cascade(label="Помощь", menu=self.menu_item_help)

        self.menu_item_help.add_command(label="О программе", command=self.about)

        # Bind to action()
        self.root.bind("<Key>", self.action)
        self.root.bind("<ButtonRelease>", self.action)

        # Right Menu initialization
        self.right_menu = RightMenu(self.root, self.text_field)

    def close_window(self):
        """Close an old independent window."""
        self.root.destroy()

    def about(self):
        """Create a new window with information about the program."""
        # Create the window
        self.about_window = tk.Toplevel(self.toolbar)

        # Configure the window
        self.about_window.title("О программе")
        self.about_window.geometry("300x150")

        # Create the window label
        self.about_label = tk.Label(self.about_window, text="Версия программы 1.0")
        self.about_label.pack()

    def action(self, event: tk.Event):
        """Print information about the current position of the cursor and the symbol at this position."""
        # Check selection
        try:
            print(f'select from {self.text_field.index(tk.SEL_FIRST)} to {self.text_field.index(tk.SEL_LAST)}')

        except tk.TclError:
            pass
        except Exception as e:
            with open(config.path_to_errors, 'a') as f:
                print(f'{datetime.now()} - sth in action() from main.py - "{e}"', file=f)

        # Print all information about the symbol
        finally:
            index = self.text_field.index(tk.INSERT)
            print(f'current cursor position: {index} - "{self.text_field.get(index)}", tags: {self.text_field.tag_names(index)}')

    def open_window(self):
        """Open a new independent window from an existing file."""
        print('open_window')

    def save_to_file(self):
        """Save the text field with all information about all symbols to a new file."""
        print('save_to_file')


def create_window():
    """Create and update a new independent window."""
    root = tk.Tk()
    root.title("Текстовый редактор")
    Pad(root).pack(expand=1, fill="both")
    root.mainloop()


if __name__ == "__main__":
    create_window()
