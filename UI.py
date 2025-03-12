# Import Module
from tkinter import *
import Encryption # importing encryption file and its methods

# Function for when enter button is clicked
def clicked(email_txt, password_txt):
    email = email_txt.get()
    password = password_txt.get()
    Encryption.encrypt(email, password)
    email_txt.delete(0, END)
    email_txt.insert(0, "")
    password_txt.delete(0, END)
    password_txt.insert(0, "")

# Function for creating an entry
def create_entry():
    email_label = Label(root, text="Email:")
    email_label.grid(column=1, row =0)
    email_txt = Entry(root, width=10)
    email_txt.grid(column=2, row=0)
    password_label = Label(root, text="Password:")
    password_label.grid(column=1, row=1)
    password_txt = Entry(root, width=10)
    password_txt.grid(column=2, row=1)

    new_btn = Button(root, text="Enter",
                 fg="red", command=lambda: clicked(email_txt,password_txt))
    # set Button grid
    new_btn.grid(column=1, row=3)

# Function for displaying entries
def display_entries():
    file = open("entries.txt" , "w")

# create root window
root = Tk()

# root window title and dimension
root.title("Example")
# Set geometry (widthxheight)
root.geometry('500x400')

menu = Menu(root)
item = Menu(menu)
item.add_command(label='New Entry', command = create_entry)
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)


root.mainloop()
