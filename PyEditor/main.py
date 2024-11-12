from tkinter import Text, filedialog
from customtkinter import *
from PIL import Image
import os
from CTkScrollableDropdown import *
from CTkMenuBar import *
import webbrowser
from CTkMessagebox import CTkMessagebox

tk_title = "\tPyEditor"

set_appearance_mode("dark")
set_default_color_theme("green")
root = CTk()
root.title(tk_title) 
root.iconbitmap("images\\icon.ico")

win_width = root.winfo_screenwidth()
win_height = root.winfo_screenheight()
root.geometry(f'{win_width-350}x{win_height-200}+75+75')

LGRAY = '#3e4042'
DGRAY = '#25292e' 
RGRAY = '#10121f' 

root.config(bg="#25292e")
title_bar = CTkFrame(root, fg_color=RGRAY)

image_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "images")
icon = CTkImage(Image.open(os.path.join(image_path, "icon.png")), size=(40, 40))
settings_image = CTkImage(Image.open(os.path.join(image_path, "setting.png")), size=(38, 38))
close_image = CTkImage(Image.open(os.path.join(image_path, "x.png")), size=(35, 35))

CTkLabel(title_bar, text="", fg_color=RGRAY, image=icon).pack(side=LEFT, padx=6)

# File menus
menu = CTkMenuBar(title_bar, height=10, bg_color=RGRAY, pady=7, padx=5)
file = menu.add_cascade("File", font=("Corbel", 20), hover_color=LGRAY)
edit = menu.add_cascade("Edit", font=("Corbel", 20), hover_color=LGRAY)
help_menu = menu.add_cascade("Help", font=("Corbel", 20), hover_color=LGRAY)
about = menu.add_cascade("About", font=("Corbel", 20), hover_color=LGRAY)

file_values = [" Open                       Ctrl+O", " Save                        Ctrl+S",  " Save as          Ctrl+Shift+S", " Exit                          Ctrl+Q"]
edit_values = [" Undo                      Ctrl+Z", " Cut                         Ctrl+C",  " Paste                     Ctrl+V"]

file_options = {" Open                       Ctrl+O" : "open_file", " Save                        Ctrl+S" : "save_file", " Save as          Ctrl+Shift+S" : "save_as_file", " Exit                          Ctrl+Q" : "exit"}
edit_options = {" Undo                      Ctrl+Z" : "undo", " Cut                         Ctrl+C" : "cut",  " Paste                     Ctrl+V" : "paste", " Find                        Ctrl+F" : "find_text", " Replace          Ctrl+R" : "replace_text"}
about_options = {" About" : "About", " Settings" : "settings"}
help_options = {" View Help" : "view_help", " Source Code" : "source_code"}

def select_option(option):
    if option in file_options:
        action = file_options[option]
    elif option in edit_options:
        action = edit_options[option]
    elif option in about_options:
        action = about_options[option]
    elif option in help_options:
        action = help_options[option]
    else:
        action = None
    
    if action:
        globals()[action]()

def open_file(event=None):
    filepath = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, 'r') as file:
            content = file.read()
            editor.editor.delete('1.0', END)
            editor.editor.insert('1.0', content)
        update_title(filepath)
        global current_file
        current_file = filepath

def save_file(event=None):
    if current_file:
        with open(current_file, 'w') as file:
            file.write(editor.editor.get('1.0', END))
        update_title(current_file)
    else:
        save_as_file()

def save_as_file(event=None):
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, 'w') as file:
            file.write(editor.editor.get('1.0', END))
        update_title(filepath)
        global current_file
        current_file = filepath

def undo(event=None):
    try:
        editor.editor.edit_undo()
    except:
        pass

def cut(event=None):
    try:
        editor.editor.event_generate("<<Cut>>")
    except:
        pass

def paste(event=None):
    try:
        editor.editor.event_generate("<<Paste>>")
    except:
        pass

def exit(event=None):
    root.quit()

def update_title(filepath):
    """Update the title bar with the filename."""
    filename = os.path.basename(filepath)
    title_bar_title.configure(text=f"\t{filename} - PyEditor")

def About():
    editor.display_settings_bar()

def settings():
    editor.display_settings_bar()

