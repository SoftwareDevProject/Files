# vault_gui.py
# Written by: Kenneth Hook, Jacob Lee, Samuel Ofori-Addi, Meera Pillai
# Purpose: This code is the GUI file for the application after entering the project from entering the master password. 

from tkinter import *
from tkinter import messagebox, simpledialog, ttk
import Encryption
import random

# Opening display screen object
def open_vault():
    vault = Tk()
    vault.title("🛡️ Password Vault")
    vault.geometry("700x500")
     # Clearing window frame object
    def clear():
        for widget in vault.winfo_children():
            if not isinstance(widget, Menu):
                widget.destroy()
    # Refreshing display
    def refresh():
        clear()
        Label(vault, text="Your Saved Entries", font=("Arial", 14, "bold")).pack(pady=10)

        entries = Encryption.load_entries()

        if not entries:
            Label(vault, text="No entries yet.", font=("Arial", 12)).pack(pady=10)
        else:
            for i, (cat, email, password) in enumerate(entries):
                masked_password = "*" * (len(password) + random.randint(1,10))
                frame = Frame(vault)
                frame.pack(anchor=W, padx=20, pady=2)
                Label(frame, text=f"[{cat}] {email} — {masked_password}", font=("Arial", 11)).grid(row=0, column=0, sticky=W)

                Button(frame, text="Edit", command=lambda idx=i: edit_entry(idx), bg="lightblue").grid(row=0, column=1, padx=5)
                Button(frame, text="Delete", command=lambda idx=i: delete_entry(idx), bg="khaki").grid(row=0, column=2, padx=5)
                Button(frame, text="Reveal Password", command=lambda idx=i: reveal_password(idx), bg="plum2").grid(row=0, column=3, padx=5)
                Button(frame, text="Copy Password", command=lambda idx=i: copy_entry(idx), bg="pale green").grid(row=0,column=4,padx=5)

        button_frame = Frame(vault)
        button_frame.pack(pady=15)

        Button(button_frame, text="➕ Add Entry", command=add_entry, font=("Arial", 12)).grid(row=0, column=0, padx=5)
        Button(button_frame, text="🔍 Search Entry", command=search_entry, font=("Arial", 12)).grid(row=0, column=1, padx=5)
        Button(button_frame, text="🚪 Sign Out", command=sign_out, font=("Arial", 12), bg="gray").grid(row=0, column=2, padx=5)

    # Reveals password
    def reveal_password(index):
        clear()
        Label(vault, text="Your Saved Entries", font=("Arial", 14, "bold")).pack(pady=10)

        entries = Encryption.load_entries()

        if not entries:
            Label(vault, text="No entries yet.", font=("Arial", 12)).pack(pady=10)
        else:
            for i, (cat, email, password) in enumerate(entries):
                masked_password = "*" * (len(password) + random.randint(1,10))
                frame = Frame(vault)
                frame.pack(anchor=W, padx=20, pady=2)
                if i == index:
                    Label(frame, text=f"[{cat}] {email} — {Encryption.decrypt_password(cat,email)}", font=("Arial", 11)).grid(row=0, column=0,sticky=W)
                    Button(frame, text="Edit", command=lambda idx=i: edit_entry(idx), bg="lightblue").grid(row=0,column=1,padx=5)
                    Button(frame, text="Delete", command=lambda idx=i: delete_entry(idx), bg="khaki").grid(row=0,column=2,padx=5)
                    Button(frame, text="Hide Password", command=refresh, bg="plum2").grid(row=0, column=3, padx=5)
                    Button(frame, text="Copy Password", command=lambda idx=i: copy_entry(idx), bg="pale green").grid(row=0, column=4, padx=5)
                else:
                    Label(frame, text=f"[{cat}] {email} — {masked_password}", font=("Arial", 11)).grid(row=0, column=0,sticky=W)
                    Button(frame, text="Edit", command=lambda idx=i: edit_entry(idx), bg="lightblue").grid(row=0,column=1,padx=5)
                    Button(frame, text="Delete", command=lambda idx=i: delete_entry(idx), bg="khaki").grid(row=0,column=2,padx=5)
                    Button(frame, text="Reveal Password", command=refresh, bg="plum2").grid(row=0, column=3, padx=5)
                    Button(frame, text="Copy Password", command=lambda idx=i: copy_entry(idx), bg="pale green").grid(row=0, column=4, padx=5)

            button_frame = Frame(vault)
            button_frame.pack(pady=15)

            Button(button_frame, text="➕ Add Entry", command=add_entry, font=("Arial", 12)).grid(row=0, column=0,padx=5)
            Button(button_frame, text="🔍 Search Entry", command=search_entry, font=("Arial", 12)).grid(row=0, column=1,padx=5)
            Button(button_frame, text="🚪 Sign Out", command=sign_out, font=("Arial", 12), bg="gray").grid(row=0,column=2,padx=5)


    def add_entry(): # Adds entry
        entry_window = Toplevel(vault)
        entry_window.title("Add New Entry")
        entry_window.geometry("300x200")
        entry_window.grab_set()

        Label(entry_window, text="Category:", font=("Arial", 11)).pack(pady=5)
        cat_entry = Entry(entry_window, width=30)
        cat_entry.pack()

        Label(entry_window, text="Email:", font=("Arial", 11)).pack(pady=5)
        email_entry = Entry(entry_window, width=30)
        email_entry.pack()

        Label(entry_window, text="Password:", font=("Arial", 11)).pack(pady=5)
        pw_entry = Entry(entry_window, width=30, show="*")
        pw_entry.pack()

        def save_and_close(): # Saves and closes entry
            cat = cat_entry.get()
            email = email_entry.get()
            password = pw_entry.get()
            if cat and email and password:
                Encryption.encrypt_and_store(cat, email, password)
                messagebox.showinfo("Saved", "Entry added.")
                refresh()
                entry_window.destroy()
            else:
                messagebox.showwarning("Missing", "All fields are required.")

        Button(entry_window, text="Save", command=save_and_close).pack(pady=10)

    def delete_entry(index): # Deletes entry
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?")
        if confirm:
            entries = Encryption.load_entries()
            if 0 <= index < len(entries):
                entries.pop(index)
                Encryption.overwrite_entries(entries)
                messagebox.showinfo("Deleted", "Entry deleted.")
                refresh()

    def edit_entry(index): # Edits entry
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

    def copy_entry(index): # Copies entry
        entries = Encryption.load_entries()
        if 0 <= index < len(entries):
            cat, email, password = entries[index]
            vault.clipboard_clear()
            vault.clipboard_append(password)
            vault.update()

    def search_entry(): # Searches entry
        clear()
        find_entry = simpledialog.askstring("Category", "Enter category name:")
        entries = Encryption.load_entries()
        index = 0
        Label(vault, text="Entries matching search", font=("Arial", 14, "bold")).pack(pady=10)
        for entry in entries:
            cat, email, password = entries[index]
            masked_password = "*" * len(password)
            index += 1
            if cat == find_entry:
                frame = Frame(vault)
                frame.pack(anchor=W, padx=20, pady=2)
                Label(frame, text=f"[{cat}] {email} — {masked_password}", font=("Arial", 11)).grid(row=0, column=0, sticky=W)

                Button(frame, text="Edit", command=lambda idx=index: edit_entry(idx), bg="lightblue").grid(row=0, column=1, padx=5)
                Button(frame, text="Delete", command=lambda idx=index: delete_entry(idx), bg="khaki").grid(row=0, column=2, padx=5)
                Button(frame, text="Reveal Password", command=lambda idx=index: reveal_for_search(index), bg="plum2").grid(row=0, column=3, padx=5)
                Button(frame, text="Copy Password", command=lambda idx=index: copy_entry(idx), bg="pale green").grid(row=0, column=4, padx=5)

        Button(vault, text="Reset", command=refresh, font=("Arial", 12)).pack(pady=15)

    def reveal_for_search(index): # Reveals the password for search (redundant from reveal password method due to this needing to occur only once)
        clear()
        Label(vault, text="Your Saved Entries", font=("Arial", 14, "bold")).pack(pady=10)

        entries = Encryption.load_entries()

        if not entries:
            Label(vault, text="No entries yet.", font=("Arial", 12)).pack(pady=10)
        else:
            for i, (cat, email, password) in enumerate(entries):
                frame = Frame(vault)
                frame.pack(anchor=W, padx=20, pady=2)
                if i == index:
                    Label(frame, text=f"[{cat}] {email} — {Encryption.decrypt_password(cat,email)}", font=("Arial", 11)).grid(row=0, column=0,sticky=W)
                    Button(frame, text="Edit", command=lambda idx=i: edit_entry(idx), bg="lightblue").grid(row=0,column=1,padx=5)
                    Button(frame, text="Delete", command=lambda idx=i: delete_entry(idx), bg="khaki").grid(row=0,column=2,padx=5)
                    Button(frame, text="Hide Password", command=refresh, bg="plum2").grid(row=0, column=3, padx=5)
                    Button(frame, text="Copy Password", command=lambda idx=i: copy_entry(idx),bg="pale green").grid(row=0, column=4, padx=5)

    def sign_out(): # Sign out method
        confirm = messagebox.askyesno("Sign Out", "Are you sure you want to sign out?")
        if confirm:
            vault.destroy()
            import main


    refresh()
    vault.mainloop()
