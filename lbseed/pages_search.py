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
"""Mixin classes that add trend and search pages to the graphical interface.

These classes should not be instantiatied directly. They are just used
in a multiple inheritance, or mixin pattern, to provide the necessary
building command to build the specific page in the main interface.

::
    class TrendPage:
        def setup_page_trend(self, parent):
            ...

    class Application(ttk.Frame, TrendPage):
        def __init__(self, root):
            page_trend = ttk.Frame(root)
            self.setup_page_trend(page_trend)
"""

import tkinter as tk
import tkinter.ttk as ttk

import lbseed.blocks as blocks


class TrendPage:
    def setup_page_trend(self, parent):
        self.setup_top_trend(parent)
        self.setup_textbox_trend(parent)

    def setup_top_trend(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_button_trend(frame, start=0)
        self.setup_grid_chck_trend_top(frame, start=3)
        self.setup_grid_radio_trend_claims(frame, start=8, col=0)
        self.setup_grid_chck_trend_streams(frame, start=8, col=1)
        self.setup_info_trend(frame, start=9)

    def setup_grid_button_trend(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Show trending claims",
                                b_command=self.list_trending_claims,
                                l_text=("Display trending claims "
                                        "in the network"),
                                start=start)

        spin, lb = blocks.setup_spin_gen(parent,
                                         frm=0, to=20, incr=1,
                                         default=0,
                                         s_text_var=self.spin_sr_page,
                                         s_command=self.list_trending_claims,
                                         l_text=("Page to search; "
                                                 "use 0 to display all pages\n"
                                                 "(1000 claims maximum)"),
                                         start=start+1)
        spin["width"] = 25
        spin.grid_forget()
        spin.grid(row=start+1, column=0)

        sp, lb = blocks.setup_spin_gen(parent,
                                       frm=0, to=512, incr=1,
                                       default=32,
                                       s_text_var=self.spin_sr_threads,
                                       s_command=self.list_trending_claims,
                                       l_text=("Number of threads to resolve "
                                               "pages in parallel; "
                                               "use 0 to avoid threads"),
                                       start=start+2)
        sp["width"] = 25
        sp.grid_forget()
        sp.grid(row=start+2, column=0)

    def setup_grid_chck_trend_top(self, parent, start=0):
        blocks.setup_check_trend_fields(parent,
                                        create_var=self.chck_sr_create,
                                        height_var=self.chck_sr_height,
                                        release_var=self.chck_sr_release,
                                        cid_var=self.chck_sr_cid,
                                        type_var=self.chck_sr_typ,
                                        chname_var=self.chck_sr_chname,
                                        sizes_var=self.chck_sr_sizes,
                                        fees_var=self.chck_sr_fees,
                                        title_var=self.chck_sr_title,
                                        start=start)

    def setup_grid_radio_trend_claims(self, parent, start=0, col=1):
        frame = ttk.Frame(parent, relief="groove", borderwidth=2)
        frame.grid(row=start, column=col, sticky=tk.W + tk.E + tk.N)

        blocks.setup_radio_trend_claims(frame,
                                        claim_type_var=self.rad_sr_claim,
                                        activate_func=self.activate_tr_checks,
                                        deactivate_func=self.deact_tr_checks,
                                        start=0, col=0)

    def deact_tr_checks(self):
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
            blocks.setup_check_trend_typ(frame,
                                         all_var=self.chck_tr_all,
                                         all_command=self.switch_tr_all,
                                         video_var=self.chck_tr_vid,
                                         audio_var=self.chck_tr_audio,
                                         doc_var=self.chck_tr_doc,
                                         image_var=self.chck_tr_img,
                                         bin_var=self.chck_tr_bin,
                                         model_var=self.chck_tr_model,
                                         not_all_cmd=self.switch_tr_various,
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

    def setup_textbox_trend(self, parent):
        self.textbox_trend = blocks.setup_textbox(parent,
                                                  font=self.txt_lst_font)


class SearchPage:
    def setup_page_search(self, parent):
        self.setup_top_search(parent)
        self.setup_textbox_search(parent)

    def setup_top_search(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_button_search(frame, start=0)
        self.setup_grid_entry_search(frame, start=3)
        self.setup_grid_chck_search_top(frame, start=5)
        self.setup_grid_radio_search_claims(frame, start=10, col=0)
        self.setup_grid_chck_search_stream(frame, start=10, col=1)
        self.setup_info_search(frame, start=11)

    def setup_grid_button_search(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Search",
                                b_command=self.list_search,
                                l_text=("Search claims in the network.\n"
                                        "These results are obtained from "
                                        "the 'claim_search' method\n"
                                        "of the SDK, "
                                        "so they aren't very accurate."),
                                start=start)

        spin, lb = blocks.setup_spin_gen(parent,
                                         frm=0, to=20, incr=1,
                                         default=0,
                                         s_text_var=self.spin_sr_page,
                                         s_command=self.list_search,
                                         l_text=("Page to search; "
                                                 "use 0 to display all pages\n"
                                                 "(1000 claims maximum)"),
                                         start=start+1)
        spin["width"] = 25
        spin.grid_forget()
        spin.grid(row=start+1, column=0)

        sp, lb = blocks.setup_spin_gen(parent,
                                       frm=0, to=512, incr=1,
                                       default=32,
                                       s_text_var=self.spin_sr_threads,
                                       s_command=self.list_search,
                                       l_text=("Number of threads to resolve "
                                               "pages in parallel; "
                                               "use 0 to avoid threads"),
                                       start=start+2)
        sp["width"] = 25
        sp.grid_forget()
        sp.grid(row=start+2, column=0)

    def setup_grid_entry_search(self, parent, start=0):
        frame1 = ttk.Frame(parent)
        frame1.grid(row=start, columnspan=2, sticky=tk.W, pady=6)

        lb1 = ttk.Label(frame1, text="Text:", width=5)

        entry = ttk.Entry(frame1,
                          width=40,
                          textvariable=self.sr_entry,
                          font=None)

        entry.bind("<<Activate>>", blocks.f_with_event(self.list_search))

        lb1r = ttk.Label(frame1, text=("String to search. "
                                       "Use a small number of terms, "
                                       "as using many words\n"
                                       "may produce no results.\n"
                                       "Surround the entire "
                                       "string with double "
                                       'quotation "marks"\n'
                                       "to search that string exactly."))

        lb1.grid(row=0, column=0, sticky=tk.N)
        entry.grid(row=0, column=1, sticky=tk.N)
        lb1r.grid(row=0, column=2, padx=3)

        frame2 = ttk.Frame(parent)
        frame2.grid(row=start+1, columnspan=2, sticky=tk.W, pady=6)

        lb2 = ttk.Label(frame2, text="Tags:", width=5)

        tags = ttk.Entry(frame2,
                         width=40,
                         textvariable=self.sr_entry_tags,
                         font=None)

        tags.bind("<<Activate>>", blocks.f_with_event(self.list_search))

        lb2r = ttk.Label(frame2, text=("Tags to search separated by commas "
                                       "(food, nature, music, etc.)."))

        lb2.grid(row=0, column=0)
        tags.grid(row=0, column=1)
        lb2r.grid(row=0, column=2, padx=3)

    def setup_grid_chck_search_top(self, parent, start=0):
        blocks.setup_check_trend_fields(parent,
                                        create_var=self.chck_sr_create,
                                        height_var=self.chck_sr_height,
                                        release_var=self.chck_sr_release,
                                        cid_var=self.chck_sr_cid,
                                        type_var=self.chck_sr_typ,
                                        chname_var=self.chck_sr_chname,
                                        sizes_var=self.chck_sr_sizes,
                                        fees_var=self.chck_sr_fees,
                                        title_var=self.chck_sr_title,
                                        start=start)

    def setup_grid_radio_search_claims(self, parent, start=0, col=1):
        frame = ttk.Frame(parent, relief="groove", borderwidth=2)
        frame.grid(row=start, column=col, sticky=tk.W + tk.E + tk.N)

        blocks.setup_radio_trend_claims(frame,
                                        claim_type_var=self.rad_sr_claim,
                                        activate_func=self.activate_sr_checks,
                                        deactivate_func=self.deact_sr_checks,
                                        start=0, col=0)

    def deact_sr_checks(self):
        self.chck_tr_all.set(True)
        variables = [self.chck_tr_vid, self.chck_tr_audio,
                     self.chck_tr_doc, self.chck_tr_img,
                     self.chck_tr_bin, self.chck_tr_model]

        for v in variables:
            v.set(False)

        widgets = [self.sr_chck_all, self.sr_chck_vid,
                   self.sr_chck_audio, self.sr_chck_doc,
                   self.sr_chck_img, self.sr_chck_bin,
                   self.sr_chck_model]

        for widget in widgets:
            widget["state"] = "disabled"

    def activate_sr_checks(self):
        widgets = [self.sr_chck_all, self.sr_chck_vid,
                   self.sr_chck_audio, self.sr_chck_doc,
                   self.sr_chck_img, self.sr_chck_bin,
                   self.sr_chck_model]

        for widget in widgets:
            widget["state"] = "enabled"

    def setup_grid_chck_search_stream(self, parent, start=0, col=1):
        frame = ttk.Frame(parent, relief="groove", borderwidth=2)
        frame.grid(row=start, column=col, sticky=tk.W + tk.E + tk.N)

        (self.sr_chck_all,
         self.sr_chck_vid,
         self.sr_chck_audio,
         self.sr_chck_doc,
         self.sr_chck_img,
         self.sr_chck_bin,
         self.sr_chck_model) = \
            blocks.setup_check_trend_typ(frame,
                                         all_var=self.chck_tr_all,
                                         all_command=self.switch_sr_all,
                                         video_var=self.chck_tr_vid,
                                         audio_var=self.chck_tr_audio,
                                         doc_var=self.chck_tr_doc,
                                         image_var=self.chck_tr_img,
                                         bin_var=self.chck_tr_bin,
                                         model_var=self.chck_tr_model,
                                         not_all_cmd=self.switch_sr_various,
                                         start=0, col=0)

    def switch_sr_all(self):
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

    def switch_sr_various(self):
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

    def setup_info_search(self, parent, start=0):
        blocks.info_search(parent, start=start)

    def setup_textbox_search(self, parent):
        self.textbox_search = blocks.setup_textbox(parent,
                                                   font=self.txt_lst_font)
