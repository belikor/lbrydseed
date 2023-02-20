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
"""Basic building blocks for the GUI that are used in listing pages."""
import tkinter as tk
import tkinter.ttk as ttk


def setup_check_list(parent,
                     blocks_var=None,
                     cid_var=None,
                     blobs_var=None,
                     size_var=None,
                     show_ch_var=None,
                     start=0):
    """Setup the checkbuttons to list various properties."""
    chck_blks = ttk.Checkbutton(parent,
                                variable=blocks_var,
                                text="Show block height")
    chck_blks.grid(row=start, column=1, sticky=tk.W)

    chck_cid = ttk.Checkbutton(parent,
                               variable=cid_var,
                               text="Show claim ID (40-character string)")
    chck_cid.grid(row=start+1, column=1, sticky=tk.W)

    chck_blobs = ttk.Checkbutton(parent,
                                 variable=blobs_var,
                                 text=("Show number of blobs "
                                       "(each blob is 2 MB)"))
    chck_blobs.grid(row=start+2, column=1, sticky=tk.W)

    chck_size = ttk.Checkbutton(parent,
                                variable=size_var,
                                text=("Show length of claim (mm:ss) "
                                      "and total size (MB)"))
    chck_size.grid(row=start+3, column=1, sticky=tk.W)

    chck_ch = ttk.Checkbutton(parent,
                              variable=show_ch_var,
                              text="Show signing channel of the claim")
    chck_ch.grid(row=start+4, column=1, sticky=tk.W)


def setup_radio_list(parent,
                     name_var=None,
                     start=0):
    """Set up the radiobuttons to choose what to display as name."""
    name = ttk.Radiobutton(parent,
                           text="Show claim name",
                           variable=name_var, value="name")
    title = ttk.Radiobutton(parent,
                            text="Show claim title",
                            variable=name_var, value="title")
    path = ttk.Radiobutton(parent,
                           text="Show path of the existing media file",
                           variable=name_var, value="path")
    name.grid(row=start, column=1, sticky=tk.W)
    title.grid(row=start+1, column=1, sticky=tk.W)
    path.grid(row=start+2, column=1, sticky=tk.W)


def setup_check_ch_list(parent,
                        create_var=None,
                        height_var=None,
                        release_var=None,
                        cid_var=None,
                        type_var=None,
                        chname_var=None,
                        sizes_var=None,
                        supp_var=None,
                        fees_var=None,
                        title_var=None,
                        reverse_var=None,
                        start=0):
    """Setup the checkbuttons to control displaying properties of claims."""
    chck_create = ttk.Checkbutton(parent,
                                  variable=create_var,
                                  text=("Show the creation block height\n"
                                        "and creation time"))
    chck_create.grid(row=start, column=0, sticky=tk.W)

    chck_height = ttk.Checkbutton(parent,
                                  variable=height_var,
                                  text=("Show the block height "
                                        "and timestamp"))
    chck_height.grid(row=start+1, column=0, sticky=tk.W)

    chck_release = ttk.Checkbutton(parent,
                                   variable=release_var,
                                   text=("Show the release time"))
    chck_release.grid(row=start+2, column=0, sticky=tk.W)

    chck_cid = ttk.Checkbutton(parent,
                               variable=cid_var,
                               text="Show claim ID (40-character string)")
    chck_cid.grid(row=start+3, column=0, sticky=tk.W)

    chck_type = ttk.Checkbutton(parent,
                                variable=type_var,
                                text=("Show the type of claim, stream, "
                                      "and media,\n"
                                      "if applicable"))
    chck_type.grid(row=start+4, column=0, sticky=tk.W)

    chck_chname = ttk.Checkbutton(parent,
                                  variable=chname_var,
                                  text=("Show the name of the channel"))
    chck_chname.grid(row=start, column=1, sticky=tk.W)

    chck_size = ttk.Checkbutton(parent,
                                variable=sizes_var,
                                text=("Show the duration and size, "
                                      "if applicable"))
    chck_size.grid(row=start+1, column=1, sticky=tk.W)

    chck_supp = ttk.Checkbutton(parent,
                                variable=supp_var,
                                text=("Show the total LBC support "
                                      "on the claim"))
    chck_supp.grid(row=start+2, column=1, sticky=tk.W)

    chck_fees = ttk.Checkbutton(parent,
                                variable=fees_var,
                                text=("Show the fee to access the claim, "
                                      "if applicable"))
    chck_fees.grid(row=start+3, column=1, sticky=tk.W)

    chck_title = ttk.Checkbutton(parent,
                                 variable=title_var,
                                 text=("Show the claim 'title' "
                                       "instead of the claim 'name'"))
    chck_title.grid(row=start+4, column=1, sticky=tk.W)

    chck_reverse = ttk.Checkbutton(parent,
                                   variable=reverse_var,
                                   text=("Show in descending order "
                                         "(newer items first, older last)"))
    chck_reverse.grid(row=start+5, column=1, sticky=tk.W)
