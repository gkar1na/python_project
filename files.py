#!/usr/bin/env python
# coding: utf-8

import config
import os
import data_converters
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog


class RenameIt:
    def __init__(self, root: tk.Frame):
        self._filetype = config.file_format
        self._root = root
        self._parser = data_converters.Parser()
        self._serializer = data_converters.Serializer()

    def _browse_files(self, func_type: str):
        if func_type == 'o':
            func = filedialog.askopenfilename
            title = 'Выберите имя файла'
        else:
            func = filedialog.asksaveasfilename
            title = 'Введите имя файла'
        filename = func(initialdir=os.getcwd(),
                        title=title,
                        filetypes=(self._filetype,
                                   ("Text files",
                                    "*.txt*"),
                                   ("all files",
                                    "*.*")))
        print(filename)
        return filename

    def _txt_confirmation(self):
        def cancel():
            pop_up.grab_release()
            pop_up.destroy()

        pop_up = tk.Toplevel(self._root)
        pop_up.grab_set()
        pop_up.resizable(False, False)
        pop_up.geometry('250x100+100+100')
        l = tk.Label(pop_up, justify=tk.CENTER, text="Запись в формат '.txt' сохранит\n"
                                                     "только текст без форматирования.\n"
                                                     "Продолжить?")
        l.place(x=0, y=0)
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
        if filename is None:
            filename = self._browse_files('o')
        if not filename:
            return None
        ftype = filename.split('.')[-1]
        main_type = self._filetype[1][2:-1]
        if ftype not in ['txt', main_type]:
            info_popup('Данный формат файла не поддерживается')
            return None
        f = open(filename, 'r')
        text = f.read()
        f.close()
        if ftype == main_type:
            char_list = self._parser.parse(text)
            if char_list is None:
                info_popup('Файл поврежден')
        else:
            char_list = self._parser.parse_from_txt(text)
        return char_list

    def save_file(self, char_list: list, filename: str = None):
        if filename is None:
            filename = self._browse_files('s')
        if not filename:
            return 0
        ftype = filename.split('.')[-1]
        main_type = self._filetype[1][2:-1]
        if ftype not in ['txt', main_type]:
            info_popup('Данный формат файла не поддерживается')
            return 0
        if ftype == main_type:
            text = self._serializer.serialize(char_list)
        else:
            if self._txt_confirmation():
                text = self._serializer.serialize_to_txt(char_list)
            else:
                return 0
        f = open(filename, 'w')
        f.write(text)
        f.close()
        info_popup('Файл сохранен')
        return 1


def info_popup(msg: str, title: str = None):
    messagebox.showinfo(title=title, message=msg)


def browse_files(func_type: str):
    if func_type == 'o':
        func = filedialog.askopenfilename
        title = 'Выберите имя файла'
    else:
        func = filedialog.asksaveasfilename
        title = 'Введите имя файла'
    filename = func(initialdir="/",
                    title=title,
                    filetypes=(config.file_format,
                               ("Text files",
                                "*.txt*"),
                               ("all files",
                                "*.*")))
    print(filename)
    return filename


def _get_file_route(win_type: str):
    pop_up = tk.Toplevel()
    pop_up.resizable(False, False)
    pop_up.geometry('250x100')
    route_field = tk.Entry(pop_up, bd=1)
    route_field.place(x=80, y=10, width=80)
    var = tk.IntVar()
    btn = tk.Button(pop_up, fg='blue', command=lambda: var.set(1))
    if win_type == 'o':
        btn.config(text='Открыть')
    else:
        btn.config(text='Сохранить')
    btn.place(x=80, y=50)
    cancel_btn = tk.Button(pop_up, text='Отмена', fg='blue', command=pop_up.destroy)
    cancel_btn.place(x=160, y=50)
    test_btn = tk.Button(pop_up, text='test', command=lambda: browse_files(route_field, win_type))
    test_btn.place(x=0, y=0)
    pop_up.title(f"Введите путь к файлу")
    btn.wait_variable(var)
    path = route_field.get()
    pop_up.destroy()
    return path


def test():
    """Function to test classes' operability"""
    files = RenameIt(tk.Frame())
    open_fname = 'test.txt'
    save_fname = 'test.ppf'
    char_list = files.open_file(open_fname)
    print(char_list)
    status = files.save_file(char_list, save_fname)


if __name__ == '__main__':
    test()
