import tkinter as tk

window = tk.Tk()
window.title("My First UI")
window.geometry("300x200")  # Set window size

label = tk.Label(window, text="Enter your name:")
label.pack()  # Place the label in the window

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Submit", command=lambda: print("Name:", entry.get()))
button.pack()
