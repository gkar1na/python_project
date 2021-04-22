#!/usr/bin/env python
# coding: utf-8

from tkinter import *
from tkinter.font import Font
import random
import time
import os

# Настройки цветовой гаммы
color_fon = '#D3D3D3'  # цвет фона программы
color_btn = '#A9A9A9'  # цвет кнопок
color_btn_act = color_btn  # цвет кнопок в активном состоянии

# Шрифты
font_text = 'IMPACT'  # шрифт текстов
font_btn = 'garamond'  # шрифт кнопок
font_ans = 'impact'  # шрифт ответов

# Создание окна
root = Tk()
# root.attributes("-fullscreen", True)

x = root.winfo_screenwidth()  # ширина окна
y = root.winfo_screenheight()  # высота окна

canvas = Canvas(root,
                width=x+10,
                height=y+10,
                bd=-5)
canvas.pack()


# canvas.create_text(x / 2,
#                    20 * y / 200,
#                    text='Добро пожаловать!',
#                    fill='black',
#                    font=(font_text, 70),
#                    anchor='center')

# Поле ввода ответа
# Creates a bold font
bold_font = Font(family="Helvetica", size=14, weight="bold")

text = Text()
text.insert("end", "Select part of text and then click 'Bold'...")
text.focus()
text.pack(fill="both", expand=True)

# configuring a tag called BOLD
text.tag_configure("BOLD", font=bold_font)


root.mainloop()
