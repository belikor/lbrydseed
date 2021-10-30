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


class TrendPage:
    def setup_page_trend(self, parent):
        self.setup_top_trend(parent)
        self.setup_textbox_trend(parent)

    def setup_top_trend(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_button_trend(frame, start=0)
        self.setup_grid_chck_trend_top(frame, start=2)
        self.setup_grid_radio_trend_claims(frame, start=3, col=0)
        self.setup_grid_chck_trend_streams(frame, start=3, col=1)
        self.setup_info_trend(frame, start=4)

    def setup_grid_button_trend(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Show trending claims",
                                b_command=self.show_trending_claims,
                                l_text=("Display trending claims "
                                        "in the network"),
                                start=start)

        spin, lb = blocks.setup_spin_page(parent,
                                          s_text_var=self.spin_page,
                                          s_command=self.show_trending_claims,
                                          l_text=("Page to search"),
                                          start=start+1)

        spin["width"] = 25
        spin.grid_forget()
        spin.grid(row=start+1, column=0)

    def setup_grid_chck_trend_top(self, parent, start=0):
        chck_cid = ttk.Checkbutton(parent,
                                   variable=self.chck_tr_cid,
                                   text=("Show claim ID"))
        chck_cid.grid(row=start, column=1, sticky=tk.W)

    def setup_grid_radio_trend_claims(self, parent, start=0, col=1):
        frame = ttk.Frame(parent, relief="groove", borderwidth=2)
        frame.grid(row=start, column=col, sticky=tk.W + tk.E + tk.N)

        blocks.setup_radio_trend_claims(frame,
                                        claim_type_var=self.chck_tr_claim_t,
                                        activate_func=self.activate_tr_checks,
                                        deactivate_func=self.deactivate_tr_checks,
                                        start=0, col=0)

    def deactivate_tr_checks(self):
        self.chck_tr_all.set(True)
        variables = [self.chck_tr_vid, self.chck_tr_audio,
                     self.chck_tr_doc, self.chck_tr_img,
                     self.chck_tr_bin, self.chck_tr_model]

        for v in variables:
            v.set(False)

        widgets = [self.tr_chck_all, self.tr_chck_vid,
                   self.tr_chck_audio, self.tr_chck_doc,
                   self.tr_chck_img, self.tr_chck_bin,
                   self.tr_chck_model]

        for widget in widgets:
            widget["state"] = "disabled"

    def activate_tr_checks(self):
        widgets = [self.tr_chck_all, self.tr_chck_vid,
                   self.tr_chck_audio, self.tr_chck_doc,
                   self.tr_chck_img, self.tr_chck_bin,
                   self.tr_chck_model]

        for widget in widgets:
            widget["state"] = "enabled"

    def setup_grid_chck_trend_streams(self, parent, start=0, col=1):
        frame = ttk.Frame(parent, relief="groove", borderwidth=2)
        frame.grid(row=start, column=col, sticky=tk.W + tk.E + tk.N)

        (self.tr_chck_all,
         self.tr_chck_vid,
         self.tr_chck_audio,
         self.tr_chck_doc,
         self.tr_chck_img,
         self.tr_chck_bin,
         self.tr_chck_model) = \
            blocks.setup_check_trend(frame,
                                     all_var=self.chck_tr_all,
                                     all_command=self.switch_tr_all,
                                     video_var=self.chck_tr_vid,
                                     audio_var=self.chck_tr_audio,
                                     doc_var=self.chck_tr_doc,
                                     image_var=self.chck_tr_img,
                                     bin_var=self.chck_tr_bin,
                                     model_var=self.chck_tr_model,
                                     not_all_command=self.switch_tr_various,
                                     start=0, col=0)

    def switch_tr_all(self):
        """Change variables if all claims are considered."""
        variables = [self.chck_tr_vid, self.chck_tr_audio,
                     self.chck_tr_doc, self.chck_tr_img,
                     self.chck_tr_bin, self.chck_tr_model]

        if self.chck_tr_all.get():
            for v in variables:
                v.set(False)
        else:
            self.chck_tr_vid.set(True)
            self.chck_tr_doc.set(True)

    def switch_tr_various(self):
        """If any stream checkbox is used, it is not all claims anymore."""
        if (self.chck_tr_vid.get()
                or self.chck_tr_audio.get()
                or self.chck_tr_doc.get()
                or self.chck_tr_img.get()
                or self.chck_tr_bin.get()
                or self.chck_tr_model.get()):
            self.chck_tr_all.set(False)
        if (not self.chck_tr_vid.get()
                and not self.chck_tr_audio.get()
                and not self.chck_tr_doc.get()
                and not self.chck_tr_img.get()
                and not self.chck_tr_bin.get()
                and not self.chck_tr_model.get()):
            self.chck_tr_all.set(True)

    def setup_info_trend(self, parent, start=0):
        blocks.info_search(parent, start=start)

        page = ttk.Label(parent, textvariable=self.label_tr_info)
        page.grid(row=start+1, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_trend(self, parent):
        self.textbox_trend = blocks.setup_textbox(parent,
                                                  font=self.txt_lst_font)
