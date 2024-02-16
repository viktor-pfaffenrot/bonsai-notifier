#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 01:38:01 2022

Author: Viktor Pfaffenrot

This small GUI manages the dates of typical bonsai maintenance actions and
displays some basic infos.


All but fertilizing can be set to today's date by clicking on the left plus
button. In case of fertilization, the next fertilization date will be set when
clicking the plus button. The date is determined according to the tree's
fertilization schedule (typically every two months in the growing season).
All dates can be manually set by entering the corresponding fields.

New bonsai can be added by clicking on 'Add Bonsai'. This prompts to another
field asking for the name and the purchase date of the new tree. Specific infos
can be parsed by clicking on 'Fill Info'. When saving, a json file is created
for the specific tree. Before filling, submit the tree to the database.

Deleting the currently shown bonsai is achieved by clicking on 'Del. Bonsai'.
"""

from bonsai_class import bonsai
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import tkinter as tk
import textwrap
import customtkinter as ctk
from PIL import Image, ImageTk
import numpy as np
import json
import re
import os


class bonsai_notifier:
    r"""
    update buttons:

    .. automethod:: update_next_fertilize
    .. automethod:: update_last_pruning
    .. automethod:: update_last_repot
    .. automethod:: update_last_wiring

    remaining buttons:

    .. automethod:: next_bonsai
    .. automethod:: prev_bonsai
    .. automethod:: update_bonsai_database
    .. automethod:: show_info
    .. automethod:: add_bonsai



    remaining:
    """

    def __init__(self, master: object, db_file: str, dims: tuple):
        # ----------------------------LOAD BONSAI CLASS------------------------
        bonsai.initiate_database(db_file)
        self.trees_at_start = bonsai.load_database(db_file)
        self.trees = bonsai.load_database(db_file)

        self.treeidx = np.random.randint(np.size(self.trees))

        for tree in self.trees:
            tree.set_info(db_file)

        self.actions = (
            "next_fertilize",
            "last_pruning",
            "last_repot",
            "last_wiring",
        )
        self.fg_color = ("#4F101A", "#4F101A")

        self.create_labels(master)
        self.create_buttons(master, dims)
        self.create_entries(master)

        self.Name_upon_creation = []

    def create_labels(self, master: object):
        text = textwrap.fill(self.trees[self.treeidx].name, width=20)
        self.NameLabel = canvas.create_text(
            170, 25, text=text, font=("Times", 20, "bold"), fill="white"
        )
        text = (
            textwrap.fill("next fertilize", width=10),
            textwrap.fill("last pruning", width=8),
            textwrap.fill("last repot", width=8),
            textwrap.fill("last wiring", width=8),
        )

        self.ActionLabel = []
        for ii in range(4):
            self.ActionLabel.append(
                canvas.create_text(
                    35,
                    75 + ii * 75,
                    text=text[ii],
                    font=("Times", 16),
                    fill="white",
                    justify="center",
                )
            )

    def create_buttons(self, master: object, dims: tuple):
        imagepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "images"
        )

        # Next button
        ButtonNextImage = ctk.CTkImage(
            Image.open(f"{imagepath}/arrow_right.png")
        )
        ButtonNext = ctk.CTkButton(
            canvas,
            image=ButtonNextImage,
            border_width=0,
            text="",
            width=40,
            height=40,
            fg_color="transparent",
            command=self.next_bonsai,
        )
        ButtonNext.image = ButtonNextImage
        ButtonNext.place(x=dims[0] - 40, y=2)
        # previous button
        ButtonPrevImage = ctk.CTkImage(
            Image.open(f"{imagepath}/arrow_left.png")
        )
        ButtonPrev = ctk.CTkButton(
            canvas,
            image=ButtonPrevImage,
            border_width=0,
            text="",
            width=40,
            height=40,
            fg_color="transparent",
            command=self.prev_bonsai,
        )
        ButtonPrev.place(x=0, y=2)
        # change button
        master.update()
        ButtonChangeImage = ctk.CTkImage(Image.open(f"{imagepath}/plus.png"))
        ButtonChange = []
        cmd = (
            "self.update_next_fertilize",
            "self.update_last_pruning",
            "self.update_last_repot",
            "self.update_last_wiring",
        )
        for ii in range(4):
            ButtonChange.append(
                ctk.CTkButton(
                    canvas,
                    image=ButtonChangeImage,
                    border_width=0,
                    text="",
                    width=40,
                    height=40,
                    fg_color="transparent",
                    command=eval(cmd[ii]),
                )
            )
            ButtonChange[ii].place(y=60 + ii * 75, x=dims[0] - 40)
        # add bonsai
        ButtonAddBonsai = ctk.CTkButton(
            canvas,
            text="Add Bonsai",
            font=("Times", 16),
            fg_color=self.fg_color,
            width=40,
            height=20,
            command=lambda: self.add_bonsai(master, dims),
        )
        ButtonAddBonsai.place(y=dims[1] - 60, x=dims[0] // 5)
        # remove bonsai
        ButtonRemBonsai = ctk.CTkButton(
            canvas,
            text="Del. Bonsai",
            font=("Times", 16),
            fg_color=self.fg_color,
            width=40,
            height=20,
            command=self.remove_bonsai,
        )
        ButtonRemBonsai.place(y=dims[1] - 60, x=dims[0] // 1.75)
        # save changes
        ButtonSave = ctk.CTkButton(
            canvas,
            text="Save Changes",
            font=("Times", 16),
            fg_color=self.fg_color,
            width=40,
            height=20,
            command=lambda: self.update_bonsai_database(master, db_file),
        )
        ButtonSave.place(y=dims[1] - 30, x=dims[0] // 1.8)
        # show infos
        ButtonInfo = ctk.CTkButton(
            canvas,
            text="Show Info",
            font=("Times", 16),
            fg_color=self.fg_color,
            width=40,
            height=20,
            command=lambda: self.show_info(master),
        )
        ButtonInfo.place(y=dims[1] - 30, x=dims[0] // 4.7)

    def create_entries(self, master: object):
        self.DateInput = []
        for ii in range(4):
            self.DateInput.append(
                ctk.CTkEntry(
                    canvas,
                    width=107,
                    border_width=0,
                    font=("Times", 20),
                    fg_color="transparent",
                )
            )
            self.DateInput[ii].place(x=130, y=65 + ii * 75)
            self.DateInput[ii].insert(
                0, getattr(self.trees[self.treeidx], self.actions[ii])
            )

    # -----------------------------------METHODS--------------------------------
    def next_bonsai(self, DO_DELETE=False):
        self.update_inputfield(DO_DELETE)
        trees = np.array(range(0, len(self.trees)))
        self.treeidx = (self.treeidx + 1) % len(trees)

        canvas.delete(self.NameLabel)
        text = textwrap.fill(self.trees[self.treeidx].name, width=20)
        self.NameLabel = canvas.create_text(
            170, 25, text=text, font=("Times", 20, "bold"), fill="white"
        )
        self.change_inputfield()

    def prev_bonsai(self):
        self.update_inputfield()
        trees = np.array(range(0, len(self.trees)))
        self.treeidx = (self.treeidx - 1) % len(trees)

        canvas.delete(self.NameLabel)
        text = textwrap.fill(self.trees[self.treeidx].name, width=20)
        self.NameLabel = canvas.create_text(
            170, 25, text=text, font=("Times", 20, "bold"), fill="white"
        )
        self.change_inputfield()

    def update_next_fertilize(self):
        next_fertilize = date.today() + relativedelta(months=2)

        # if fertilizing happens to land in off-season, increase till growing
        # season
        if next_fertilize.month > 9:
            next_fertilize = next_fertilize + relativedelta(
                months=(3 - next_fertilize.month) % 12
            )

        # do not fertilizes for one month after repot
        if self.DateInput[2].get() != "Not Yet":
            last_repot = datetime.strptime(self.DateInput[2].get(), "%d.%m.%Y")
            if next_fertilize < last_repot.date() + relativedelta(months=1):
                next_fertilize = last_repot + relativedelta(months=1)

        self.trees[self.treeidx].set_next_fertilize(
            next_fertilize.strftime("%d.%m.%Y")
        )
        self.DateInput[0].delete(0, "end")
        self.DateInput[0].insert(0, self.trees[self.treeidx].next_fertilize)

    def update_last_pruning(self):
        self.trees[self.treeidx].set_last_pruning(
            date.today().strftime("%d.%m.%Y")
        )
        self.DateInput[1].delete(0, "end")
        self.DateInput[1].insert(0, self.trees[self.treeidx].last_pruning)

    def update_last_repot(self):
        self.trees[self.treeidx].set_last_repot(
            date.today().strftime("%d.%m.%Y")
        )
        self.DateInput[2].delete(0, "end")
        self.DateInput[2].insert(0, self.trees[self.treeidx].last_repot)

    def update_last_wiring(self):
        self.trees[self.treeidx].set_last_wiring(
            date.today().strftime("%d.%m.%Y")
        )
        self.DateInput[3].delete(0, "end")
        self.DateInput[3].insert(0, self.trees[self.treeidx].last_wiring)

    def update_inputfield(self, DO_DELETE=False):
        r"""
        Here, the current entries are updated.
        """

        if not DO_DELETE:
            DateInput_new = [self.DateInput[ii].get() for ii in range(0, 4)]

            # DateInput_old = [getattr(self.trees[self.treeidx], self.actions[ii]) for ii in range(0,4)]
            [
                setattr(
                    self.trees[self.treeidx],
                    self.actions[ii],
                    DateInput_new[ii],
                )
                for ii in range(0, 4)
            ]  # if DateInput_new != DateInput_old

    def change_inputfield(self):
        r"""
        Changes the entry fields upon button press
        """
        [self.DateInput[ii - 1].delete(0, "end") for ii in range(1, 5)]
        [
            self.DateInput[ii].insert(
                0, getattr(self.trees[self.treeidx], self.actions[ii])
            )
            for ii in range(0, 4)
        ]

    def update_bonsai_database(self, master: object, db_file: str):
        r"""
        When Save Change is pressed, the entire list of bonsai classes is
        compared with that at the start of the app.
        If they differ, the bonsai database is updated.
        """

        self.update_inputfield()
        if self.trees_at_start != self.trees:
            for idx, tree in enumerate(self.trees):
                if tree != self.trees_at_start[idx]:
                    bonsai.update_database(tree, db_file, True)
            self.trees_at_start = self.trees

    # -----------------------------Create new window---------------------------
    def create_new_window(self, master: object):
        window = ctk.CTkToplevel(master)
        window.configure(fg_color="#25212F")
        window.wm_attributes("-type", "splash")
        return window

    # --------------------------show and save info window----------------------
    def show_info(self, master: object, init=False):
        """
        Raises another toplevel window showing some additional infos in a list
        of bullet points. If the tree is initialized, some placeholding points
        are shown.
        The structure is: \n
        Method: \n
        \*points. \n
        The bullet points can be filled using ``*``.
        """

        window = self.create_new_window(master)
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()

        dims = [700, 500]
        x = ws - 2 * dims[0]
        y = hs - dims[1] - 400

        window.geometry("%dx%d+%d+%d" % (dims[0], dims[1], x, y))

        if init:
            text = self.Name_upon_creation[0]
        else:
            text = self.trees[self.treeidx].name

        BonsaiLabel = ctk.CTkLabel(
            window,
            text=text,
            font=ctk.CTkFont(family="Times", size=25, weight="bold"),
        )
        BonsaiLabel.grid(row=0, column=1, pady=(10, 0), padx=0)

        # get size of the label widget and place it in the horiontal center of
        # the window
        master.update()
        w = BonsaiLabel.winfo_width()
        BonsaiLabel.grid(
            row=0, column=1, pady=(10, 0), padx=dims[0] // 2 - w // 2
        )

        index = next(
            (
                ii
                for ii, obj in enumerate(self.trees)
                if obj.name == BonsaiLabel.cget("text")
            ),
            None,
        )

        if os.path.exists(self.trees[index].info):
            with open(self.trees[index].info, "r") as json_file:
                info = json.load(json_file)

        text_widget = ctk.CTkTextbox(
            window,
            activate_scrollbars=True,
            font=("Times", 20),
            width=dims[0],
            height=dims[1],
            fg_color="#25212F",
        )
        text_widget.grid(row=2, column=1)

        if os.path.exists(self.trees[index].info):
            # Insert JSON data into the text widget
            for action, points in info.items():
                text_widget.insert(tk.END, f"{action}:\n")
                for point in points:
                    text_widget.insert(tk.END, f"    • {point}\n")
                    text_widget.insert(tk.END, "\n")

        else:
            actions = ["Repot", "Pruning", "Wiring"]
            for action in actions:
                text_widget.insert(tk.END, f"{action}:\n")
                for point in range(3):
                    text_widget.insert(tk.END, "    • \n")
                    text_widget.insert(tk.END, "\n")

        # close window
        ButtonClose = ctk.CTkButton(
            window,
            text="Close",
            font=("Times", 20),
            fg_color=self.fg_color,
            width=40,
            height=20,
            command=window.destroy,
        )
        ButtonClose.place(y=11, x=dims[0] // 2 + w // 2 + 20)

        # save changes
        ButtonSave = ctk.CTkButton(
            window,
            text="Save",
            font=("Times", 20),
            fg_color=self.fg_color,
            width=40,
            height=20,
            command=lambda: self.save_info(master, text_widget, BonsaiLabel),
        )
        ButtonSave.place(y=11, x=dims[0] // 2 - w // 2 - 70)

    def save_info(
        self, master: object, text_widget: object, BonsaiLabel: object
    ):
        """
        Converts the info text string into a dictionary of the same shape as the input
        and saves it to a json file with the same name as the bonsai name
        """
        info = text_widget.get("1.0", "end-1c")
        sections = re.split(r"\n+", info.strip())
        info_out = {}
        action = ""
        content = []

        for section in sections:
            if action != "" and action != section.strip(":"):
                info_out[action] = content

            if ":" in section:
                action = section.strip(":")
                content = []
            else:
                content.append(section.strip().strip("• "))

        index = next(
            (
                ii
                for ii, obj in enumerate(self.trees)
                if obj.name == BonsaiLabel.cget("text")
            ),
            None,
        )

        info_out = {
            key: [s.replace("*", "") for s in value]
            for key, value in info_out.items()
        }

        with open(self.trees[index].info, "w") as json_file:
            json.dump(info_out, json_file, indent=4)

    # --------------------------Add new and remove old bonsai methods---------------
    def add_bonsai(self, master: object, dims: tuple):
        """
        Creates a new toplevel window asking for the name and the purchase date
        of the new tree and adds the tree to the database. Filling additional
        infos is possible after submitting to the database.
        """

        window = self.create_new_window(master)

        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()

        dims = list(dims)
        dims[1] = 200
        x = ws - 3.5 * dims[0]
        y = hs - dims[1] - 400

        window.geometry("%dx%d+%d+%d" % (dims[0], dims[1], x, y))

        # create the label at the top of the window
        AddBonsaiLabel = ctk.CTkLabel(
            window,
            text="Specify bonsai:",
            font=ctk.CTkFont(family="Times", size=25, weight="bold"),
        )
        AddBonsaiLabel.grid(row=0, column=1, pady=(10, 0), padx=90)

        # create the entry field for the name and the purchase date
        text = ("Name", "purchase date")
        Queries = []
        for ii in range(2):
            Queries.append(
                ctk.CTkEntry(
                    window,
                    width=200,
                    border_width=0,
                    font=("Times", 20),
                    justify="center",
                )
            )
            Queries[ii].place(y=55 + ii * 60, x=dims[0] // 2 - 100)
            Queries[ii].insert(0, text[ii])

        # create buttons to submit the tree to the database and to close the window
        ButtonInitInfo = ctk.CTkButton(
            window,
            text="Fill Info",
            font=("Times", 16),
            fg_color=self.fg_color,
            width=40,
            height=20,
            command=lambda: self.show_info(master, init=True),
            state=tk.DISABLED,
        )
        ButtonInitInfo.place(y=dims[1] - 30, x=dims[0] // 2.5)

        ButtonSubmit = ctk.CTkButton(
            window,
            text="Submit",
            font=("Times", 16),
            fg_color=self.fg_color,
            width=40,
            height=20,
            command=lambda: add_new_bonsai(
                self, master, db_file, text, ButtonInitInfo
            ),
        )
        ButtonSubmit.place(y=dims[1] - 30, x=dims[0] // 5)

        ButtonClose = ctk.CTkButton(
            window,
            text="Close",
            font=("Times", 16),
            fg_color=self.fg_color,
            width=40,
            height=20,
            command=window.destroy,
        )
        ButtonClose.place(y=dims[1] - 30, x=dims[0] // 1.55)

        def add_new_bonsai(
            self,
            master: object,
            db_file: str,
            text: tuple,
            ButtonInitInfo: object = None,
        ):
            # calculate the need fertilizing date
            Input = [Queries[ii].get() for ii in range(2)]
            if 3 <= datetime.now().month <= 9:
                Input[1] = datetime.strptime(Input[1], "%d.%m.%Y") + timedelta(
                    days=7
                )
            else:
                Input[1] = datetime.strptime(
                    Input[1], "%d.%m.%Y"
                ) + relativedelta(months=1)
            Input[1] = Input[1].strftime("%d.%m.%Y")

            # create a new tree id
            newid = int(
                1
                + np.max(
                    [
                        self.trees[ii].treeid
                        for ii in range(0, np.size(self.trees))
                    ]
                )
            )

            # create known attributes for the new tree
            Input.insert(0, newid)
            bonsai_attributes = ["treeid", "name", self.actions[0]]

            # append the list of bonsai classes by one and set the new attributes
            self.trees.append(bonsai())
            [
                setattr(self.trees[-1], bonsai_attributes[ii], Input[ii])
                for ii in range(3)
            ]

            directory, filename = os.path.split(db_file)

            setattr(
                self.trees[-1],
                "info",
                f"{directory}/{self.trees[-1].name}.json",
            )
            bonsai.update_database(self.trees[-1], db_file, True)

            self.Name_upon_creation.append(Queries[0].get())

            # if bonsai was submitted to the database, enable filling infos
            if ButtonInitInfo != None:
                ButtonInitInfo.configure(state="normal")
            # cleaning up
            # [Queries[ii].delete(0,'end') for ii in range(0,2)]
            # [Queries[ii].insert(0,text[ii]) for ii in range(0,2)]

    def remove_bonsai(self):
        # here are 2 bugs:
        # 2. if a bonsai is deleted, the previous one has its entries
        bonsai.update_database(self.trees[self.treeidx], db_file, False)
        if os.path.isfile(self.trees[self.treeidx].info):
            os.remove(self.trees[self.treeidx].info)
        self.trees.remove(self.trees[self.treeidx])
        self.treeidx = self.treeidx - 1
        if self.treeidx < 0:
            self.treeidx = 0
        self.next_bonsai(DO_DELETE=True)


# ------------------------------------------------------------------------------


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(base_dir, "db/bonsai_database.db")
    root = tk.Tk()

    root.title("")
    root.wm_attributes("-type", "splash")
    ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
    ctk.set_default_color_theme(
        "dark-blue"
    )  # Themes: blue (default), dark-blue, green

    w = 340
    h = 390
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    # calculate x and y coordinates for the Tk root window
    x = ws - 2 * w
    y = hs - h - 35

    # set the dimensions of the screen
    # and where it is placed
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))

    canvas = tk.Canvas(
        root, width=w, height=h, highlightthickness=0, bd=0, bg="#25212F"
    )
    canvas.pack(fill="both", expand=True)

    img_file = os.path.join(base_dir, "images/bg_drawing.png")
    background_img = ImageTk.PhotoImage(
        Image.open(img_file).resize((w, h))
    )  # Image.ANTIALIAS
    canvas.create_image(-20, 0, image=background_img, anchor="nw")

    b = bonsai_notifier(root, db_file, (w, h))

    root.mainloop()
