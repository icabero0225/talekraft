from tkinter import *
from tkinter import ttk
import os

class Chapter:
    def __init__(self, project, chapter):
        self.project = project
        self.chapter = chapter

class Section:
    def __init__(self, chapter, section):
        self.chapter = chapter
        self.section = section

def remove_extension(text, chars=3):
    return text[:-chars-1]

in_menu = False
tabwidth = 8

os.makedirs("Projects", exist_ok=True)

root = Tk()
root.overrideredirect(True)
root.geometry("800x480+345+25")

sidebar = Toplevel()
sidebar.overrideredirect(True)
sidebar.geometry("320x480+25+25")
sidebar.option_add("*Font", "Garamond")

project_view = Frame(sidebar)
project_view.pack(expand=True, fill=BOTH)

current_font = "Garamond"

# Set default font for the text widget
default_font_size = 14
default_font = (current_font, default_font_size)



"""Sidebar Logic"""
def go_back_func():
    print("Go Back")

def hide_chap_popup():
    new_chapter_label.place_forget()
    new_chapter_name.place_forget()
    add_new_chapter.place_forget()
    new_chapter_name.delete(0, END)
    cancel_add_new_chapter.place_forget()
    new_chapter_error.place_forget()
    current_width = add_chap_popup.winfo_width()
    current_height = add_chap_popup.winfo_height()

    if current_width > 1 and current_height > 1:
        print(f"Current: {current_width}x{current_height}")
        new_width = max(current_width - 32/2, 1)
        new_height = max(current_height - 48/2, 1)
        add_chap_popup.config(width=new_width, height=new_height)
        sidebar.after(7, hide_chap_popup)
    else:
        in_menu = False
        add_chap_popup.config(width=0, height=0)

def add_chap_func():

    for char in new_chapter_name.get():
        if char in unacceptable_file_chars:
            populate_chapter_popup(f"Invalid Char: {char}")
            return

    if not new_chapter_name.get().strip():
        populate_chapter_popup("Chapter name cannot be empty!")
        return

    for chapter in chapters:
        if new_chapter_name.get() == chapter.chapter:
            populate_chapter_popup("Chapter already exists!")
            return

    os.makedirs(os.path.join("Projects", current_project, new_chapter_name.get()))
    refresh_project_view()
    add_new_chapter.focus_set()
    hide_chap_popup()

def expand_chap_popup(message = ""):
    in_menu = True
    target_width = 320 - 32*2.5
    target_height = 480 - 48*2.5

    def animate():
        print(f"Current Width: {add_chap_popup.winfo_width()}, Target Width: {target_width}")
        current_width = add_chap_popup.winfo_width()
        current_height = add_chap_popup.winfo_height()

        if current_width < target_width or current_height < target_height:
            new_width = min(target_width, current_width + 32/2)
            new_height = min(target_height, current_height + 48/2)
            add_chap_popup.config(width=new_width, height=new_height)
            sidebar.after(7, animate)
        else:
            populate_chapter_popup()
    animate()

def hide_section_popup():
    new_section_label.place_forget()
    new_section_name.place_forget()
    add_new_section.place_forget()
    new_section_name.delete(0, END)
    cancel_add_new_section.place_forget()
    new_section_error.place_forget()

    current_width = add_section_popup.winfo_width()
    current_height = add_section_popup.winfo_height()

    if current_width > 1 and current_height > 1:
        print(f"Current: {current_width}x{current_height}")
        new_width = max(current_width - 32/2, 1)
        new_height = max(current_height - 48/2, 1)
        add_section_popup.config(width=new_width, height=new_height)
        sidebar.after(7, hide_section_popup)
    else:
        in_menu = False
        add_section_popup.config(width=0, height=0)

