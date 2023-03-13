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
"""Mixin classes that add the different pages to the main graphical interface.

These classes should not be instantiatied directly. They are just used
in a multiple inheritance, or mixin pattern, to provide the necessary
building command to build the specific page in the main interface.

::
    class DownloadClaimsPage:
        def setup_page_dch(self, parent):
            ...

    class Application(ttk.Frame, DownloadClaimsPage):
        def __init__(self, root):
            page_dch = ttk.Frame(root)
            self.setup_page_dch(page_dch)
"""
import tkinter as tk
import tkinter.ttk as ttk

import lbseed.blocks as blocks


class SettingsPage:
    """Mixin class to provide the configuration page to the application."""
    def setup_page_settings(self, parent):
        self.setup_top_settings(parent)
        self.setup_textbox_settings(parent)

    def setup_top_settings(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_settings(frame, start=0)
        self.setup_info_settings(frame, start=2)

    def setup_grid_top_settings(self, parent, start=0):
        entry, label = \
            blocks.setup_entry_gen(parent,
                                   font=self.e_font,
                                   text_var=self.server_var,
                                   l_text=("Address of the 'lbrynet' daemon. "
                                           "It defaults to localhost:5279"),
                                   start=start)
        entry["width"] = self.b_width

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Display LBRY settings",
                                b_command=self.list_lbrynet_settings,
                                l_text=("Display the settings "
                                        "for the running 'lbrynet' daemon"),
                                start=start+1)

    def setup_info_settings(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("The settings that aren't specified "
                               "in the 'config' file "
                               "will use their default values."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_settings(self, parent, start=0):
        self.textbox_settings = blocks.setup_textbox(parent,
                                                     font=self.txt_font)
        self.textbox_settings.insert("1.0", "(settings)")
        self.textbox_settings["state"] = "disabled"


class StatusPage:
    """Mixin class to provide the status page to the application."""
    def setup_page_status(self, parent):
        self.setup_top_status(parent)
        self.setup_info_status(parent)

    def setup_top_status(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_st(frame, start=0)

    def setup_grid_top_st(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Display LBRY status",
                                b_command=self.list_lbrynet_status,
                                l_text=("Display status information "
                                        "for the running 'lbrynet' daemon"),
                                start=start)

    def setup_info_status(self, parent, start=0):
        self.textbox_status = blocks.setup_textbox(parent, font=self.txt_font)
        self.textbox_status.insert("1.0", "(status)")
        self.textbox_status["state"] = "disabled"
