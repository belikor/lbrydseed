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
"""Mixin classes that add advanced pages to the main graphical interface.

These classes should not be instantiatied directly. They are just used
in a multiple inheritance, or mixin pattern, to provide the necessary
building command to build the specific page in the main interface.

::
    class SeedPage:
        def setup_page_seed(self, parent):
            ...

    class Application(ttk.Frame, SeedPage):
        def __init__(self, root):
            page_seed_ratio = ttk.Frame(root)
            self.setup_page_seed(page_seed_ratio)
"""

import tkinter as tk
import tkinter.ttk as ttk

import lbseed.blocks as blocks


class SeedPage:
    """Mixin class to provide the seeding page to the application."""
    def setup_page_seed(self, parent):
        self.setup_top_seed(parent)
        self.setup_textbox_seed(parent)
        self.setup_plot()

    def setup_top_seed(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_button_seed(frame, start=0)
        self.setup_grid_check_seed(frame, start=1)
        self.setup_info_seed(frame, start=2)

    def setup_grid_button_seed(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Display seeding ratio",
                                b_command=self.seeding_ratio,
                                l_text=("This is an estimation of uploaded "
                                        "and downloaded blobs\n"
                                        "based on information found "
                                        "in the log files."),
                                start=start)

    def setup_grid_check_seed(self, parent, start=0):
        chk_plot = ttk.Checkbutton(parent,
                                   variable=self.check_seed_plot,
                                   text=("Plot histograms of blob activity "
                                         "(requires Matplotlib)"))
        chk_plot.grid(row=start, column=1, sticky=tk.W)

    def setup_info_seed(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("If uploaded blobs is 0, "
                               "make sure the ports 3333 and 4444 "
                               "are forwarded in your router."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_seed(self, parent):
        self.textbox_seed = blocks.setup_textbox(parent,
                                                 font=self.txt_lst_font)

    def setup_plot(self):
        self.top_plot = tk.Toplevel()
        self.top_plot.withdraw()
        self.top_plot.title("Upload/download seeding ratio")
        self.top_plot.protocol("WM_DELETE_WINDOW", self.remove_plot)
        return self.top_plot

    def remove_plot(self):
        self.top_plot.withdraw()

        values = list(self.top_plot.children.values())
        for v in values:
            v.destroy()
        return self.top_plot


class ControllingClaimsPage:
    """Mixin class to provide the controlling claims page."""
    def setup_page_controlling(self, parent):
        self.setup_top_controlling(parent)
        self.setup_textbox_controlling(parent)

    def setup_top_controlling(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_button_contr(frame, start=0)
        self.setup_grid_check_contr(frame, start=1)
        self.setup_grid_check_contr_compact(frame, start=5)
        self.setup_info_contr(frame, start=6)

    def setup_grid_button_contr(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Display controlling claims",
                                b_command=self.controlling_claims,
                                l_text=('Show our claims, and whether '
                                        'we have the "controlling claim"\n'
                                        '(claim with the highest bid '
                                        'when compared to other claims '
                                        'of the same name)'),
                                start=start)

    def setup_grid_check_contr(self, parent, start=0):
        blocks.setup_check_controlling(parent,
                                       contr_var=self.check_c_contr,
                                       non_contr_var=self.check_c_non_contr,
                                       skip_repost_var=self.check_c_skip_repost,
                                       ch_only_var=self.check_c_ch_only,
                                       start=start)

    def setup_grid_check_contr_compact(self, parent, start=0):
        frame = ttk.Frame(parent, relief="groove", borderwidth=2)
        frame.grid(row=start, column=1, sticky=tk.W + tk.E)

        (self.chck_claim_id,
         self.chck_is_repost,
         self.chck_competing,
         self.chck_reposts) = \
             blocks.setup_check_contr_compact(frame,
                                              compact_var=self.check_c_compact,
                                              compact_command=self.compact_disable,
                                              cid_var=self.check_c_cid,
                                              is_repost_var=self.check_c_is_repost,
                                              n_competing_var=self.check_c_competing,
                                              n_reposts_var=self.check_c_reposts,
                                              start=0)

    def compact_disable(self):
        if self.check_c_compact.get():
            self.chck_claim_id["state"] = "normal"
            self.chck_is_repost["state"] = "normal"
            self.chck_competing["state"] = "normal"
            self.chck_reposts["state"] = "normal"
        else:
            self.chck_claim_id["state"] = "disabled"
            self.chck_is_repost["state"] = "disabled"
            self.chck_competing["state"] = "disabled"
            self.chck_reposts["state"] = "disabled"

    def setup_info_contr(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("'Staked' is the support in our claim while "
                               "'highest bid' is in a competing claim.\n"
                               "Note: at the moment the counters "
                               "for competing claims and reposts "
                               "goes to a maximum of 50.\n"
                               "This normally indicates that the claim "
                               "is very popular, and thus is reposted "
                               "by many users."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_controlling(self, parent):
        self.textbox_controlling = blocks.setup_textbox(parent,
                                                        font=self.txt_lst_font)
