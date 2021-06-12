#!/usr/bin/env python
# coding: utf-8

from work.scripts import data_converters
from work import config
import os
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog


class FileOperator:
    def __init__(self, root: tk.Frame):
        """Set root window and used elements"""
        self.filetype = config.file_format
        self.root = root
        self.parser = data_converters.Parser()
        self.serializer = data_converters.Serializer()

    def browse_files(self, func_type: str):
        """Get filename via explorer"""
        if func_type == 'o':
            func = filedialog.askopenfilename
            title = 'Выберите имя файла'
        else:
            func = filedialog.asksaveasfilename
            title = 'Введите имя файла'
        filename = func(initialdir=os.path.join(os.getcwd(), 'files'),
                        title=title,
                        filetypes=(self.filetype,
                                   ("Text files",
                                    "*.txt*"),
                                   ("all files",
                                    "*.*")))
        return filename

    def txt_confirmation(self):
        """Create window to confirm saving to txt file"""
        def cancel():
            pop_up.grab_release()
            pop_up.destroy()

        pop_up = tk.Toplevel(self.root)
        pop_up.grab_set()
        pop_up.resizable(False, False)
        pop_up.geometry('250x100+100+100')
        label = tk.Label(pop_up, justify=tk.CENTER, text="Запись в формат '.txt' сохранит\n"
                                                         "только текст без форматирования.\n"
                                                         "Продолжить?")
        label.place(x=0, y=0)
        var = tk.IntVar()
        cont_btn = tk.Button(pop_up, fg='blue', text='Да', command=lambda: var.set(1))
        cont_btn.place(x=80, y=50)
        cancel_btn = tk.Button(pop_up, text='Нет', fg='blue', command=cancel)
        cancel_btn.place(x=160, y=50)
        pop_up.title(f"test")
        cont_btn.wait_variable(var)
        pop_up.grab_release()
        pop_up.destroy()
        return 1

    def open_file(self, filename: str = None):
        """Open file and return character list"""
        if filename is None:
            filename = self.browse_files('o')
        if not filename:
            return None
        ftype = filename.split('.')[-1]
        main_type = self.filetype[1][2:-1]
        if ftype not in ['txt', main_type]:
            info_popup('Данный формат файла не поддерживается')
            return None
        f = open(filename, 'r')
        text = f.read()
        f.close()
        if ftype == main_type:
            char_list = self.parser.parse(text)
            if char_list is None:
                info_popup('Файл поврежден')
        else:
            char_list = self.parser.parse_from_txt(text)
        return char_list

    def save_file(self, char_list: list, filename: str = None):
        """Save character list into file"""
        if filename is None:
            filename = self.browse_files('s')
        if not filename:
            return 0
        ftype = filename.split('.')[-1]
        main_type = self.filetype[1][2:-1]
        if ftype not in ['txt', main_type]:
            info_popup('Данный формат файла не поддерживается')
            return 0
        if ftype == main_type:
            text = self.serializer.serialize(char_list)
        else:
            if self.txt_confirmation():
                text = self.serializer.serialize_to_txt(char_list)
            else:
                return 0
        f = open(filename, 'w')
        f.write(text)
        f.close()
        info_popup('Файл сохранен')
        return 1


def info_popup(msg: str, title: str = None):
    """Create popup with given message"""
    messagebox.showinfo(title=title, message=msg)