def view_help():
    type_frame = CTkToplevel(root, fg_color="#292f35")
    type_frame.overrideredirect(True)

    toplevel_width = 500
    toplevel_height = 500

    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()

    x = root_x + (root_width - toplevel_width) // 2
    y = root_y + (root_height - toplevel_height) // 2

    type_frame.geometry(f"{toplevel_width}x{toplevel_height}+{x}+{y-40}")
    type_frame.resizable(False, False)
    type_frame.attributes("-topmost", True)
    type_frame.grab_set()

    frame = CTkFrame(type_frame, fg_color="#111", border_color="#111", corner_radius=10)
    frame.pack(fill=BOTH, expand=True, padx=0, pady=0)

    # Title Frame
    help_title_frame = CTkFrame(frame, fg_color="#111")
    help_frame = CTkFrame(help_title_frame, fg_color="transparent")
    CTkLabel(help_frame, text="Help", font=("IBM Plex Sans", 30, "bold"), text_color="white").pack(side=LEFT, padx=10)
    CTkButton(
        help_frame,
        text="",
        width=0,
        fg_color="transparent",
        hover_color="#333",
        image=close_image,
        command=lambda: type_frame.destroy()
    ).pack(side=RIGHT)
    help_frame.pack(side=TOP, fill=X, padx=20, pady=10)

    horizontal_line_note_title = CTkFrame(help_title_frame, height=2, fg_color="#a5a5a5")
    horizontal_line_note_title.pack(side=BOTTOM, fill=X, pady=0, padx=0)

    help_title_frame.pack(fill=X, pady=5, padx=0, ipady=0)

    # Shortcuts Section
    scrollable_frame = CTkScrollableFrame(frame, fg_color="#111")
    scrollable_frame.pack(side=TOP, fill=BOTH, expand=True)
    shortcuts_section = CTkFrame(scrollable_frame, fg_color="#111")
    CTkLabel(shortcuts_section, text="Keyboard Shortcuts", font=("IBM Plex Sans", 25, "bold"), text_color="white").pack(pady=10)

    shortcuts = [
        ("Open File", "Ctrl + O"),
        ("Save File", "Ctrl + S"),
        ("Save As", "Ctrl + Shift + S"),
        ("Exit", "Ctrl + Q"),
        ("Undo", "Ctrl + Z"),
        ("Cut", "Ctrl + C"),
        ("Paste", "Ctrl + V"),
        ("Find", "Ctrl + F"),
        ("Replace", "Ctrl + R")
    ]

    for action, shortcut in shortcuts:
        shortcut_frame = CTkFrame(shortcuts_section, fg_color="#292f35", corner_radius=5)
        shortcut_frame.pack(fill=X, padx=20, pady=5, ipady=10, ipadx=20)

        CTkLabel(shortcut_frame, text=action, font=("monospace", 18), text_color="white").pack(side=LEFT, padx=20, pady=5)
        CTkLabel(shortcut_frame, text=f"{shortcut}", font=("monospace", 18), text_color="white").pack(side=RIGHT, padx=20, pady=5)

    shortcuts_section.pack(fill=BOTH, expand=True, pady=0, ipady=10)

    frame.pack(fill=BOTH, expand=True)

def source_code():
    webbrowser.open_new_tab(url="https://github.com/SarthakTools/Spotify")

def on_closing():
    if editor.modified:
        print("Working")
        # response = messagebox.askyesnocancel("Unsaved Changes", "Do you want to save changes before closing?")
        msg = CTkMessagebox(title="Unsaved Changes", message="Do you want to save changes before closing?",
                        icon="question", option_1="Cancel", option_2="No", option_3="Yes", font=("monospace", 15, "bold"), width=400, wraplength=400)
        response = msg.get()
        if response == "Yes":
            save_file()
            root.quit()
        elif response is None:
            return
        else:
            root.quit()
    else:
        root.quit()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Adding the dropdowns
CTkScrollableDropdown(file, values=file_values, width=230, height=500, button_height=40, scrollbar=False, fg_color="#080912", text_color="white",
                       justify="left", button_color="#080912", font=("monospace", 15), command=select_option)
CTkScrollableDropdown(edit, values=edit_values, width=230, height=500, button_height=40, scrollbar=False, fg_color="#080912", text_color="white",
                       justify="left", button_color="#080912", font=("monospace", 15), command=select_option)
CTkScrollableDropdown(help_menu, values=[" View Help", " Source Code"], width=230, height=500, button_height=40, scrollbar=False, fg_color="#080912", text_color="white",
                       justify="left", button_color="#080912", font=("monospace", 15), command=lambda e: select_option(e))
CTkScrollableDropdown(about, values=[" About", " Settings"], width=190, height=500, button_height=40, scrollbar=False, fg_color="#080912", text_color="white",
                       justify="left", button_color="#080912", font=("monospace", 18), command=select_option)

menu.pack(side=LEFT, pady=0, fill=Y)

title_bar_title = CTkLabel(title_bar, text=tk_title, font=("consolas", 20), text_color="white")
title_bar_title.pack(side=LEFT, padx=260)

title_bar.pack(fill=X, padx=3, pady=3, ipady=3)

window = CTkFrame(root, fg_color=DGRAY)
window.pack(expand=True, fill=BOTH)

