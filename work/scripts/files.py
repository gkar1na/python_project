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
        self.initialdir = os.path.join(os.getcwd(), 'files')
        self.last_file = None

    def save_on_quit(self):
        """Ask whether to save unsaved changes before closing window or not"""
        def cancel():
            pop_up.grab_release()
            var.set(0)
            pop_up.destroy()

        pop_up = tk.Toplevel(self.root)
        pop_up.grab_set()
        pop_up.resizable(False, False)
        pop_up.geometry('250x100+100+100')
        label = tk.Label(pop_up, justify=tk.CENTER, text="У вас есть несохраненные изменения\n"
                                                         "Сохранить их?")
        label.place(x=0, y=0)
        var = tk.IntVar()
        yes_btn = tk.Button(pop_up, fg='blue', text='Да', command=lambda: var.set(1))
        yes_btn.place(x=40, y=50)
        no_btn = tk.Button(pop_up, fg='blue', text='Нет', command=lambda: var.set(-1))
        no_btn.place(x=100, y=50)
        cancel_btn = tk.Button(pop_up, text='Отмена', fg='blue', command=cancel)
        cancel_btn.place(x=160, y=50)
        pop_up.wait_variable(var)
        pop_up.grab_release()
        res = var.get()
        pop_up.destroy()
        return res

    def browse_files(self, func_type: str):
        """Get filename via explorer"""
        if func_type == 'o':
            func = filedialog.askopenfilename
            title = 'Выберите имя файла'
        else:
            func = filedialog.asksaveasfilename
            title = 'Введите имя файла'
        filename = func(initialdir=self.initialdir,
                        title=title,
                        filetypes=(self.filetype,
                                   ("Text files",
                                    "*.txt*"),
                                   ("all files",
                                    "*.*")),
                        defaultextension=self.filetype[1][1:-1])
        if filename:
            self.initialdir = filename.rsplit(os.sep, maxsplit=1)[0]
        return filename

    def txt_confirmation(self):
        """Create window to confirm saving to txt file"""
        def cancel():
            pop_up.grab_release()
            var.set(0)
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
        cont_btn.wait_variable(var)
        pop_up.grab_release()
        res = var.get()
        pop_up.destroy()
        return res

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
                self.last_file = filename
                self.root.root.title(f"Текстовый редактор (%s)" % filename)
        else:
            char_list = self.parser.parse_from_txt(text)
        return char_list

    def save_file(self, char_list: list):
        """Save character list into current working file"""
        if self.last_file is None:
            return self.save_as_file(char_list)
        text = self.serializer.serialize(char_list)
        f = open(self.last_file, 'w')
        f.write(text)
        f.close()
        return 1

    def save_as_file(self, char_list: list, filename: str = None):
        """Save character list into chosen file"""
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
            self.last_file = filename
            self.root.root.title(f"Текстовый редактор (%s)" % filename)
        else:
            if self.txt_confirmation():
                text = self.serializer.serialize_to_txt(char_list)
            else:
                return 0
        f = open(filename, 'w')
        f.write(text)
        f.close()
        if ftype == 'txt':
            return 0
        return 1

    def clear_last_file(self):
        self.root.root.title("Текстовый редактор (new_file)")
        self.last_file = None


def info_popup(msg: str, title: str = None):
    """Create popup with given message"""
    messagebox.showinfo(title=title, message=msg)
