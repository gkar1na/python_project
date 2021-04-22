#!/usr/bin/env python
# coding: utf-8


from tkinter import *

# функции для обработки пунктов меню
# Пункт меню: Создать
def new_win():
  win = Toplevel(root)
  win.title("Окно создания")
  win.minsize(width=300, height=150)

# Пункт меню: Выход
def close_win():
  root.destroy()

# Пункт меню: О программе
def about():
  win = Toplevel(root)
  win.geometry("300x150")
  lab = Label(win, text="Версия программы 1.0")
  lab.pack()

# создаем главное окно программы
root = Tk()
root.title("Заголовок окна программы") #заголовок окна
root.geometry("400x200") # начальные размеры окна

# создаем объект меню на главном окне
m = Menu(root)

# окно конфигурируется с указанием меню для него
root.config(menu=m)

# создается пункт меню с размещением на основном меню (m)
fm = Menu(m)
m.add_cascade(label="Файл", menu=fm)
fm.add_command(label="Открыть...")
fm.add_command(label="Создать", command=new_win)
fm.add_command(label="Сохранить...")

# вложенное меню
nfm = Menu(fm)
fm.add_cascade(label="Import", menu=nfm)
nfm.add_command(label="Image")
nfm.add_command(label="Text")

fm.add_command(label="Выход", command=close_win)

# второй пункт меню
hm = Menu(m)
m.add_cascade(label="?", menu=hm)
hm.add_command(label="Справка")
hm.add_command(label="О программе", command=about)

root.mainloop()