# Initialize the editor
current_file = None

class MyEditor:
    def __init__(self):
        self.editor_frame = CTkFrame(window, fg_color="#25292e")
        self.editor_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.font_family = "Consolas"
        self.font_size = 17
        self.font_style = "normal"

        frame = CTkFrame(self.editor_frame, fg_color=DGRAY, corner_radius=5)
        self.line_numbers = Text(frame, font=(self.font_family, self.font_size, self.font_style), width=3, padx=4, pady=4, bg="#292f35", fg="#a5a5a5", border=0, state='disabled', cursor="arrow")
        self.line_numbers.pack(side=RIGHT, fill=Y, padx=0)
        frame.pack(side=LEFT, pady=1, fill=Y, padx=0, ipadx=4)

        self.editor = Text(self.editor_frame, font=(self.font_family, self.font_size, self.font_style), bg="#25292e", fg="white", insertbackground="white", undo=True, border=0)
        self.editor.pack(side=LEFT, fill=BOTH, expand=True, pady=1, padx=10)

        self.editor.bind('<<Modified>>', self.on_modify)
        self.editor.bind('<Configure>', self.update_line_numbers)

        self.update_line_numbers()
        self.settings_displayed = False
        self.modified = False

    def on_modify(self, event=None):
        self.modified = True
        self.update_line_numbers()
        self.editor.edit_modified(False)

    def update_line_numbers(self, event=None):
        try:
            self.line_numbers.configure(state='normal')
            self.line_numbers.delete('1.0', END)

            text_content = self.editor.get('1.0', 'end-1c')
            number_of_lines = text_content.count('\n') + 1

            line_numbers_string = '\n'.join(str(i) for i in range(1, number_of_lines + 1))
            self.line_numbers.insert('1.0', line_numbers_string)
            
            self.line_numbers.configure(state='disabled')
            self.line_numbers.see(f"{number_of_lines}.0")
        except:
            pass
    
    def display_settings_bar(self):
        if not self.settings_displayed:
            image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
            close_image = CTkImage(Image.open(os.path.join(image_path, "close_white.png")), size=(30, 30))
            font_image = CTkImage(Image.open(os.path.join(image_path, "font_white.png")), size=(40, 40))

            # Hide the editor frame
            self.editor_frame.pack_forget()
            
            self.settings_frame = CTkFrame(window, fg_color="#202124")

            self.topic_frame = CTkFrame(self.settings_frame, fg_color="transparent", corner_radius=0)
            CTkLabel(self.topic_frame, text="Settings", width=0, fg_color="transparent", font=("IBM Plex Sans", 35, "bold"), text_color="white").pack(side=LEFT, pady=5, padx=20)
            CTkButton(self.topic_frame, text="", image=close_image, width=0, fg_color="transparent", hover_color=LGRAY, command=self.withdraw_settings_bar).pack(side=RIGHT, padx=15)
            self.topic_frame.pack(side=TOP, fill=X, pady=5, padx=5)

            self.font_frame = CTkFrame(self.settings_frame, fg_color="#333")

            CTkLabel(self.font_frame, text=" Font", compound=LEFT, width=0, fg_color="transparent", image=font_image, font=("Poppins", 30, "bold"), text_color="white").pack(side=TOP, anchor="nw", pady=5, padx=20)

            # Initialize option menus only in the settings bar
            family_frame = CTkFrame(self.font_frame, fg_color="transparent")
            CTkLabel(family_frame, text="Family", font=("Poppins", 25, "bold"), text_color="white").pack(side=LEFT)
            self.family = CTkOptionMenu(family_frame, height=38, width=250, font=("Poppins", 20), values=[self.font_family], fg_color="#1f538d", button_color="#14375e", button_hover_color="#1e2c40")
            family_dropdown = CTkScrollableDropdown(self.family, values=["Poppins", "IBM Plex Sans", "monospace", "sans-serif", "Consolas", "Roboto", "Open Sans", "Montserrat", "Raleway"], width=250, height=500, button_height=40, scrollbar=True, fg_color="#080912", text_color="white", justify="left", button_color="#080912", font=("monospace", 15))
            self.family.pack(side=RIGHT)
            family_frame.pack(fill=X, padx=40)

            size_frame = CTkFrame(self.font_frame, fg_color="transparent")
            CTkLabel(size_frame, text="Size", font=("Poppins", 25, "bold"), text_color="white").pack(side=LEFT)
            self.size = CTkOptionMenu(size_frame, height=38, width=250, font=("Poppins", 20), values=[f"{self.font_size}"], fg_color="#1f538d", button_color="#14375e", button_hover_color="#1e2c40")
            size_dropdown = CTkScrollableDropdown(self.size, values=["17", "25", "30", "35", "40"], width=250, height=500, button_height=40, scrollbar=True, fg_color="#080912", text_color="white", justify="left", button_color="#080912", font=("monospace", 15))
            self.size.pack(side=RIGHT)
            size_frame.pack(fill=X, padx=40, pady=10)

            style_frame = CTkFrame(self.font_frame, fg_color="transparent")
            CTkLabel(style_frame, text="Style", font=("Poppins", 25, "bold"), text_color="white").pack(side=LEFT)
            self.style = CTkOptionMenu(style_frame, height=38, width=250, font=("Poppins", 20), values=[self.font_style], fg_color="#1f538d", button_color="#14375e", button_hover_color="#1e2c40")
            style_dropdown = CTkScrollableDropdown(self.style, values=["normal", "italic", "bold"], width=250, height=500, button_height=40, scrollbar=True, fg_color="#080912", text_color="white", justify="left", button_color="#080912", font=("monospace", 15))
            self.style.pack(side=RIGHT)
            style_frame.pack(fill=X, padx=40, pady=5)

            apply_frame = CTkFrame(self.font_frame)
            self.applied_text = CTkLabel(apply_frame, text="I Love Python Programming.", font=(self.font_family, self.font_size, self.font_style))
            self.applied_text.pack(side=LEFT, padx=20)
            CTkButton(apply_frame, text="Set Default", font=("IBM Plex Sans", 15), command=lambda: self.change_font("default")).pack(side=RIGHT, ipady=5, padx=10)
            CTkButton(apply_frame, text="Apply", font=("IBM Plex Sans", 15), command=lambda: self.change_font("apply")).pack(side=RIGHT, ipady=5, padx=5)
            apply_frame.pack(side=BOTTOM, fill=X, padx=150, ipady=10)

            self.font_frame.pack(side=TOP, padx=30, fill=X, pady=5, ipady=10)

            self.about_frame = CTkFrame(self.settings_frame, fg_color="#333")
            
            CTkLabel(self.about_frame, text="About", font=("IBM Plex Sans", 40, "bold"), text_color="white").pack(side=TOP, anchor="nw", padx=20, pady=20)
            CTkLabel(self.about_frame, text="About      : @ 2024 PyEditor Limited. All rights reserved", font=("Consolas", 20, "bold")).pack(side=TOP, anchor="nw", padx=20)
            CTkLabel(self.about_frame, text="Version    : 1.1", font=("Consolas", 20, "bold")).pack(side=TOP, anchor="nw", padx=20)
            CTkLabel(self.about_frame, text="Developer  : Sarthak Singh", font=("Consolas", 20, "bold")).pack(side=TOP, anchor="nw", padx=20)
        
            self.about_frame.pack(side=TOP, fill=BOTH, padx=30, pady=5, ipady=10)

            self.settings_frame.pack(fill=BOTH, expand=True)
            self.settings_displayed = True

    def withdraw_settings_bar(self):
        if self.settings_displayed:
            self.settings_frame.destroy()
            self.editor_frame.pack(side=LEFT, fill=BOTH, expand=True)
            self.editor.bind('<<Modified>>', self.on_modify)
            self.editor.bind('<Configure>', self.update_line_numbers)
            self.update_line_numbers()
            self.settings_displayed = False

    def change_font(self, option):
        if option == "default":
            self.font_family = "Consolas"
            self.font_size = 17
            self.font_style = "normal"
            self.editor.configure(font=(self.font_family, self.font_size, self.font_style))
            self.line_numbers.configure(font=(self.font_family, self.font_size, self.font_style))
            self.applied_text.configure(font=(self.font_family, self.font_size, self.font_style))
        elif option == "apply":
            self.font_family = self.family.get()
            self.font_size = int(self.size.get())
            self.font_style = self.style.get()
            self.editor.configure(font=(self.font_family, self.font_size, self.font_style))
            self.applied_text.configure(font=(self.font_family, self.font_size, self.font_style))
            self.line_numbers.configure(font=(self.font_family, self.font_size, self.font_style))

# Create instance of editor
editor = MyEditor()

# Bind settings button to display settings bar
settings_button = CTkButton(title_bar, text="", image=settings_image, width=50, height=50, fg_color=RGRAY, hover_color=LGRAY, command=editor.display_settings_bar)
settings_button.pack(side=RIGHT, padx=15)

root.bind('<Control-o>', open_file)
root.bind('<Control-s>', save_file)
root.bind('<Control-Shift-s>', save_as_file)
root.bind('<Control-q>', exit)
root.bind('<Control-z>', undo)
root.bind('<Control-x>', cut)
root.bind('<Control-v>', paste)

root.mainloop()