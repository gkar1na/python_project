import tkinter as tk


class RightMenu:
    """Class for copy-paste-cut functions."""
    def __init__(self, root, text_field: tk.Text):
        self.root = root
        self.text_field = text_field
        self.buffer_tags = []
        self.buffer_selected = None
        self.menu = tk.Menu(root, tearoff=False)
        self.menu.add_command(label="Вырезать", command=self.cut)
        self.menu.add_command(label="Копировать", command=self.copy)
        self.menu.add_command(label="Вставить", command=self.paste)
        self.root.bind("<Button-2>", self.popup)
        self.root.bind("<Button-3>", self.popup)

    def popup(self, e):
        """Show right click menu."""
        self.menu.tk_popup(e.x_root, e.y_root)

    def paste(self):
        """Paste function."""
        print("PASTE")
        first_index = self.text_field.index(tk.INSERT)
        self.text_field.insert(first_index, self.buffer_selected)
        last_index = self.text_field.index(tk.INSERT)
        (first_row, first_column) = first_index.split('.')
        (last_row, last_column) = last_index.split('.')
        k = 0
        for i in range(int(first_row), int(last_row)+1):
            for j in range(int(first_column), int(last_column)):
                tags = self.buffer_tags[k]
                print('PASTE process: current tag: ', tags, 'I: ', k)
                for tag in tags:
                    # if tag == 'sel':
                    #     continue
                    self.text_field.tag_add(tag, f'{i}.{j}')
                k += 1

    def copy(self, delete=False):
        """Copy function."""
        print("COPY")
        self.buffer_tags = []
        self.buffer_selected = self.text_field.selection_get()
        first_index = self.text_field.index(tk.SEL_FIRST)
        last_index = self.text_field.index(tk.SEL_LAST)
        (first_row, first_column) = first_index.split('.')
        (last_row, last_column) = last_index.split('.')
        for i in range(int(first_row), int(last_row)+1):
            for j in range(int(first_column), int(last_column)):
                self.buffer_tags.append(self.text_field.tag_names(f'{i}.{j}'))
        if delete:
            self.text_field.delete(first_index, last_index)

    def cut(self):
        """Cut function."""
        self.copy(delete=True)
