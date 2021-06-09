#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
from work.scripts import base
from work import config


class Pad(base.Frame):

    def close_window(self):
        """Close an old independent window."""

        self.root.destroy()

    def about(self):
        """Create a new window with information about the program."""
        # Create the window
        about_window = tk.Toplevel(self.toolbar)

        # Configure the window
        about_window.title("О программе")
        about_window.geometry("300x150")

        # Create the window label
        about_label = tk.Label(about_window, text="Версия программы 1.0")
        about_label.pack()

    def open_window(self, event: tk.Event = None):
        """Open a new independent window from an existing file."""
        input_data = self.file.open_file(config.open_file_name)
        print(input_data)
        if input_data is None:
            return
        self.text_field.delete('1.0', tk.END)
        self.right_menu.index = '1.0'
        self.right_menu.buffer_tags = []
        self.right_menu.buffer_selected = []

        for data in input_data:
            self.right_menu.buffer_tags.append(data['tags'])
            self.right_menu.buffer_selected.append(data['char'])

        self.right_menu.buffer_selected = ''.join(self.right_menu.buffer_selected)
        self.right_menu.paste(True)
        print('open_window')

    def save_to_file(self, event: tk.Event = None):
        """Save the text field with all information about all symbols to a new file."""
        output_data = []
        index = '1.0'
        while self.text_field.compare(index, '<', 'end'):
            output_data.append({
                'char': self.text_field.get(index),
                'index': index,
                'tags': self.text_field.tag_names(index)
            })
            index = self.text_field.index(f'{index}+1c')
        print(output_data)
        status = self.file.save_file(output_data, config.open_file_name)
        if not status:
            return
        print('save_to_file')

    def new_window(self, event: tk.Event = None):
        """Again run files.py."""
        self.text_field.delete('1.0', tk.END)


def create_window():
    """Create and update a new independent window."""
    root = tk.Tk()
    root.title(f"Текстовый редактор")
    p = Pad(root)
    p.pack(expand=1, fill="both")
    root.bind('<Control-Key-s>', p.save_to_file)
    root.bind('<Control-Key-o>', p.open_window)
    root.bind('<Control-Key-n>', p.new_window)
    root.mainloop()
