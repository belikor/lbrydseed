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
"""Mixin classes that add the download pages to the main graphical interface.

These classes should not be instantiatied directly. They are just used
in a multiple inheritance, or mixin pattern, to provide the necessary
building command to build the specific page in the main interface.

::
    class DownloadChsPage:
        def setup_page_dch(self, parent):
            ...

    class Application(ttk.Frame, DownloadChsPage):
        def __init__(self, root):
            page_dch = ttk.Frame(root)
            self.setup_page_dch(page_dch)
"""

import tkinter as tk
import tkinter.ttk as ttk

import lbseed.blocks as blocks


class DownloadChsPage:
    """Mixin class to provide the download channel page to the application."""
    def setup_page_dch(self, parent):
        self.setup_top_dch(parent)
        frame1 = ttk.Frame(parent)
        frame1.pack(padx=4, pady=4, fill="both", expand=False)
        frame2 = ttk.Frame(parent)
        frame2.pack(padx=4, pady=4, fill="both", expand=True)
        self.setup_textbox_dch(frame1)
        self.setup_textbox_dch_summ(frame2)

    def setup_top_dch(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_dch(frame, start=0)
        self.setup_grid_button_dch(frame, start=1)
        self.setup_grid_check_dch(frame, start=4)
        self.setup_info_dch(frame, start=7)

    def setup_grid_top_dch(self, parent, start=0):
        blocks.setup_entry_gen(parent,
                               font=self.e_font,
                               text_var=self.entry_d_dir,
                               l_text=("Download directory. "
                                       "It defaults to your home directory."),
                               start=start)

    def setup_grid_button_dch(self, parent, start=0):
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
                                b_text="Download claims from channels",
                                b_command=self.download_chs,
                                l_text=("Start downloading the newest claims "
                                        "from the channels"),
                                start=start+2)

    def setup_grid_check_dch(self, parent, start=0):
        (self.chck_save_dch,
         self.chck_owndir_dch) = \
            blocks.setup_check_download(parent,
                                        repost_var=self.check_d_repost,
                                        own_dir_var=self.check_d_own_dir,
                                        save_var=self.check_d_save,
                                        enable_command=self.chck_enable_dch,
                                        start=start)

    def chck_enable_dch(self, force_second_var=True):
        if self.check_d_save.get():
            if force_second_var:
                self.check_d_own_dir.set(True)
            self.chck_owndir_dch["state"] = "normal"
        else:
            self.check_d_own_dir.set(False)
            self.chck_owndir_dch["state"] = "disabled"

    def setup_info_dch(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Add a channel name or the claim ID "
                               "of the channel (40-character string), "
                               "a semicolon,\n"
                               "and the number of items to download "
                               "from this channel."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_dch(self, parent):
        channels = blocks.set_up_default_channels()
        self.textbox_dch = blocks.setup_textbox(parent, font=self.txt_font)
        self.textbox_dch.insert("1.0", channels)

    def setup_textbox_dch_summ(self, parent):
        self.textbox_dch_summ = \
            blocks.setup_textbox(parent, font=self.txt_lst_font)
        self.textbox_dch_summ.insert("1.0", "(information about the claims)")
        self.textbox_dch_summ["state"] = "disabled"


class DownloadClaimsPage:
    """Mixin class to provide the download single page to the application."""
    def setup_page_d(self, parent):
        self.setup_top_d(parent)
        frame1 = ttk.Frame(parent)
        frame1.pack(padx=4, pady=4, fill="both", expand=False)
        frame2 = ttk.Frame(parent)
        frame2.pack(padx=4, pady=4, fill="both", expand=True)
        self.setup_textbox_d(frame1)
        self.setup_textbox_d_summ(frame2)

    def setup_top_d(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_d(frame, start=0)
        self.setup_grid_button_d(frame, start=1)
        self.setup_grid_check_d(frame, start=3)
        self.setup_info_d(frame, start=6)

    def setup_grid_top_d(self, parent, start=0):
        blocks.setup_entry_gen(parent,
                               font=self.e_font,
                               text_var=self.entry_d_dir,
                               l_text=("Download directory. "
                                       "It defaults to your home directory."),
                               start=start)

    def setup_grid_button_d(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Resolve online",
                                b_command=self.resolve_claims_d,
                                l_text="Confirm that the claims exist",
                                start=start)

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Download claims",
                                b_command=self.download_claims,
                                l_text="Start downloading claims",
                                start=start+1)

    def setup_grid_check_d(self, parent, start=0):
        (self.chck_save_d,
         self.chck_owndir_d) = \
            blocks.setup_check_download(parent,
                                        repost_var=self.check_d_repost,
                                        own_dir_var=self.check_d_own_dir,
                                        save_var=self.check_d_save,
                                        enable_command=self.chck_enable_d,
                                        start=start)

    def chck_enable_d(self, force_second_var=True):
        if self.check_d_save.get():
            if force_second_var:
                self.check_d_own_dir.set(True)
            self.chck_owndir_d["state"] = "normal"
        else:
            self.check_d_own_dir.set(False)
            self.chck_owndir_d["state"] = "disabled"

    def setup_info_d(self, parent, start=0):
        blocks.info_claims(parent, start=start)

    def setup_textbox_d(self, parent):
        claims = blocks.set_up_default_claims()
        self.textbox_d = blocks.setup_textbox(parent, font=self.txt_font)
        self.textbox_d.insert("1.0", claims)

    def setup_textbox_d_summ(self, parent):
        self.textbox_d_summ = \
            blocks.setup_textbox(parent, font=self.txt_lst_font)
        self.textbox_d_summ.insert("1.0", "(information about the claims)")
        self.textbox_d_summ["state"] = "disabled"
