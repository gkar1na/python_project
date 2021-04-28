#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
from tkinter.font import Font, BOLD, ITALIC, ROMAN, NORMAL, names, nametofont
from pony.orm import *
import db
import config

@db_session
class Pad(tk.Frame):

    def __init__(self, parent: tk.Tk, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.toolbar = tk.Frame(self, bg="#eee")
        self.toolbar.pack(side="top", fill="x")


        # self.variable = tk.StringVar(self.toolbar)
        # self.variable.set(self.option_list[0])
        # self.opt = tk.OptionMenu(self.toolbar, self.variable, *self.option_list)
        # self.opt.config(width=90, font=('Helvetica', 12))
        # self.opt.pack()

        self.symbols = [
            []
        ]

        # self.family = config.family
        # self.size = config.size
        # self.weight = config.weight

        self.current_font_ID = config.default_font
        self.current_font = self.create_font(self.current_font_ID)


        # Creates a bold font
        # self.default_font = Font(
        #     self,
        #     family=self.current_font['family'],
        #     size=self.current_font['size'],
        #     weight=self.current_font['weight'],
        #     slant=self.current_font['slant']
        # )
        # self.italic_font = Font(
        #     self,
        #     family='Helvetica',
        #     size=14,
        #     weight='normal',
        #     slant=ITALIC
        # )

        self.text = tk.Text(self)
        self.text.configure(font=self.current_font)
        self.text.insert("end", "Test text\nqwertyuiop\nasdfghjkl\nzxcvbnm")
        self.text.focus()

        # create a Scrollbar and associate it with txt
        self.scrollb = tk.Scrollbar(self, command=self.text.yview)
        self.scrollb.pack(side="right", fill='y')
        self.text['yscrollcommand'] = self.scrollb.set

        self.text.pack(fill="both", expand=True)

        # configuring a tag called BOLD
        for font in set(select(font.id for font in db.Font)):
            self.text.tag_configure(font, font=self.create_font(font))
        # self.text.tag_configure('current', font=self.current_font)
        # self.text.tag_configure("bold", font=self.bold_font)
        # self.text.tag_configure("italic", font=self.italic_font)

        for color in set(select(color.id for color in db.Color)):
            self.text.tag_configure(f'{color}_fore', foreground=color)
            self.text.tag_configure(f'{color}_back', background=color)

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
        self.fm.add_separator()
        self.fm.add_command(label="Выход", command=self.close_win)

        # второй пункт меню
        self.text_type = tk.Menu(self.m)
        self.m.add_cascade(label="Начертание", menu=self.text_type)
        self.text_type.add_command(label="Жирный", command=lambda: self.make_font(self.change_weight))
        self.text_type.add_command(label="Курсив", command=lambda: self.make_font(self.change_slant))
        self.text_type.add_command(label="Подчеркнутый", command=lambda: self.make_font(self.change_underline))
        self.text_type.add_command(label="Что-то", command=lambda: self.make_font(self.change_overstrike))

        # третий пункт меню
        self.text_font = tk.Menu(self.m)
        self.m.add_cascade(label="Шрифт", menu=self.text_font)
        self.text_font.add_command(label='Calibri', command=lambda: self.make_font(self.change_family, 'Calibri'))
        self.text_font.add_command(label='Arial', command=lambda: self.make_font(self.change_family, 'Arial'))
        self.text_font.add_command(label='Helvetica', command=lambda: self.make_font(self.change_family, 'Helvetica'))

        # четвертый пункт меню
        self.text_size = tk.Menu(self.m)
        self.m.add_cascade(label="Размер", menu=self.text_size)
        self.text_size.add_command(label='10', command=lambda: self.make_font(self.change_size, '10'))
        self.text_size.add_command(label='12', command=lambda: self.make_font(self.change_size, '12'))
        self.text_size.add_command(label='14', command=lambda: self.make_font(self.change_size, '14'))
        self.text_size.add_command(label='18', command=lambda: self.make_font(self.change_size, '18'))
        self.text_size.add_command(label='24', command=lambda: self.make_font(self.change_size, '24'))
        self.text_size.add_command(label='28', command=lambda: self.make_font(self.change_size, '28'))
        self.text_size.add_command(label='30', command=lambda: self.make_font(self.change_size, '30'))
        self.text_size.add_command(label='34', command=lambda: self.make_font(self.change_size, '34'))
        self.text_size.add_command(label='48', command=lambda: self.make_font(self.change_size, '48'))
        self.text_size.add_command(label='54', command=lambda: self.make_font(self.change_size, '54'))
        self.text_size.add_command(label='60', command=lambda: self.make_font(self.change_size, '60'))
        self.text_size.add_command(label='74', command=lambda: self.make_font(self.change_size, '74'))

        self.text_color_fore = tk.Menu(self.m)
        self.m.add_cascade(label='Цвет текста', menu=self.text_color_fore)
        self.text_color_fore.add_command(label='Красный',
                                         command=lambda: self.make_font(self.change_color_fore, '#ff0000'))
        self.text_color_fore.add_command(label='Зеленый',
                                         command=lambda: self.make_font(self.change_color_fore, '#00ff00'))
        self.text_color_fore.add_command(label='Синий',
                                         command=lambda: self.make_font(self.change_color_fore, '#0000ff'))
        self.text_color_fore.add_command(label='Белый',
                                         command=lambda: self.make_font(self.change_color_fore, '#ffffff'))
        self.text_color_fore.add_command(label='Черный',
                                         command=lambda: self.make_font(self.change_color_fore, '#000000'))

        self.text_color_back = tk.Menu(self.m)
        self.m.add_cascade(label='Цвет фона', menu=self.text_color_back)
        self.text_color_back.add_command(label='Красный',
                                         command=lambda: self.make_font(self.change_color_back, '#ff0000'))
        self.text_color_back.add_command(label='Зеленый',
                                         command=lambda: self.make_font(self.change_color_back, '#00ff00'))
        self.text_color_back.add_command(label='Синий',
                                         command=lambda: self.make_font(self.change_color_back, '#0000ff'))
        self.text_color_back.add_command(label='Белый',
                                         command=lambda: self.make_font(self.change_color_back, '#ffffff'))
        self.text_color_back.add_command(label='Черный',
                                         command=lambda: self.make_font(self.change_color_back, '#000000'))

        # последний пункт меню
        hm = tk.Menu(self.m)
        self.m.add_cascade(label="?", menu=hm)
        hm.add_command(label="Справка")
        hm.add_command(label="О программе", command=self.about)

        self.parent.bind("<Key>", self.action)
        self.parent.bind("<ButtonRelease>", self.action)


    def create_font(self, ID: str):
        family = get(font.family for font in db.Font if font.id == ID)
        size = get(font.size for font in db.Font if font.id == ID)
        weight = get(font.weight for font in db.Font if font.id == ID)
        slant = get(font.slant for font in db.Font if font.id == ID)
        underline = get(font.underline for font in db.Font if font.id == ID)
        overstrike = get(font.overstrike for font in db.Font if font.id == ID)

        font = Font(
            family=family,
            size=size,
            weight=weight,
            slant=slant,
            underline=underline,
            overstrike=overstrike
        )

        return font

    def change_family(self, family, size, weight, slant, underline, overstrike,  new_family, *args):
        family = new_family
        return family, size, weight, slant, underline, overstrike

    def change_size(self, family, size, weight, slant, underline, overstrike, new_size, *args):
        size = new_size
        return family, size, weight, slant, underline, overstrike

    def change_weight(self, family, size, weight, slant, underline, overstrike, *args):
        weight = 'b' if weight == 'n' else 'n'
        return family, size, weight, slant, underline, overstrike

    def change_slant(self, family, size, weight, slant, underline, overstrike, *args):
        slant = 'r' if slant == 'i' else 'i'
        return family, size, weight, slant, underline, overstrike

    def change_underline(self, family, size, weight, slant, underline, overstrike, *args):
        underline = '1' if underline == '0' else '0'
        return family, size, weight, slant, underline, overstrike

    def change_overstrike(self, family, size, weight, slant, underline, overstrike, *args):
        overstrike = '1' if overstrike == '0' else '0'
        return family, size, weight, slant, underline, overstrike

    def change_color_fore(self, family, size, weight, slant, underline, overstrike, new_color_fore, index, *args):
        # print(new_color_fore, index)
        try:
            tags = self.text.tag_names(index)
            tag = None
            for i in range(len(tags)):
                if tags[i].find('_fore') != -1 and tags[i].find('#') != -1:
                    tag = tags[i]
                    break
            if tag:
                self.text.tag_remove(tag, index)
        except:
            pass
        self.text.tag_add(f'{new_color_fore}_fore', index)
        return family, size, weight, slant, underline, overstrike

    def change_color_back(self, family, size, weight, slant, underline, overstrike, new_color_back, index, *args):
        # print(new_color_back, index)
        try:
            tags = self.text.tag_names(index)
            tag = None
            for i in range(len(tags)):
                if tags[i].find('_back') != -1 and tags[i].find('#') != -1:
                    tag = tags[i]
                    break
            if tag:
                self.text.tag_remove(tag, index)
        except:
            pass

        self.text.tag_add(f'{new_color_back}_back', index)
        return family, size, weight, slant, underline, overstrike


    def make_font(self, func, new_value=None):
        try:
            index = self.text.index(f"{tk.SEL_FIRST}")
            while self.text.compare(index, '<', tk.SEL_LAST):
                tags = list(self.text.tag_names(index))
                try:
                    tag = None
                    tags.remove('sel')
                    for i in range(len(tags)):
                        if tags[i].find('.') != -1:
                            tag = tags[i]
                            break
                    if tag:
                        self.text.tag_remove(tag, index)
                    else:
                        tag = self.current_font_ID
                except:
                    tag = self.current_font_ID
                family, size, weight, slant, underline, overstrike = func(*map(str, tag.split('.')), new_value, index)
                tag = f'{family}.{size}.{weight}.{slant}.{underline}.{overstrike}'
                self.text.tag_add(tag, index)
                tags = list(self.text.tag_names(index))
                print('-'*100)
                print(index)
                print(tags)
                index = self.text.index(f"{index}+1c")
        except tk.TclError:
            pass

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

    def action(self, event: tk.Event):
        row, column = map(int, self.text.index(tk.INSERT).split('.'))
        try:
            print(f'select from {self.text.index(tk.SEL_FIRST)} to {self.text.index(tk.SEL_LAST)}')
        except:
            pass
        finally:
            print(f'current cursor position: {row}.{column}')


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
