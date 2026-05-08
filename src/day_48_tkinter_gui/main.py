# src/day_48_tkinter_gui/main.py
"""
Day 48: Creating Desktop GUI Apps with Tkinter
"""

import tkinter as tk
from tkinter import messagebox

def main():
    print("Welcome to Day 48 – Tkinter GUI Apps")
    print("Launching a simple GUI window...\n")

    try:
        root = tk.Tk()
        root.title("My First Tkinter App - Day 48")
        root.geometry("400x300")

        def show_message():
            messagebox.showinfo("Hello", "Welcome to Python GUI Programming!")

        label = tk.Label(root, text="Hello from Tkinter!", font=("Arial", 14))
        label.pack(pady=20)

        button = tk.Button(root, text="Click Me!", command=show_message, bg="lightblue")
        button.pack(pady=10)

        root.mainloop()
    except Exception as e:
        print(f"GUI Error: {e}")
        print("Tkinter may not be available in this environment.")


if __name__ == "__main__":
    main()