def add_section_func():
    global active_chap

    for char in new_section_name.get():
        if char in unacceptable_file_chars:
            populate_section_popup(f"Invalid Char: {char}")
            return

    if not new_section_name.get().strip(): #If new_section_name is empty or whitespace
        populate_section_popup("Name cannot be empty!")
        return

    for section in sections:
        if new_section_name.get() == remove_extension(section.section):
            populate_section_popup("Section already exists!")
            return

    file_path = os.path.normpath(f"Projects/{current_project}/{active_chap}/{new_section_name.get()}.txt")

    with open(file_path, "w") as file:
        file.write("")

    refresh_project_view()
    treeview.selection_set(f"{current_project}/{active_chap}")
    treeview.focus(f"{current_project}/{active_chap}")
    hide_section_popup()

def populate_chapter_popup(message = ""):
    new_chapter_label.place_forget()
    new_chapter_name.place_forget()
    add_new_chapter.place_forget()
    new_chapter_name.delete(0, END)
    cancel_add_new_chapter.place_forget()
    
    new_chapter_label.place(relx=0.5, rely=0.1, anchor="center")
    new_chapter_name.place(relx=0.5, rely=0.18, anchor="center")
    add_new_chapter.place(relx=0.5, rely=0.36, anchor="center")
    cancel_add_new_chapter.place(relx=0.5, rely=0.45, anchor="center")
    new_chapter_error.place(relx=0.5, rely=0.26, anchor="center")
    new_chapter_name.focus_set()
    new_chapter_error.config(text=message)

def populate_section_popup(message = ""):
    new_section_label.place_forget()
    new_section_name.place_forget()
    add_new_section.place_forget()
    new_section_name.delete(0, END)
    cancel_add_new_section.place_forget()

    new_section_label.place(relx=0.5, rely=0.1, anchor="center")
    new_section_name.place(relx=0.5, rely=0.18, anchor="center")
    add_new_section.place(relx=0.5, rely=0.36, anchor="center")
    cancel_add_new_section.place(relx=0.5, rely=0.45, anchor="center")
    new_section_error.place(relx=0.5, rely=0.26, anchor="center")
    new_section_name.focus_set()
    new_section_error.config(text=message)

def ExpandSectionPopup():
    in_menu = True
    current_width = add_section_popup.winfo_width()
    current_height = add_section_popup.winfo_height()
    target_width = 320 - 32*2.5
    target_height = 480 - 48*2.5

    if current_width < target_width or current_height < target_height:
        new_width = min(target_width, current_width + 32/2)
        new_height = min(target_height, current_height + 48/2)
        add_section_popup.config(width=new_width, height=new_height)
        sidebar.after(7, ExpandSectionPopup)
    else:        
        populate_section_popup()

def ExpandSectionProperties():
    print("View Section Properties")

def SaveSection(event):
    global buffer, active_section
    with open(f"Projects/{os.path.normpath(active_section)}", "w", encoding="utf-8") as file:
        file.write(buffer)

def OpenSection():
    global buffer, active_section
    with open(f"Projects/{os.path.normpath(active_section)}", "r", encoding="utf-8") as file:
        buffer = file.read()
        set_screen_focus(False)
    update_display()

go_back = Button(project_view, text="< Projects", command=go_back_func, font=(default_font, 9, "bold"))
go_back.pack(fill=BOTH)

add_chap = Button(project_view, text="New Chapter", command=expand_chap_popup, font=(default_font, 9, "bold"))
add_chap.pack(fill=BOTH)

treeview = ttk.Treeview(project_view, selectmode="browse")
style = ttk.Style()
style.configure("Treeview", font=("Garamond", 12, "bold"))
style.configure("Treeview.Heading", font=("Garamond", 12, "bold"))
treeview.pack(expand=True, fill=BOTH)

add_chap_popup = Frame(project_view, bg="#FFFFFF", width=0, height=0, highlightthickness=2, highlightbackground="#000000")
add_chap_popup.place(relx=0.5, rely=0.5, anchor="center")

add_section_popup = Frame(project_view, bg="#FFFFFF", width=0, height=0, highlightthickness=2, highlightbackground="#000000")
add_section_popup.place(relx=0.5, rely=0.5, anchor="center")

section_properties_popup = Frame(project_view, bg="#FFFFFF", width=0, height=0)
section_properties_popup.place(relx=0.5, rely=0.5, anchor="center")

