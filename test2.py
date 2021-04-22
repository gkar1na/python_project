#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
from tkinter.font import Font, BOLD, ITALIC, ROMAN, NORMAL


class Pad(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.toolbar = tk.Frame(self, bg="#eee")
        self.toolbar.pack(side="top", fill="x")

        self.option_list = [
            'Выбрать курсив',
            'bold',
            'no bold'
        ]

        # self.variable = tk.StringVar(self.toolbar)
        # self.variable.set(self.option_list[0])
        # self.opt = tk.OptionMenu(self.toolbar, self.variable, *self.option_list)
        # self.opt.config(width=90, font=('Helvetica', 12))
        # self.opt.pack()

        # self.bold_btn = tk.Button(self.toolbar, text="Bold", command=self.make_bold)
        # self.bold_btn.pack(side="left")
        #
        # self.clear_btn = tk.Button(self.toolbar, text="Clear", command=self.clear)
        # self.clear_btn.pack(side="left")



        # Creates a bold font
        self.bold_font = Font(self, family="Helvetica", size=14, weight="bold")
        self.italic_font = Font(self, family="Helvetica", size=14, weight="normal", slant=ITALIC)

        self.text = tk.Text(self)
        self.text.insert("end", "Select part of text and then click 'Bold'...")
        self.text.focus()

        # create a Scrollbar and associate it with txt
        self.scrollb = tk.Scrollbar(self, command=self.text.yview)
        self.scrollb.pack(side="right", fill='y')
        self.text['yscrollcommand'] = self.scrollb.set

        self.text.pack(fill="both", expand=True)

        # configuring a tag called BOLD
        self.text.tag_configure("BOLD", font=self.bold_font)
        self.text.tag_configure("italic", font=self.italic_font)


        # создаем объект меню на главном окне
        self.m = tk.Menu(self.toolbar)

        # окно конфигурируется с указанием меню для него
        self.parent.config(menu=self.m)

        # создается пункт меню с размещением на основном меню (m)
        self.fm = tk.Menu(self.m)
        self.m.add_cascade(label="Файл", menu=self.fm)
        self.fm.add_command(label="Открыть...")
        self.fm.add_command(label="Создать", command=self.new_win)
        self.fm.add_command(label="Сохранить...")

        # # вложенное меню
        # self.nfm = tk.Menu(self.fm)
        # # fm.add_cascade(label="Import", menu=nfm)
        # self.nfm.add_command(label="Image")
        # self.nfm.add_command(label="Text")

        self.fm.add_command(label="Выход", command=self.close_win)



        # второй пункт меню
        self.text_type = tk.Menu(self.m)
        self.m.add_cascade(label="Начертание", menu=self.text_type)
        self.text_type.add_command(label="Жирный", command=self.make_bold)
        self.text_type.add_command(label="Курсив", command=self.make_italic)
        self.text_type.add_command(label="Подчеркнутый")

        # третий пункт меню
        self.text_font = tk.Menu(self.m)
        self.m.add_cascade(label="Шрифт", menu=self.text_font)
        self.text_font.add_command(label="Calibri")
        self.text_font.add_command(label="Arial")

        # четвертый пункт меню
        self.text_size = tk.Menu(self.m)
        self.m.add_cascade(label="Размер", menu=self.text_size)
        self.text_size.add_command(label="14")
        self.text_size.add_command(label="40")
        self.text_size.add_command(label="80")

        # последний пункт меню
        hm = tk.Menu(self.m)
        self.m.add_cascade(label="?", menu=hm)
        hm.add_command(label="Справка")
        hm.add_command(label="О программе", command=self.about)

    def make_bold(self):
        # tk.TclError exception is raised if not text is selected
        try:
            self.bold_font['size'] = 80
            self.text.tag_add("BOLD", "sel.first", "sel.last")
        except tk.TclError:
            pass

    def make_italic(self):
        # tk.TclError exception is raised if not text is selected
        try:
            self.bold_font['size'] = 40
            self.text.tag_add("italic", "sel.first", "sel.last")
        except tk.TclError:
            pass

    def clear(self):
        self.text.tag_remove("BOLD",  "sel.first", "sel.last")
        # print(self.text.info())
        # i1, i2 = self.text.index("sel.first"), self.text.index("sel.last")
        # for i in range(i1, i2+1):
        #     clear_symbol(i)

    # функции для обработки пунктов меню
    # Пункт меню: Создать
    def new_win(self):
        demo()

    # Пункт меню: Выход
    def close_win(self):
        self.parent.destroy()

    # Пункт меню: О программе
    def about(self):
        self.win = tk.Toplevel(self.toolbar)
        self.win.title("О программе")
        self.win.geometry("300x150")
        self.lab = tk.Label(self.win, text="Версия программы 1.0")
        self.lab.pack()



def clear_symbol(index):
    symbols = []
    symbols[index].no_bold()
    pass


def demo():
    root = tk.Tk()
    root.title("Текстовый редактор")
    Pad(root).pack(expand=1, fill="both")
    root.mainloop()


if __name__ == "__main__":
    demo()
