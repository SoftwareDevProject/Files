# Import Module
from tkinter import *

# create root window
root = Tk()

# root window title and dimension
root.title("Example")
# Set geometry (widthxheight)
root.geometry('500x400')

menu = Menu(root)
item = Menu(menu)
item.add_command(label='New')
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)

# adding a label to the root window
lbl = Label(root, text = "Enter data")
lbl.grid()

txt = Entry(root, width=10)
txt.grid(column =1, row =0)

def clicked():
    lbl.configure(text = "Data has been entered")
    newlbl = Label(root, text = "You entered " + txt.get())
    newlbl.grid(column=1,row=1)
    txt.delete(0, END)
    txt.insert(0,"")



# button widget with red color text
# inside
btn = Button(root, text = "Enter" ,
             fg = "red", command=clicked)
# set Button grid
btn.grid(column=2, row=0)

# all widgets will be here
# Execute Tkinter
root.mainloop()
