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
"""Basic building blocks that are used in the controlling claim page."""
import tkinter as tk
import tkinter.ttk as ttk


def setup_check_controlling(parent,
                            contr_var=None,
                            non_contr_var=None,
                            skip_repost_var=None,
                            ch_only_var=None,
                            start=0):
    """Setup the checkbuttons to show controlling claims."""
    chck_contr = ttk.Checkbutton(parent,
                                 variable=contr_var,
                                 text=("Show controlling claims "
                                       "(highest bids)"))
    chck_contr.grid(row=start, column=1, sticky=tk.W)

    chck_non_contr = ttk.Checkbutton(parent,
                                     variable=non_contr_var,
                                     text=("Show non-controlling claims "
                                           "(lower bids)"))
    chck_non_contr.grid(row=start+1, column=1, sticky=tk.W)

    chck_repost = ttk.Checkbutton(parent,
                                  variable=skip_repost_var,
                                  text="Skip reposts")
    chck_repost.grid(row=start+2, column=1, sticky=tk.W)

    chck_channel = ttk.Checkbutton(parent,
                                   variable=ch_only_var,
                                   text="Only show channels")
    chck_channel.grid(row=start+3, column=1, sticky=tk.W)


def setup_check_contr_compact(parent,
                              compact_var=None,
                              compact_command=None,
                              cid_var=None,
                              is_repost_var=None,
                              n_competing_var=None,
                              n_reposts_var=None,
                              start=0):
    """Setup the checkbuttons that work only with the compact option."""
    chck_compact = ttk.Checkbutton(parent,
                                   variable=compact_var,
                                   text=("Compact information "
                                         "(one claim per row)"),
                                   command=compact_command)
    chck_compact.grid(row=start, column=1, sticky=tk.W)

    chck_claim_id = ttk.Checkbutton(parent,
                                    variable=cid_var,
                                    text="Show claim ID")
    chck_claim_id.grid(row=start+1, column=1, sticky=tk.W)

    chck_is_repost = ttk.Checkbutton(parent,
                                     variable=is_repost_var,
                                     text="Indicate if the claim is a repost")
    chck_is_repost.grid(row=start+2, column=1, sticky=tk.W)

    chck_competing = ttk.Checkbutton(parent,
                                     variable=n_competing_var,
                                     text=("Show how many competing claims "
                                           "there are with the same name"))
    chck_competing.grid(row=start+3, column=1, sticky=tk.W)

    chck_reposts = ttk.Checkbutton(parent,
                                   variable=n_reposts_var,
                                   text=("Show how many reposts "
                                         "there are of this claim"))
    chck_reposts.grid(row=start+4, column=1, sticky=tk.W)

    return chck_claim_id, chck_is_repost, chck_competing, chck_reposts
