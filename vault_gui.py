# vault_gui.py
# Written by: Kenneth Hook, Jacob Lee, Samuel Ofori-Addi, Meera Pillai
# Purpose: This code is the GUI file for the application after entering the project from entering the master password. 
from tkinter import *
from tkinter import messagebox, simpledialog
import Encryption

# Opens application
def open_vault():
    vault = Tk()
    vault.title("🛡️ Password Vault")
    vault.geometry("700x500")

    # Clears the application
    def clear():
        for widget in vault.winfo_children():
            if not isinstance(widget, Menu):
                widget.destroy()

    # Refreshes the application
    def refresh():
        clear()
        Label(vault, text="Your Saved Entries", font=("Arial", 14, "bold")).pack(pady=10)

        entries = Encryption.load_entries()

        if not entries:
            Label(vault, text="No entries yet.", font=("Arial", 12)).pack(pady=10)
        else:
            for i, (cat, email, password) in enumerate(entries):
                frame = Frame(vault)
                frame.pack(anchor=W, padx=20, pady=2)
                Label(frame, text=f"[{cat}] {email} — {password}", font=("Arial", 11)).grid(row=0, column=0, sticky=W)

                Button(frame, text="Edit", command=lambda idx=i: edit_entry(idx), bg="lightblue").grid(row=0, column=1, padx=5)
                Button(frame, text="Delete", command=lambda idx=i: delete_entry(idx), bg="tomato").grid(row=0, column=2, padx=5)

        Button(vault, text="➕ Add Entry", command=add_entry, font=("Arial", 12)).pack(pady=15)

    # Adds an entry
    def add_entry():
        cat = simpledialog.askstring("Category", "Enter category:")
        email = simpledialog.askstring("Email", "Enter email:")
        password = simpledialog.askstring("Password", "Enter password:", show="*")
        if cat and email and password:
            Encryption.encrypt_and_store(cat, email, password)
            messagebox.showinfo("Saved", "Entry added.")
            refresh()
        else:
            messagebox.showwarning("Missing", "All fields are required.")

    # Deletes an entry
    def delete_entry(index):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?")
        if confirm:
            entries = Encryption.load_entries()
            if 0 <= index < len(entries):
                entries.pop(index)
                Encryption.overwrite_entries(entries)
                messagebox.showinfo("Deleted", "Entry deleted.")
                refresh()

    # Edits an entry
    def edit_entry(index):
        entries = Encryption.load_entries()
        if 0 <= index < len(entries):
            cat, email, password = entries[index]
            new_email = simpledialog.askstring("Edit Email", "Update Email:", initialvalue=email)
            new_password = simpledialog.askstring("Edit Password", "Update Password:", initialvalue=password, show="*")
            if new_email and new_password:
                entries[index] = (cat, new_email, new_password)
                Encryption.overwrite_entries(entries)
                messagebox.showinfo("Updated", "Entry updated.")
                refresh()

    refresh()
    vault.mainloop()