new_chapter_label = Label(add_chap_popup, text="Chapter Name", bg="#FFFFFF")
new_chapter_name = Entry(add_chap_popup)
add_new_chapter = Button(add_chap_popup, text="Add Chapter", command=add_chap_func)
cancel_add_new_chapter = Button(add_chap_popup, text="Cancel", command=hide_chap_popup)
new_chapter_error = Label(add_chap_popup, fg="#000000", font=(default_font, 9, "bold"), bg="#FFFFFF")

new_section_label = Label(add_section_popup, text="Section Name", bg="#FFFFFF")
new_section_name = Entry(add_section_popup)
add_new_section = Button(add_section_popup, text="Add Section", command=add_section_func)
cancel_add_new_section = Button(add_section_popup, text="Cancel", command=hide_section_popup)
new_section_error = Label(add_section_popup, fg="#000000", font=(default_font, 9, "bold"), bg="#FFFFFF")

can_go_up = False

active_section = None
last_sidebar_item = add_chap
last_treeview_item = None

def tree_selection_changed(event):
    global can_go_up
    items = treeview.get_children()
    if items:
        if treeview.focus() == items[0]:
            if not can_go_up:
                can_go_up = True
        else:
            can_go_up = False

treeview.bind("<<TreeviewSelect>>", tree_selection_changed)

def unselect_treeview():
    for item in treeview.selection():
        treeview.selection_remove(item)

def sidebar_focus(item):
    global last_sidebar_item
    item.focus_set()
    last_sidebar_item = item
    print(f"Sidebar Focus: {last_sidebar_item}")

def treeview_focus(item):
    global last_treeview_item
    last_treeview_item = item
    treeview.selection_set(last_treeview_item)
    treeview.focus(item)
    print(f"Treeview Focus: {last_treeview_item}")

def change_focus(event, forward = True):
    current_focus = sidebar.focus_get();
    if current_focus == go_back:
        if forward:
            sidebar_focus(add_chap)
        else:
            return
    elif current_focus == add_chap:
        if forward:
            items = treeview.get_children()
            if items:
                sidebar_focus(treeview)
                treeview_focus(items[0])
        if not forward:
            sidebar_focus(go_back)
    elif current_focus == treeview:
        if not forward:
            items = treeview.get_children()
            if treeview.focus() == items[0] and can_go_up:
                unselect_treeview()
                sidebar_focus(add_chap)
            elif treeview.focus() == items[0] and not can_go_up:
                treeview_focus(items[0])
        treeview_focus(treeview.selection()[0])
    elif current_focus == new_chapter_name:
        if forward:
            last_sidebar_item = add_new_chapter
            sidebar_focus(add_new_chapter)
    elif current_focus == add_new_chapter:
        if not forward:
            sidebar_focus(new_chapter_name)
        if forward:
            sidebar_focus(cancel_add_new_chapter)
    elif current_focus == cancel_add_new_chapter:
        if not forward:
            sidebar_focus(add_new_chapter)
    elif current_focus == new_section_name:
        if forward:
            sidebar_focus(add_new_section)
    elif current_focus == add_new_section:
        if not forward:
            sidebar_focus(new_section_name)
        if forward:
            sidebar_focus(cancel_add_new_section)
    elif current_focus == cancel_add_new_section:
        if not forward:
            sidebar_focus(add_new_section)
    else:
        print("No Current Focus or No Implementation for Current Focus")

go_back.focus_set()

sidebar.bind("<Down>", change_focus)
sidebar.bind("<Up>", lambda event: change_focus(event, False))

current_project = "Project 1"

treeview.heading("#0", text=current_project)

chapters = []
sections = []

active_chap = "Nothing"

