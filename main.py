from tkinter import *
from tkinter import filedialog

window = Tk()

window.title("Transshipment solver")

window.geometry('350x200')

o_lbl = Label(window, text="Origins")
o_lbl.grid(column=0, row=0)
o_file = None


def o_btn_clicked():
    global o_file
    o_file_2 = filedialog.askopenfilename()
    if o_file_2 is not ():
        o_file = o_file_2
        o_lbl.configure(text="Done !")


o_btn = Button(window, text="Select csv", command=o_btn_clicked)
o_btn.grid(column=1, row=0)

t_lbl = Label(window, text="Transshipments")
t_lbl.grid(column=0, row=1)
t_file = None


def t_btn_clicked():
    global t_file
    t_file_2 = filedialog.askopenfilename()
    if t_file_2 is not ():
        t_file = t_file_2
        t_lbl.configure(text="Done !")


t_btn = Button(window, text="Select csv", command=t_btn_clicked)
t_btn.grid(column=1, row=1)

d_lbl = Label(window, text="Destinations")
d_lbl.grid(column=0, row=2)
d_file = None


def d_btn_clicked():
    global d_file
    d_file_2 = filedialog.askopenfilename()
    if d_file_2 is not ():
        d_file = d_file_2
        d_lbl.configure(text="Done !")


d_btn = Button(window, text="Select csv", command=d_btn_clicked)
d_btn.grid(column=1, row=2)

window.mainloop()