# Main.py
# Written by: Kenneth Hook, Jacob Lee, Samuel Ofori-Addi, Meera Pillai
# Purpose: This code is the main file for this project. Upon running, this file will start the application.

# Imports
from tkinter import *
from tkinter import simpledialog, messagebox
import Encryption

# App window
root = Tk()
root.title("Password Manager - Locked")
root.geometry("400x250")

# Helper to clean screen
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Screen to set a new master password
def set_master_password_screen():
    clear_window()
    Label(root, text="Set Master Password", font=("Arial", 14)).pack(pady=10)

    pw_entry = Entry(root, show="*", font=("Arial", 12), width=25)
    pw_entry.pack(pady=5)

    confirm_entry = Entry(root, show="*", font=("Arial", 12), width=25)
    confirm_entry.pack(pady=5)

    # Saving master password
    def save_password():
        pw = pw_entry.get()
        confirm = confirm_entry.get()
        if not pw or not confirm:
            messagebox.showwarning("Missing", "Please fill in both fields.")
            return
        if pw != confirm:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return
        Encryption.set_master_password(pw)
        messagebox.showinfo("Success", "Master password set.")
        login_screen()

    Button(root, text="Save", font=("Arial", 12), command=save_password).pack(pady=10)

# Screen to enter existing master password
def login_screen():
    clear_window()
    Label(root, text="Enter Master Password", font=("Arial", 14)).pack(pady=10)

    pw_entry = Entry(root, show="*", font=("Arial", 12), width=25)
    pw_entry.pack(pady=10)

    def check_password():
        pw = pw_entry.get()
        if Encryption.verify_master_password(pw):
            root.destroy()
            launch_main_app()
        else:
            messagebox.showerror("Invalid", "Wrong master password!")

    Button(root, text="Login", font=("Arial", 12), command=check_password).pack(pady=10)

# Launch vault GUI after successful login
def launch_main_app():
    import vault_gui
    vault_gui.open_vault()

# Startup logic
if Encryption.master_password_exists():
    login_screen()
else:
    set_master_password_screen()

root.mainloop()
