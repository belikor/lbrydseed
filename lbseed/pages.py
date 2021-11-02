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
    class DownloadSinglePage:
        def setup_page_dch(self, parent):
            ...

    class Application(ttk.Frame, DownloadSinglePage):
        def __init__(self, root):
            page_dch = ttk.Frame(root)
            self.setup_page_dch(page_dch)
"""

import tkinter as tk

import lbseed.resolve as res
from .pages_base import (ConfigPage,
                         DownloadChPage, DownloadSinglePage,
                         ListPage,
                         DeleteSinglePage, DeleteChPage,
                         SupportListPage, SupportAddPage)
from .pages_adv import SeedPage, ControllingClaimsPage


class Variables:
    """Mixin class to provide variables to the application."""
    def setup_vars(self):
        self.e_font = tk.font.Font(family="monospace", size=10)
        self.b_width = 26
        self.txt_font = tk.font.Font(family="monospace")
        self.txt_lst_font = tk.font.Font(family="monospace", size=9)

        self.server_var = tk.StringVar()
        self.server_var.set("http://localhost:5279")
        self.down_dir_var = tk.StringVar()
        server = res.get_download_dir(server=self.server_var.get())
        self.down_dir_var.set(server)
        self.own_dir_var = tk.BooleanVar()
        self.own_dir_var.set(True)
        self.save_var = tk.BooleanVar()
        self.save_var.set(True)

        self.entry_chan = tk.StringVar()

        self.del_what_var = tk.StringVar()
        self.del_what_var.set("media")

        self.check_cid = tk.BooleanVar()
        self.check_cid.set(False)
        self.check_blobs = tk.BooleanVar()
        self.check_blobs.set(True)
        self.check_show_ch = tk.BooleanVar()
        self.check_show_ch.set(True)
        self.check_name = tk.BooleanVar()
        self.check_name.set(True)

        self.check_s_ch = tk.BooleanVar()
        self.check_s_ch.set(False)
        self.check_s_claims = tk.BooleanVar()
        self.check_s_claims.set(True)
        self.check_s_cid = tk.BooleanVar()
        self.check_s_cid.set(False)
        self.check_s_combine = tk.BooleanVar()
        self.check_s_combine.set(True)

        self.check_seed_plot = tk.BooleanVar()
        self.check_seed_plot.set(False)

        self.check_c_contr = tk.BooleanVar()
        self.check_c_contr.set(False)
        self.check_c_non_contr = tk.BooleanVar()
        self.check_c_non_contr.set(True)
        self.check_c_skip_repost = tk.BooleanVar()
        self.check_c_skip_repost.set(False)
        self.check_c_ch_only = tk.BooleanVar()
        self.check_c_ch_only.set(False)
        self.check_c_cid = tk.BooleanVar()
        self.check_c_cid.set(False)
        self.check_c_is_repost = tk.BooleanVar()
        self.check_c_is_repost.set(True)
        self.check_c_competing = tk.BooleanVar()
        self.check_c_competing.set(True)
        self.check_c_reposts = tk.BooleanVar()
        self.check_c_reposts.set(True)
        self.check_c_compact = tk.BooleanVar()
        self.check_c_compact.set(True)

        self.rad_s_support = tk.StringVar()
        self.rad_s_support.set("create")


# Use the classes to prevent warnings by code checkers (flake8)
True if ConfigPage else False
True if DownloadChPage else False
True if DownloadSinglePage else False
True if ListPage else False
True if DeleteSinglePage else False
True if DeleteChPage else False
True if SupportListPage else False
True if SupportAddPage else False

True if SeedPage else False
True if ControllingClaimsPage else False
