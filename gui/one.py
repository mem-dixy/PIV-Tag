from Frame import Frame
from list import list
import tkinter
import tkinter.ttk

from PIL import ImageTk
from list import list


class one(Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.button_back = self._init_button("<<", self._button_back)
        self.button_next = self._init_button(">>", self._button_next)
        self.button_quit = self._init_button("Exit Program", self.tk.quit)

    def create_widgets(self, image_list):
        fist = image_list
        fist.reset()
        self.image_list = list()
        self.image_list.add(ImageTk.PhotoImage(fist.get()))
        fist.next()
        self.image_list.add(ImageTk.PhotoImage(fist.get()))
        fist.next()
        self.image_list.add(ImageTk.PhotoImage(fist.get()))
        fist.next()

        #self.image_list = image_list

        self.label_screen = self._init_label(self.image_list.get(), 512, 512)
        self.button_quit.grid(row=0, column=1)
        self.button_back.grid(row=2, column=0)
        self.button_next.grid(row=2, column=2)
        self.label_screen.grid(row=1, column=0, columnspan=3)

    def reset_image(self):
        self.label_screen["image"] = self.image_list.get()

    def _button_back(self):
        self.image_list.back()
        self.reset_image()

    def _button_next(self):
        self.image_list.next()
        self.reset_image()
