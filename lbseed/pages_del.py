#!/usr/bin/env python3
# --------------------------------------------------------------------------- #
# The MIT License (MIT)                                                       #
#                                                                             #
# Copyright (c) 2021 Eliud Cabrera Castillo <e.cabrera-castillo@tum.de>       #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining       #
# a copy of this software and associated documentation files                  #
# (the "Software"), to deal in the Software without restriction, including    #
# without limitation the rights to use, copy, modify, merge, publish,         #
# distribute, sublicense, and/or sell copies of the Software, and to permit   #
# persons to whom the Software is furnished to do so, subject to the          #
# following conditions:                                                       #
#                                                                             #
# The above copyright notice and this permission notice shall be included     #
# in all copies or substantial portions of the Software.                      #
#                                                                             #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     #
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
# DEALINGS IN THE SOFTWARE.                                                   #
# --------------------------------------------------------------------------- #
"""Mixin classes that add the deleting pages to the main graphical interface.

These classes should not be instantiatied directly. They are just used
in a multiple inheritance, or mixin pattern, to provide the necessary
building command to build the specific page in the main interface.

::
    class DeleteClaimsPage:
        def setup_page_del(self, parent):
            ...

    class Application(ttk.Frame, DeleteClaimsPage):
        def __init__(self, root):
            page_del = ttk.Frame(root)
            self.setup_page_del(page_del)
"""

import tkinter as tk
import tkinter.ttk as ttk

import lbseed.blocks as blocks


class DeleteClaimsPage:
    """Mixin class to provide the delete page to the application."""
    def setup_page_del(self, parent):
        self.setup_top_del(parent)
        self.setup_textbox_del(parent)

    def setup_top_del(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_del(frame, start=0)
        self.setup_grid_radio_del(frame, start=2)
        self.setup_info_del(frame, start=5)

    def setup_grid_top_del(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Resolve online",
                                b_command=self.resolve_claims,
                                l_text="Confirm that the claims exist",
                                start=start)

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Delete claims",
                                b_command=self.delete_claims,
                                l_text="Delete locally downloaded claims",
                                start=start+1)

    def setup_grid_radio_del(self, parent, start=0):
        blocks.setup_radio_delete(parent,
                                  del_what_var=self.rad_delete_what,
                                  start=start)

    def setup_info_del(self, parent, start=0):
        blocks.info_claims(parent, start=start)

    def setup_textbox_del(self, parent):
        claims = blocks.set_up_default_claims(clean_up=True)
        self.textbox_del = blocks.setup_textbox(parent, font=self.txt_font)
        self.textbox_del.insert("1.0", claims)


class DeleteChsPage:
    """Mixin class to provide the list page to the application."""
    def setup_page_delch(self, parent):
        self.setup_top_delch(parent)
        self.setup_textbox_delch(parent)

    def setup_top_delch(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_button_delch(frame, start=0)
        self.setup_grid_radio_delch(frame, start=3)
        self.setup_info_delch(frame, start=6)

    def setup_grid_button_delch(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Validate input",
                                b_command=self.validate_chs,
                                l_text=("Verify that the input "
                                        "can be read correctly"),
                                start=start)

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Resolve online",
                                b_command=self.resolve_chs,
                                l_text="Confirm that the channels exist",
                                start=start+1)

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Clean up claims",
                                b_command=self.delete_chs,
                                l_text=("Start deleting claims "
                                        "from the oldest to the newest"),
                                start=start+2)

    def setup_grid_radio_delch(self, parent, start=0):
        blocks.setup_radio_delete(parent,
                                  del_what_var=self.rad_delete_what,
                                  start=start)

    def setup_info_delch(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Add a channel, a semicolon, "
                               "and the number of items to keep "
                               "from this channel.\n"
                               "The N newest claims (by publication date) "
                               "will remain while older items "
                               "will be removed.\n"
                               "If the number is 0, it will remove "
                               "all downloaded items from the channel."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_delch(self, parent):
        channels = blocks.set_up_default_channels(clean_up=True)
        self.textbox_delch = blocks.setup_textbox(parent, font=self.txt_font)
        self.textbox_delch.insert("1.0", channels)
