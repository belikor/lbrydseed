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
import tkinter.ttk as ttk

import lbseed.blocks as blocks
import lbseed.resolve as res


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


class ConfigPage:
    """Mixin class to provide the configuration page to the application."""
    def setup_page_cfg(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_top_config(frame, start=0)

    def setup_top_config(self, parent, start=0):
        entry = ttk.Entry(parent,
                          textvariable=self.server_var,
                          font=self.e_font,
                          width=self.b_width)
        entry.grid(row=start, column=0, sticky=tk.W + tk.E)
        le = ttk.Label(parent,
                       text=("Address of the 'lbrynet' daemon. "
                             "It defaults to localhost:5279"))
        le.grid(row=start, column=1, sticky=tk.W, padx=2)


class DownloadChPage:
    """Mixin class to provide the download channel page to the application."""
    def setup_page_dch(self, parent):
        self.setup_top_dch(parent)
        self.setup_textbox_dch(parent)

    def setup_top_dch(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_dch(frame, start=0)
        self.setup_grid_button_dch(frame, start=1)
        self.setup_grid_check_dch(frame, start=4)
        self.setup_info_dch(frame, start=6)

    def setup_grid_top_dch(self, parent, start=0):
        blocks.setup_download_entry(parent,
                                    dir_var=self.down_dir_var,
                                    font=self.e_font,
                                    start=start)

    def setup_grid_button_dch(self, parent, start=0):
        blocks.setup_buttons_val_res(parent,
                                     width=self.b_width,
                                     validate_func=self.validate_ch,
                                     resolve_func=self.resolve_ch,
                                     start=start)

        b_download = ttk.Button(parent, text="Download claims",
                                width=self.b_width,
                                command=self.download_ch)
        b_download.grid(row=start+2, column=0)
        b_download.bind("<<Activate>>",
                        blocks.f_with_event(self.download_ch))

        lr = ttk.Label(parent,
                       text=("Start downloading the newest claims "
                             "from the channels"))
        lr.grid(row=start+2, column=1, sticky=tk.W, padx=2)

    def setup_grid_check_dch(self, parent, start=0):
        blocks.setup_download_check(parent,
                                    own_dir_var=self.own_dir_var,
                                    save_var=self.save_var,
                                    start=start)

    def setup_info_dch(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Add a channel, a comma, "
                               "and the number of items to download "
                               "from this channel"))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_dch(self, parent):
        channels = blocks.set_up_default_channels()
        self.textbox_dch = blocks.setup_textbox(parent, font=self.txt_font)
        self.textbox_dch.insert("1.0", channels)


class DownloadSinglePage:
    """Mixin class to provide the download single page to the application."""
    def setup_page_d(self, parent):
        self.setup_top_d(parent)
        self.setup_textbox_d(parent)

    def setup_top_d(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_d(frame, start=0)
        self.setup_grid_button_d(frame, start=1)
        self.setup_grid_check_d(frame, start=3)
        self.setup_info_d(frame, start=5)

    def setup_grid_top_d(self, parent, start=0):
        blocks.setup_download_entry(parent,
                                    dir_var=self.down_dir_var,
                                    font=self.e_font,
                                    start=start)

    def setup_grid_button_d(self, parent, start=0):
        blocks.setup_button_resolve_claims(parent,
                                           width=self.b_width,
                                           resolve_func=self.resolve_claims,
                                           start=start)

        b_download = ttk.Button(parent, text="Download claims",
                                width=self.b_width,
                                command=self.download_claims)
        b_download.grid(row=start+1, column=0)
        b_download.bind("<<Activate>>",
                        blocks.f_with_event(self.download_claims))

        l2 = ttk.Label(parent,
                       text="Start downloading the claims")
        l2.grid(row=start+1, column=1, sticky=tk.W, padx=2)

    def setup_grid_check_d(self, parent, start=0):
        blocks.setup_download_check(parent,
                                    own_dir_var=self.own_dir_var,
                                    save_var=self.save_var,
                                    start=start)

    def setup_info_d(self, parent, start=0):
        blocks.info_claims(parent, start=start)

    def setup_textbox_d(self, parent):
        claims = blocks.set_up_default_claims()
        self.textbox_d = blocks.setup_textbox(parent, font=self.txt_font)
        self.textbox_d.insert("1.0", claims)


class ListPage:
    """Mixin class to provide the list page to the application."""
    def setup_page_list(self, parent):
        self.setup_top_list(parent)
        self.setup_textbox_list(parent)

    def setup_top_list(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_list(frame, start=0)
        self.setup_grid_check_list(frame, start=2)

    def setup_grid_top_list(self, parent, start=0):
        b_list = ttk.Button(parent, text="List claims",
                            width=self.b_width,
                            command=self.list_claims)
        b_list.grid(row=start, column=0)
        b_list.bind("<<Activate>>",
                    blocks.f_with_event(self.list_claims))

        llist = ttk.Label(parent,
                          text="List all locally downloaded claims")
        llist.grid(row=start, column=1, sticky=tk.W, padx=2)

        self.entry_chan = tk.StringVar()
        entry = ttk.Entry(parent,
                          textvariable=self.entry_chan,
                          font=self.e_font)
        entry.grid(row=start+1, column=0, sticky=tk.W + tk.E)
        entry.bind("<<Activate>>",
                   blocks.f_with_event(self.list_claims))

        le = ttk.Label(parent,
                       text="Filter by channel name")
        le.grid(row=start+1, column=1, sticky=tk.W, padx=2)

    def setup_grid_check_list(self, parent, start=0):
        blocks.setup_check_list(parent,
                                cid_var=self.check_cid,
                                blobs_var=self.check_blobs,
                                show_ch_var=self.check_show_ch,
                                name_var=self.check_name,
                                start=start)

    def setup_textbox_list(self, parent):
        self.textbox_list = blocks.setup_textbox(parent,
                                                 font=self.txt_lst_font)


class DeletePage:
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
        blocks.setup_button_resolve_claims(parent,
                                           width=self.b_width,
                                           resolve_func=self.resolve_claims,
                                           start=start)

        b_del = ttk.Button(parent, text="Delete claims",
                           width=self.b_width,
                           command=self.del_claims)
        b_del.grid(row=start+1, column=0)
        ldel = ttk.Label(parent,
                         text="Delete locally downloaded claims")
        ldel.grid(row=start+1, column=1, sticky=tk.W, padx=2)

    def setup_grid_radio_del(self, parent, start=0):
        blocks.setup_delete_radio(parent,
                                  del_what_var=self.del_what_var,
                                  start=start)

    def setup_info_del(self, parent, start=0):
        blocks.info_claims(parent, start=start)

    def setup_textbox_del(self, parent):
        claims = blocks.set_up_default_claims(clean_up=True)
        self.textbox_del = blocks.setup_textbox(parent, font=self.txt_font)
        self.textbox_del.insert("1.0", claims)


class DeleteChPage:
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
        blocks.setup_buttons_val_res(parent,
                                     width=self.b_width,
                                     validate_func=self.validate_ch,
                                     resolve_func=self.resolve_ch,
                                     start=start)

        b_clean = ttk.Button(parent, text="Clean up claims",
                             width=self.b_width,
                             command=self.delete_ch)
        b_clean.grid(row=start+2, column=0)
        lb = ttk.Label(parent,
                       text=("Start deleting claims "
                             "from the oldest to the newest"))
        lb.grid(row=start+2, column=1, sticky=tk.W, padx=2)

    def setup_grid_radio_delch(self, parent, start=0):
        blocks.setup_delete_radio(parent,
                                  del_what_var=self.del_what_var,
                                  start=start)

    def setup_info_delch(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Add a channel, a comma, "
                               "and the number of items to keep "
                               "from this channel; older items "
                               "will be removed"))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_delch(self, parent):
        channels = blocks.set_up_default_channels(clean_up=True)
        self.textbox_delch = blocks.setup_textbox(parent, font=self.txt_font)
        self.textbox_delch.insert("1.0", channels)
