from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Andrew's L2 Assessment Program")

opening_frame = ttk.LabelFrame(root, text="Title Screen")
opening_frame.grid(row=0, column=0, columnspan=10, padx=10, pady=10, sticky="NSEW")


def screen_1():
    clear_frame()
    title1_text = StringVar()
    title1_text.set("Video Game")
    title1_label = ttk.Label(opening_frame, textvariable=title1_text)
    title1_label.grid(row=0, column=0, columnspan=10, padx=10, pady=10)
    change_button = ttk.Button(opening_frame, text="Change", command=screen_2())
    change_button.grid(row=0, column=1)


def screen_2():
    clear_frame()
    title2_text = StringVar()
    title2_text.set("Video Game2")
    title2_label = ttk.Label(opening_frame, textvariable=title2_text)
    title2_label.grid(row=0, column=0, columnspan=10, padx=10, pady=10)
    change1_button = ttk.Button(opening_frame, text="Change", command=screen_1())
    change1_button.grid(row=0, column=1)


def clear_frame():
    for widgets in opening_frame.winfo_children():
        widgets.destroy()


opening_button = ttk.Button(opening_frame, text="Open", command=screen_1())
opening_button.grid(row=0, column=1, columnspan=10, padx=10, pady=10)
root.mainloop()
