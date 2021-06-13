import tkinter as tk


class RightMenu:
    """Class for copy-paste-cut functions."""
    def __init__(self, root: tk.Tk, text_field: tk.Text):
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

    def paste(self, *args, **kwargs):
        """Paste function."""
        try:
            flag = False
            if flag:
                num_index = 0
                while num_index < len(self.buffer_selected):
                    self.text_field.insert(self.index, self.buffer_selected[num_index])
                    for tag in self.buffer_tags[num_index]:
                        self.text_field.tag_add(tag, self.index)
                    self.index = self.text_field.index(f'{self.index}+1c')
                    num_index += 1
            else:
                index = self.text_field.index(tk.INSERT)
                self.text_field.insert(index, self.buffer_selected)
                num_index = 0
                while self.text_field.compare(index, '<', tk.INSERT):

                    # Remove all tags
                    flag = True
                    while flag:
                        tags = self.text_field.tag_names(index)
                        tag = None
                        for i in range(len(tags)):
                            if (tags[i].find('_') != -1 and tags[i].find('#') != -1) or (tags[i].find('.') != -1):
                                tag = tags[i]
                                break
                        if tag:
                            self.text_field.tag_remove(tag, index)
                        else:
                            flag = False

                    for tag in self.buffer_tags[num_index]:
                        self.text_field.tag_add(tag, index)
                    index = self.text_field.index(f'{index}+1c')
                    num_index += 1
        except tk.TclError:
            pass

    def copy(self, *args, **kwargs):
        """Copy function."""
        try:
            self.buffer_tags = []
            self.buffer_selected = self.text_field.selection_get()
            index = self.text_field.index(f"{tk.SEL_FIRST}")
            while self.text_field.compare(index, '<', tk.SEL_LAST):
                self.buffer_tags.append(self.text_field.tag_names(f'{index}'))
                index = self.text_field.index(f"{index}+1c")
        except tk.TclError:
            pass

    def cut(self, *args, **kwargs):
        """Cut function."""
        try:
            self.buffer_tags = []
            self.buffer_selected = self.text_field.selection_get()
            index = self.text_field.index(f"{tk.SEL_FIRST}")
            while self.text_field.compare(index, '<', tk.SEL_LAST):
                self.buffer_tags.append(self.text_field.tag_names(f'{index}'))
                index = self.text_field.index(f"{index}+1c")
            self.text_field.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass
