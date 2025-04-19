import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from spellchecker import SpellChecker

# Create main window
root = tk.Tk()
root.title("Smart Text Editor")
root.geometry("800x600")

# Spell Checker
spell = SpellChecker()

# Themes
dark_mode = False

# Create Text Area
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, undo=True, font=("Arial", 12))
text_area.pack(fill=tk.BOTH, expand=True)

# File Functions
def new_file():
    text_area.delete(1.0, tk.END)
    root.title("Untitled - Smart Text Editor")

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())
            root.title(f"{file_path} - Smart Text Editor")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))
            root.title(f"{file_path} - Smart Text Editor")

# Spell Check
def spell_check():
    text = text_area.get(1.0, tk.END)
    words = text.split()
    misspelled = spell.unknown(words)

    message = "Misspelled words:\n" + "\n".join(misspelled) if misspelled else "No spelling errors found."
    messagebox.showinfo("Spell Check", message)

# Theme Toggle
def toggle_theme():
    global dark_mode
    if not dark_mode:
        text_area.config(bg="#2e2e2e", fg="#ffffff", insertbackground="white")
        dark_mode = True
    else:
        text_area.config(bg="white", fg="black", insertbackground="black")
        dark_mode = False

# Menu Bar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", command=text_area.edit_undo)
edit_menu.add_command(label="Redo", command=text_area.edit_redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=lambda: text_area.event_generate("<<Cut>>"))
edit_menu.add_command(label="Copy", command=lambda: text_area.event_generate("<<Copy>>"))
edit_menu.add_command(label="Paste", command=lambda: text_area.event_generate("<<Paste>>"))

tools_menu = tk.Menu(menu_bar, tearoff=0)
tools_menu.add_command(label="Spell Check", command=spell_check)
tools_menu.add_command(label="Toggle Theme", command=toggle_theme)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
menu_bar.add_cascade(label="Tools", menu=tools_menu)

root.config(menu=menu_bar)

# Run App
root.mainloop()
