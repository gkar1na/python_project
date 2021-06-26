#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
from work.scripts import base
from work import config


class Pad(base.Frame):
    """Extend parent class functional"""

    def close_window(self):
        """Close an old independent window."""
        if self.changed:
            res = self.file.save_on_quit()
            if res == 0:
                return
            elif res == 1:
                self.save_to_file()
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

    def open_window(self):
        """Fill text field from an existing file."""
        input_data = self.file.open_file(config.open_file_name)
        if input_data is None:
            return
        self.changed = False
        self.text_field.delete('1.0', tk.END)
        self.right_menu.index = '1.0'
        self.right_menu.buffer_tags = []
        self.right_menu.buffer_selected = []

        for data in input_data:
            self.right_menu.buffer_tags.append(data['tags'])
            self.right_menu.buffer_selected.append(data['char'])

        self.right_menu.buffer_selected = ''.join(self.right_menu.buffer_selected)
        self.right_menu.paste(True)

    def get_output_data(self):
        """Create character list to save to file."""
        output_data = []
        index = '1.0'
        while self.text_field.compare(index, '<', 'end'):
            output_data.append({
                'char': self.text_field.get(index),
                'index': index,
                'tags': self.text_field.tag_names(index)
            })
            index = self.text_field.index(f'{index}+1c')
        return output_data

    def save_to_file(self):
        """Save the text field with all information about all symbols to current working file."""
        output_data = self.get_output_data()
        status = self.file.save_file(output_data)
        if not status:
            return
        self.text_changed(False)

    def save_as_file(self):
        """Save the text field with all information about all symbols to chosen file."""
        output_data = self.get_output_data()
        status = self.file.save_as_file(output_data, config.save_file_name)
        if not status:
            return
        self.changed = False

    def new_window(self):
        """Clear text field."""
        self.text_field.delete('1.0', tk.END)
        self.file.clear_last_file()
        self.changed = False

    def select_all(self):
        """Select all text."""
        self.text_field.tag_add(tk.SEL, "1.0", tk.END)
        self.text_field.mark_set(tk.INSERT, "1.0")
        self.text_field.see(tk.INSERT)

    def text_changed(self, changed: bool = True):
        """Change 'changed' status of the text."""
        if changed:
            if not self.changed:
                self.changed = True
                title = self.root.title()
                parts = title.rsplit(maxsplit=1)
                self.root.title(parts[0] + ' *' + parts[1])
        else:
            if self.changed:
                self.changed = False
                title = self.root.title()
                parts = title.rsplit(maxsplit=1)
                if parts[1][0] == '(':
                    parts[1] = '*' + parts[1]
                self.root.title(parts[0] + ' ' + parts[1][1:])

    def bind_alt_parser(self, event: tk.Event):
        """Bind some <alt+key> to functions."""
        key = event.keycode
        if key == 83:
            self.save_to_file()
        elif key == 79:
            self.open_window()
        elif key == 78:
            self.new_window()
        elif key == 88:
            self.right_menu.cut()
        elif key == 67:
            self.right_menu.copy()
        elif key == 86:
            self.right_menu.paste()
        elif key == 65:
            self.select_all()

    def bind_alt_shift_parser(self, event: tk.Event):
        """Bind some <alt+shift+key> to functions."""
        if event.keycode == 83:
            self.save_as_file()

    def bind_all_parser(self, event: tk.Event):
        """Bind some keys to functions."""
        key = event.keycode
        exceptions = list(range(112, 124)) + list(range(37, 41)) + [16, 17, 18, 20, 45, 91]
        if key == 27:
            self.text_field.tag_remove(tk.SEL, "1.0", tk.END)
        elif key not in exceptions:
            self.text_changed()


def create_window():
    """Create and update a new independent window."""
    root = tk.Tk()
    root.title("Текстовый редактор (new_file)")
    p = Pad(root)
    p.pack(expand=1, fill="both")
    root.bind('<Alt-Key>', p.bind_alt_parser)
    root.bind('<Alt-Shift-Key>', p.bind_alt_shift_parser)
    root.bind('<Key>', p.bind_all_parser)
    root.protocol("WM_DELETE_WINDOW", p.close_window)
    root.mainloop()