def refresh_project_view():
    chapters.clear()
    sections.clear()
    treeview.delete(*treeview.get_children())

    for chapter in os.listdir(f"Projects/{current_project}"):
        chapter_obj = Chapter(current_project, chapter)
        chapters.append(chapter_obj)

    for chapter in chapters:
        for section in os.listdir(f"Projects/{current_project}/{chapter.chapter}"):
            section_obj = Section(chapter, section)
            sections.append(section_obj)

    for chapter in chapters:
        treeview.insert("", END, iid=f"{chapter.project}/{chapter.chapter}", text=chapter.chapter, open=True, tags=("chapter"))

    for section in sections:
        treeview.insert(f"{section.chapter.project}/{section.chapter.chapter}", END, iid=f"{section.chapter.project}/{section.chapter.chapter}/{section.section}", text=remove_extension(section.section), open=True, tags=("section"))

refresh_project_view()

def return_pressed(event):
    current_focus = sidebar.focus_get()
    if current_focus == go_back:
        go_back.config(relief=SUNKEN)
        go_back.invoke()
        sidebar.after(100, lambda: go_back.config(relief=RAISED))
    elif current_focus == add_chap:
        add_chap.config(relief=SUNKEN)
        add_chap.invoke()
        sidebar.after(100, lambda: add_chap.config(relief=RAISED))
    elif current_focus == treeview:
        selected_item = treeview.selection()[0]
        if selected_item:
            if "chapter" in treeview.item(selected_item, "tags"):
                global active_chap
                active_chap = treeview.item(selected_item, "text")
                print(active_chap)
                ExpandSectionPopup()
            elif "section" in treeview.item(selected_item, "tags"):
                global active_section
                active_section = f"{selected_item}"
                OpenSection()
    elif current_focus == add_new_chapter or current_focus == new_chapter_name:
        add_new_chapter.config(relief=SUNKEN)
        add_new_chapter.invoke()
        sidebar.after(100, lambda: add_new_chapter.config(relief=RAISED))
    elif current_focus == add_new_section or current_focus == new_section_name:
        add_new_section.config(relief=SUNKEN)
        add_new_section.invoke()
        sidebar.after(100, lambda: add_new_section.config(relief=RAISED))
    elif current_focus ==  cancel_add_new_chapter:
        hide_chap_popup()
    elif current_focus == cancel_add_new_section:
        hide_section_popup()
    else:
        print("No Current Focus Or No Implementation For Current Focus")

sidebar.bind("<Return>", return_pressed)

def expand_all_items(event):
    for item in treeview.get_children():
        treeview.item(item, open=True)
        
        expand_all_items_recursive(item)

def expand_all_items_recursive(parent_item):
    children = treeview.get_children(parent_item)

    for child in children:
        treeview.item(child, open=True)
        expand_all_items_recursive(child)

treeview.bind("<<TreeviewClose>>", expand_all_items)

"""Text Logic"""

text = Text(root, wrap="word", width=480, height=320, padx=10, pady=10)
text.pack(fill="both", expand=True)
text.focus_set()
text.configure(font=default_font)

buffer = ""
acceptable_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-=!@#$%^&*()_+[]{}\\|;:'\",.<>/?`~ "
unacceptable_file_chars = "<>:\"/\\|?*\0"
do_not_refresh_screen = {"Up", "Down", "Shift_L", "Shift_R"}

active_bold = False
active_italic = False

# Configure formatting tags
text.tag_configure("bold", font=(f"{current_font}", default_font_size, "bold"))
text.tag_configure("italic", font=(f"{current_font}", default_font_size, "italic"))

def apply_bold(event):
    global buffer, active_bold
    if active_bold:
    	if buffer.endswith("[b]"):
    		buffer = buffer[:-3]
    	elif buffer.endswith("[i]"):
    		buffer = buffer[:-3]
    	else:
    		buffer += "[/b]"
    else:
    	if active_italic:
    		return
    	buffer += "[b]"

    active_bold = not active_bold
    update_display()

def apply_italic(event):
    global buffer, active_italic
    if active_italic:
    	if buffer.endswith("[b]"):
            buffer = buffer[:-3]
    	elif buffer.endswith("[i]"):
        	buffer = buffer[:-3]
    	else:
       		buffer += "[/i]"
    else:
    	if active_bold:
    		return
    	buffer += "[i]"

    active_italic = not active_italic
    update_display()

def on_tab_press(event):
    key_press(event)
    return "break"

