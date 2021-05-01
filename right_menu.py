import tkinter as tk

class RightMenu:
    """Class for copy-paste-cut functional"""
    def __init__(self, root, text_field: tk.Text):
        self.text_field: tk.Text = text_field
        self.buffer_tags = []
        self.buffer_selected = None
        self.menu = tk.Menu(root, tearoff=False)
        self.menu.add_command(label="Вырезать", command=self.cut)
        self.menu.add_command(label="Копировать", command=self.copy)
        self.menu.add_command(label="Вставить", command=self.paste)
        root.bind("<Button-3>", self.popup)
    
    def popup(self, e):
        """show right click menu"""
        self.menu.tk_popup(e.x_root, e.y_root)

    def paste(self):
        """paste functional"""
        print("PASTE")
        first_index = self.text_field.index(tk.INSERT)
        self.text_field.insert(first_index, self.buffer_selected)
        last_index = self.text_field.index(tk.INSERT)
        (first_row, first_collumn) = first_index.split('.')
        (last_row, last_collumn) = last_index.split('.')
        k = 0
        for i in range(int(first_row), int(last_row)+1):
            for j in range(int(first_collumn), int(last_collumn)):
                tags = self.buffer_tags[k]
                print('PASTE process: current tag: ',tags, 'I: ', k)
                for tag in tags:
                    if tag == 'sel':
                        continue
                    self.text_field.tag_add(tag, f'{i}.{j}')
                k += 1

    def copy(self, delete=False):
        """copy functional"""
        print("COPY")
        self.buffer_tags = []
        self.buffer_selected = self.text_field.selection_get()
        first_index = self.text_field.index(tk.SEL_FIRST)
        last_index = self.text_field.index(tk.SEL_LAST)
        (first_row, first_collumn) = first_index.split('.')
        (last_row, last_collumn) = last_index.split('.')
        for i in range(int(first_row), int(last_row)+1):
            for j in range(int(first_collumn), int(last_collumn)):
                self.buffer_tags.append(self.text_field.tag_names(f'{i}.{j}'))
        if delete:
            self.text_field.delete(first_index, last_index)
    def cut(self):
        """cut functional"""
        self.copy(delete=True)
