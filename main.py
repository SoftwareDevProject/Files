# Main.py
# Written by: Kenneth Hook, Jacob Lee, Samuel Ofori-Addi, Meera Pillai
# Purpose: Adds login lockout and master password reset with predefined security question selection

from tkinter import *
from tkinter import messagebox, simpledialog, ttk
import Encryption
import time

# Globals
failed_attempts = 0
lockout_time = 30  # seconds
lockout_until = None

# Instantiating window frame object
root = Tk()
root.title("Password Manager - Locked")
root.geometry("700x500")

# Clearing window frame object
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Set master password screen
def set_master_password_screen():
    clear_window()
    Label(root, text="Set Master Password", font=("Arial", 14)).pack(pady=10)

    Label(root, text="Password:", font=("Arial", 12)).pack()
    pw_entry = Entry(root, show="*", font=("Arial", 12), width=25)
    pw_entry.pack(pady=5)

    Label(root, text="Confirm Password:", font=("Arial", 12)).pack()
    confirm_entry = Entry(root, show="*", font=("Arial", 12), width=25)
    confirm_entry.pack(pady=5)

    Label(root, text="Select Security Question:", font=("Arial", 12)).pack()
    selected_question = StringVar()
    question_dropdown = ttk.Combobox(root, textvariable=selected_question, width=30, state='readonly')
    question_dropdown['values'] = Encryption.get_all_security_questions()
    question_dropdown.pack(pady=5)

    Label(root, text="Answer:", font=("Arial", 12)).pack()
    sec_a_entry = Entry(root, font=("Arial", 12), width=25)
    sec_a_entry.pack(pady=5)

    # Saving password
    def save_password():
        pw = pw_entry.get()
        confirm = confirm_entry.get()
        question = selected_question.get()
        answer = sec_a_entry.get()

        if not pw or not confirm or not question or not answer:
            messagebox.showwarning("Missing", "All fields are required.")
            return
        if pw != confirm:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return
        Encryption.set_master_password(pw)
        Encryption.set_security_question(question, answer)
        messagebox.showinfo("Success", "Master password set.")
        login_screen()

    Button(root, text="Save", font=("Arial", 12), command=save_password).pack(pady=10)

# Login screen window frame object
def login_screen():
    global failed_attempts, lockout_until
    clear_window()
    Label(root, text="Enter Master Password", font=("Arial", 14)).pack(pady=10)

    pw_entry = Entry(root, show="*", font=("Arial", 12), width=25)
    pw_entry.pack(pady=10)

    def check_password():
        nonlocal pw_entry
        global failed_attempts, lockout_until

        if lockout_until and time.time() < lockout_until:
            remaining = int(lockout_until - time.time())
            messagebox.showerror("Locked Out", f"Too many failed attempts. Try again in {remaining} seconds.")
            return

        pw = pw_entry.get()
        if Encryption.verify_master_password(pw):
            failed_attempts = 0
            root.destroy()
            launch_main_app()
        else:
            failed_attempts += 1
            if failed_attempts >= 3:
                lockout_until = time.time() + lockout_time
                messagebox.showerror("Locked", "Too many failed attempts. Try again later.")
            else:
                remaining = 3 - failed_attempts
                messagebox.showerror("Invalid", f"Wrong password! {remaining} attempts left.")

    Button(root, text="Login", font=("Arial", 12), command=check_password).pack(pady=10)
    Button(root, text="Forgot Password?", font=("Arial", 10), command=reset_password_screen).pack(pady=5)

# Reset password screen
def reset_password_screen():
    clear_window()
    question = Encryption.get_security_question()
    if not question:
        messagebox.showerror("Unavailable", "No security question was set.")
        login_screen()
        return

    Label(root, text="Reset Master Password", font=("Arial", 14)).pack(pady=10)
    Label(root, text="Security Question:\\n" + question, font=("Arial", 12)).pack(pady=5)

    ans_entry = Entry(root, font=("Arial", 12), width=25)
    ans_entry.pack(pady=5)

    Label(root, text="New Password:", font=("Arial", 12)).pack()
    new_pw_entry = Entry(root, show="*", font=("Arial", 12), width=25)
    new_pw_entry.pack(pady=5)

    Label(root, text="Confirm New Password:", font=("Arial", 12)).pack()
    confirm_pw_entry = Entry(root, show="*", font=("Arial", 12), width=25)
    confirm_pw_entry.pack(pady=5)

    # Verifying security answer and resetting password
    def verify_and_reset():
        ans = ans_entry.get()
        new_pw = new_pw_entry.get()
        confirm_pw = confirm_pw_entry.get()

        if not ans or not new_pw or not confirm_pw:
            messagebox.showwarning("Missing", "All fields are required.")
            return

        if new_pw != confirm_pw:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return

        if Encryption.verify_security_answer(ans):
            Encryption.set_master_password(new_pw)
            messagebox.showinfo("Success", "Master password has been reset.")
            login_screen()
        else:
            messagebox.showerror("Incorrect", "Security answer is incorrect.")

    Button(root, text="Reset Password", font=("Arial", 12), command=verify_and_reset).pack(pady=10)

# Launching main app
def launch_main_app():
    import vault_gui
    vault_gui.open_vault()

# Start up logic
if Encryption.master_password_exists():
    login_screen()
else:
    set_master_password_screen()

root.mainloop()
