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
"""Basic building blocks for channel subscription pages."""
import tkinter as tk
import tkinter.ttk as ttk


def setup_radio_ch_subs_shared(parent,
                               shared_var=None,
                               start=0):
    """Set up the radiobuttons to choose what database to display."""
    shared = ttk.Radiobutton(parent,
                             text="Shared database",
                             variable=shared_var, value="shared")

    local = ttk.Radiobutton(parent,
                            text="Local database",
                            variable=shared_var, value="local")

    shared.grid(row=start, column=1, sticky=tk.W)
    local.grid(row=start+1, column=1, sticky=tk.W)


def setup_radio_ch_subs_valid(parent,
                              show_var=None,
                              start=0):
    """Set up the radiobuttons to choose what channels to display."""
    show_all = ttk.Radiobutton(parent,
                               text="Show all channels",
                               variable=show_var, value="show_all")

    show_valid = ttk.Radiobutton(parent,
                                 text=("Show valid channels only "
                                       "(they resolve online)"),
                                 variable=show_var, value="show_valid")

    show_invalid = ttk.Radiobutton(parent,
                                   text=("Show invalid channels only "
                                         "(they were removed)"),
                                   variable=show_var, value="show_invalid")

    show_all.grid(row=start, column=1, sticky=tk.W)
    show_valid.grid(row=start+1, column=1, sticky=tk.W)
    show_invalid.grid(row=start+2, column=1, sticky=tk.W)


def setup_radio_ch_subs_valid2(parent,
                               show_var=None,
                               start=0):
    """Set up the radiobuttons to choose what channels to display."""
    show_all = ttk.Radiobutton(parent,
                               text="Show all channels",
                               variable=show_var, value="show_all")
    show_valid = ttk.Radiobutton(parent,
                                 text=("Show valid channels only "
                                       "(they resolve online)"),
                                 variable=show_var, value="show_valid")
    show_all.grid(row=start, column=1, sticky=tk.W)
    show_valid.grid(row=start+1, column=1, sticky=tk.W)
