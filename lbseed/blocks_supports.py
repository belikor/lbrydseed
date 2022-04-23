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
"""Basic building blocks for the GUI that are used in support pages."""
import tkinter as tk
import tkinter.ttk as ttk


def setup_check_support(parent,
                        show_ch_var=None,
                        show_claims_var=None,
                        show_cid_var=None,
                        show_invalid_var=None,
                        combine_var=None,
                        start=0):
    """Setup the checkbuttons to list supports."""
    chck_ch = ttk.Checkbutton(parent,
                              variable=show_ch_var,
                              text="Show channel claims")
    chck_ch.grid(row=start, column=1, sticky=tk.W)

    chck_claims = ttk.Checkbutton(parent,
                                  variable=show_claims_var,
                                  text=("Show stream claims "
                                        "(video, audio, document, etc.)"))
    chck_claims.grid(row=start+1, column=1, sticky=tk.W)

    chck_cid = ttk.Checkbutton(parent,
                               variable=show_cid_var,
                               text="Show claim ID")
    chck_cid.grid(row=start+2, column=1, sticky=tk.W)

    chck_combine = ttk.Checkbutton(parent,
                                   variable=combine_var,
                                   text="Show combined trending score")
    chck_combine.grid(row=start+3, column=1, sticky=tk.W)

    chck_inv = ttk.Checkbutton(parent,
                               variable=show_invalid_var,
                               text="Only show 'invalid' claims")
    chck_inv.grid(row=start+4, column=1, sticky=tk.W)


def setup_radio_support(parent,
                        support_how_var=None,
                        support_inv_var=None,
                        support_inv_cmd=None,
                        start=0):
    """Setup the radiobuttons to choose how to support claims."""
    r_create = ttk.Radiobutton(parent,
                               text=("Create a new support, regardless "
                                     "of previous supports.\n"
                                     "The number represets our support "
                                     "that will be created, and added\n"
                                     "to the 'existing' support. "
                                     "The number must be larger than 0.\n"
                                     "new_total = existing + ours\n"),
                               variable=support_how_var,
                               value="create")

    r_abandon = ttk.Radiobutton(parent,
                                text=("Abandon or change "
                                      "our support.\n"
                                      "The number represents our support "
                                      "that will be added to "
                                      "the 'base' support.\n"
                                      "If there is a previous support "
                                      "it will be discarded, and a new "
                                      "support will be made.\n"
                                      "If the number is 0, our previous "
                                      "support will be removed completely.\n"
                                      "old_total = base + ours_old\n"
                                      "new_total = base + ours_new\n"),
                                variable=support_how_var,
                                value="abandon_change")

    r_target = ttk.Radiobutton(parent,
                               text=("Target a specific total support.\n"
                                     "The number represents the final "
                                     "support that the claim should have.\n"
                                     "We will add support or reduce "
                                     "our support in order to reach "
                                     "the target.\n"
                                     "The target should be larger than "
                                     "the 'base' support, otherwise\n"
                                     "our existing support "
                                     "will be completely removed.\n"
                                     "old_total = base + ours_old\n"
                                     "target = base + ours_new\n"),
                               variable=support_how_var,
                               value="target")

    chck_inv = ttk.Checkbutton(parent,
                               variable=support_inv_var,
                               text=("Consider the claims as 'invalid'. "
                                     "Invalid claims no longer resolve "
                                     "online\n"
                                     "so their support "
                                     "should be removed or diminished.\n"
                                     "These are shown in the list "
                                     "of supports within '[brackets]'.\n"
                                     "In the textbox, write them "
                                     "without the brackets."),
                               command=support_inv_cmd)

    r_create.grid(row=start, column=1, sticky=tk.W, pady=4)
    r_abandon.grid(row=start+1, column=1, sticky=tk.W, pady=4)
    r_target.grid(row=start+2, column=1, sticky=tk.W, pady=4)
    chck_inv.grid(row=start+3, column=1, sticky=tk.W)

    return r_create, r_abandon, r_target
