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
"""Basic building blocks for the GUI that are used in listing claims pages."""
import tkinter as tk
import tkinter.ttk as ttk


def setup_check_chs_claims(parent,
                           spent_var=None,
                           update_var=None,
                           cid_var=None,
                           addr_var=None,
                           acc_var=None,
                           amount_var=None,
                           reverse_var=None,
                           start=0):
    """Setup the checkbuttons to list channel claims."""
    chck_spent = ttk.Checkbutton(parent,
                                 variable=spent_var,
                                 text=("Show spent transactions\n"
                                       "(it may show expired claims)"))
    chck_spent.grid(row=start, column=0, sticky=tk.W)

    chck_up = ttk.Checkbutton(parent,
                              variable=update_var,
                              text="Show time of last update")
    chck_up.grid(row=start+1, column=0, sticky=tk.W)

    chck_cid = ttk.Checkbutton(parent,
                               variable=cid_var,
                               text=("Show claim ID "
                                     "(40-character string)"))
    chck_cid.grid(row=start, column=1, sticky=tk.W)

    chck_addr = ttk.Checkbutton(parent,
                                variable=addr_var,
                                text=("Show addresses "
                                      "(34-character string)"))
    chck_addr.grid(row=start+1, column=1, sticky=tk.W)

    chck_acc = ttk.Checkbutton(parent,
                               variable=acc_var,
                               text=("Show accounts "
                                     "(34-character string)"))
    chck_acc.grid(row=start+2, column=1, sticky=tk.W)

    chck_amount = ttk.Checkbutton(parent,
                                  variable=amount_var,
                                  text=("Show amounts "
                                        "(base and total)"))
    chck_amount.grid(row=start+3, column=1, sticky=tk.W)

    chck_rv = ttk.Checkbutton(parent,
                              variable=reverse_var,
                              text=("Show in descending order "
                                    "(newer items first, older last)"))
    chck_rv.grid(row=start+4, column=1, sticky=tk.W)


def setup_check_claims(parent,
                       spent_var=None,
                       update_var=None,
                       cid_var=None,
                       addr_var=None,
                       type_var=None,
                       amount_var=None,
                       title_var=None,
                       reverse_var=None,
                       start=0):
    """Setup the checkbuttons to list claims."""
    chck_spent = ttk.Checkbutton(parent,
                                 variable=spent_var,
                                 text=("Show spent transactions\n"
                                       "(it may show expired claims)"))
    chck_spent.grid(row=start, column=0, sticky=tk.W)

    chck_up = ttk.Checkbutton(parent,
                              variable=update_var,
                              text="Show time of last update")
    chck_up.grid(row=start+1, column=0, sticky=tk.W)

    chck_cid = ttk.Checkbutton(parent,
                               variable=cid_var,
                               text=("Show claim ID "
                                     "(40-character string)"))
    chck_cid.grid(row=start, column=1, sticky=tk.W)

    chck_addr = ttk.Checkbutton(parent,
                                variable=addr_var,
                                text=("Show addresses "
                                      "(34-character string)"))
    chck_addr.grid(row=start+1, column=1, sticky=tk.W)

    chck_typ = ttk.Checkbutton(parent,
                               variable=type_var,
                               text=("Show the type of claim, "
                                     "stream, and media, if available"))
    chck_typ.grid(row=start+2, column=1, sticky=tk.W)

    chck_amount = ttk.Checkbutton(parent,
                                  variable=amount_var,
                                  text=("Show amounts "
                                        "(base and total)"))
    chck_amount.grid(row=start+3, column=1, sticky=tk.W)

    chck_title = ttk.Checkbutton(parent,
                                 variable=title_var,
                                 text=("Show the claim 'title' "
                                       "instead of the claim 'name'"))
    chck_title.grid(row=start+4, column=1, sticky=tk.W)

    chck_rv = ttk.Checkbutton(parent,
                              variable=reverse_var,
                              text=("Show in descending order "
                                    "(newer items first, older last)"))
    chck_rv.grid(row=start+5, column=1, sticky=tk.W)