def key_press(event):
    global buffer
    if event.keysym == "BackSpace":
        if not buffer: #if buffer was empty
            return

        # Adjust cursor if deleting a formatting tag
        if buffer.endswith("[b]"):
            buffer = buffer[:-4]
        elif buffer.endswith("[/b]"):
            buffer = buffer[:-5]
        elif buffer.endswith("[i]"):
            buffer = buffer[:-4]
        elif buffer.endswith("[/i]"):
            buffer = buffer[:-5]
        else:
            buffer = buffer[:-1]

        update_display()
        return
    
    elif event.keysym == "Return":
        buffer += "\n"
    elif event.keysym in do_not_refresh_screen:
        return
    elif event.keysym == "Tab":
        buffer += " "*tabwidth
    else:
        if event.char in acceptable_chars:
            buffer += event.char
    
    update_display()

def parse_and_format_text():
    """
    Parses the buffer, removes formatting tags,
    and returns a tuple of:
      - clean_text (the text without tags)
      - tag_positions, a list of (start_offset, end_offset, tags)
        where start_offset and end_offset are integer positions in clean_text.
    """
    clean_text = ""
    bold = False
    italic = False
    tag_positions = []
    i = 0
    while i < len(buffer):
        if buffer[i:i+3] == "[b]":
            bold = True
            i += 3
        elif buffer[i:i+4] == "[/b]":
            bold = False
            i += 4
        elif buffer[i:i+3] == "[i]":
            italic = True
            i += 3
        elif buffer[i:i+4] == "[/i]":
            italic = False
            i += 4
        else:
            start = len(clean_text)
            clean_text += buffer[i]
            end = len(clean_text)
            tags = []
            if bold:
                tags.append("bold")
            if italic:
                tags.append("italic")
            if tags:
                tag_positions.append((start, end, tags))
            i += 1
    return clean_text, tag_positions

def update_display():
    """Updates the text widget with the formatted text based on buffer,
    preserving the cursor position even when text is deleted."""
    # Save the current cursor offset (i.e. number of characters from the start)
    old_offset = len(text.get("1.0", INSERT))
    
    # Clear and reinsert updated text
    text.delete("1.0", END)
    clean_text, tag_positions = parse_and_format_text()
    text.insert("1.0", clean_text)
    
    for start, end, tags in tag_positions:
        start_index = text.index("1.0+" + str(start) + "c")
        end_index = text.index("1.0+" + str(end) + "c")
        for tag in tags:
            text.tag_add(tag, start_index, end_index)

    text.see("end")

def disable_bind(event):
    return "break";

def scroll_up(event):
	text.yview_scroll(-1, "units")

def scroll_down(event):
	text.yview_scroll(1, "units")

text.bind("<Left>", disable_bind)
text.bind("<Right>", disable_bind)
text.bind("<Up>", scroll_up)
text.bind("<Down>", scroll_down)
sidebar.bind("<Tab>", disable_bind)

# Bind key events
text.bind("<Control-b>", apply_bold)
text.bind("<Control-i>", apply_italic)
root.bind("<KeyPress>", key_press)
text.bind("<Tab>", on_tab_press)
text.bind("<Control-s>", SaveSection)
sidebar.bind("<Control-s>", SaveSection)

def set_screen_focus(is_text):
    if(in_menu):
        return
    if not is_text:
        text.focus_set()
    if is_text:
        """if last_sidebar_item:
            last_sidebar_item.focus_set()
        else:
            add_chap.focus_set()
        print(f"Set Focus: {last_sidebar_item}")"""
        if not last_sidebar_item:
            print("No Last Sidebar Item!")
        if last_sidebar_item != treeview:
            last_sidebar_item.focus_set()
        elif last_sidebar_item == treeview:
            treeview.focus_set()
            treeview.selection_set(last_treeview_item)

sidebar.bind("<Alt_L>", lambda event: set_screen_focus(False))
text.bind("<Alt_L>", lambda event: set_screen_focus(True))

def Quit(event):
    exit(0)

root.bind("<Escape>", Quit)

root.mainloop()