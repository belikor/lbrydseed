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
"""Mixin classes that add the listing pages to the main graphical interface.

These classes should not be instantiatied directly. They are just used
in a multiple inheritance, or mixin pattern, to provide the necessary
building command to build the specific page in the main interface.

::
    class ListPage:
        def setup_page_list(self, parent):
            ...

    class Application(ttk.Frame, ListPage):
        def __init__(self, root):
            page_list = ttk.Frame(root)
            self.setup_page_list(page_list)
"""

import tkinter as tk
import tkinter.ttk as ttk

import lbseed.blocks as blocks


class ListDownPage:
    """Mixin class to provide the list page to the application."""
    def setup_page_down_list(self, parent):
        self.setup_top_list(parent)
        self.setup_textbox_list(parent)

    def setup_top_list(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_list(frame, start=0)
        self.setup_grid_check_list(frame, start=2)
        self.setup_grid_radio_list(frame, start=7)
        self.setup_grid_check_reverse(frame, start=8)
        self.setup_info_list(frame, start=9)

    def setup_grid_top_list(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="List downloaded claims",
                                b_command=self.list_d_claims,
                                l_text="List all locally downloaded claims",
                                start=start)

        entry, label = \
            blocks.setup_entry_gen(parent,
                                   font=self.e_font,
                                   text_var=self.entry_chan,
                                   l_text="Filter by channel name",
                                   start=start+1)
        entry.bind("<<Activate>>", blocks.f_with_event(self.list_d_claims))

    def setup_grid_check_list(self, parent, start=0):
        blocks.setup_check_list(parent,
                                blocks_var=self.check_lst_blks,
                                cid_var=self.check_lst_cid,
                                blobs_var=self.check_lst_blobs,
                                size_var=self.check_lst_size,
                                show_ch_var=self.check_lst_show_ch,
                                start=start)

    def setup_grid_radio_list(self, parent, start=0):
        frame = ttk.Frame(parent, relief="groove", borderwidth=2)
        frame.grid(row=start, column=1, sticky=tk.W + tk.E + tk.N)

        blocks.setup_radio_list(frame,
                                name_var=self.rad_lst_name,
                                start=0)

    def setup_grid_check_reverse(self, parent, start=0):
        chk_reverse = \
            ttk.Checkbutton(parent,
                            variable=self.check_lst_reverse,
                            text=("Show in descending order "
                                  "(newer items first, older last)"))
        chk_reverse.grid(row=start, column=1, sticky=tk.W, pady=2)

    def setup_info_list(self, parent, start=0):
        desc = ttk.Label(parent,
                         text=("The 'size' corresponds to the size "
                               "of the downloaded blobs; "
                               "if all media files were to exist\n"
                               "the files would take double the space "
                               "on the hard drive.\n"
                               "The 'duration' considers only those "
                               "claims that have a duration, such as "
                               "video and audio files."))
        desc.grid(row=start, column=0, columnspan=2, sticky=tk.W)

        info = ttk.Label(parent, textvariable=self.label_lst_info)
        info.grid(row=start+1, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_list(self, parent):
        self.textbox_list = blocks.setup_textbox(parent,
                                                 font=self.txt_lst_font)


class ListDownInvalidPage:
    """Mixin class to provide the list of invalid claims page."""
    def setup_page_down_list_inv(self, parent):
        self.setup_top_list_inv(parent)
        self.setup_textbox_list_inv(parent)

    def setup_top_list_inv(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_list_inv(frame, start=0)
        self.setup_grid_check_list_inv(frame, start=2)
        self.setup_grid_radio_list_inv(frame, start=7)
        self.setup_grid_check_inv_reverse(frame, start=8)
        self.setup_grid_info_list_inv(frame, start=9)
        self.setup_info_list_inv(frame, start=10)

    def setup_grid_top_list_inv(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="List invalid claims",
                                b_command=self.list_d_claims_inv,
                                l_text=("List all locally downloaded claims "
                                        "that have become 'invalid'.\n"
                                        "This operation may take "
                                        "a long time as it needs to "
                                        "search all previously downloaded\n"
                                        "claims online."),
                                start=start)

        entry, label = \
            blocks.setup_entry_gen(parent,
                                   font=self.e_font,
                                   text_var=self.entry_chan,
                                   l_text="Filter by channel name",
                                   start=start+1)
        entry.bind("<<Activate>>", blocks.f_with_event(self.list_d_claims_inv))

    def setup_grid_check_list_inv(self, parent, start=0):
        blocks.setup_check_list(parent,
                                blocks_var=self.check_lst_blks,
                                cid_var=self.check_lst_cid,
                                blobs_var=self.check_lst_blobs,
                                size_var=self.check_lst_size,
                                show_ch_var=self.check_lst_show_ch,
                                start=start)

    def setup_grid_radio_list_inv(self, parent, start=0):
        frame = ttk.Frame(parent, relief="groove", borderwidth=2)
        frame.grid(row=start, column=1, sticky=tk.W + tk.E + tk.N)

        blocks.setup_radio_list(frame,
                                name_var=self.rad_lst_name,
                                start=0)

    def setup_grid_check_inv_reverse(self, parent, start=0):
        chk_reverse = \
            ttk.Checkbutton(parent,
                            variable=self.check_lst_reverse,
                            text=("Show in descending order "
                                  "(newer items first, older last)"))
        chk_reverse.grid(row=start, column=1, sticky=tk.W, pady=2)

    def setup_grid_info_list_inv(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("'Invalid' claims are those which "
                               "were downloaded at one point "
                               "but then they were removed "
                               "by their authors,\n"
                               "thus the claims "
                               "cannot be resolved online any more, "
                               "nor can they be re-downloaded.\n"
                               "The blobs belonging to these claims "
                               "can be considered orphaned, "
                               "and they can be removed\n"
                               "to free space in the hard drive."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_info_list_inv(self, parent, start=0):
        desc = ttk.Label(parent,
                         text=("The 'size' corresponds to the size "
                               "of the downloaded blobs; "
                               "if all media files were to exist\n"
                               "the files would take double the space "
                               "on the hard drive.\n"
                               "The 'duration' considers only those "
                               "claims that have a duration, such as "
                               "video and audio files."))
        desc.grid(row=start, column=0, columnspan=2, sticky=tk.W)

        info = ttk.Label(parent, textvariable=self.label_lst_inv_info)
        info.grid(row=start+1, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_list_inv(self, parent):
        self.textbox_list_inv = blocks.setup_textbox(parent,
                                                     font=self.txt_lst_font)


class ListChClaimsPage:
    """Mixin class to provide the list channel claims to the application."""
    def setup_page_ch_claims(self, parent):
        self.setup_top_ch_list(parent)
        self.setup_textbox_ch_list(parent)

    def setup_top_ch_list(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_ch_list(frame, start=0)
        self.setup_grid_check_ch_list(frame, start=4)
        self.setup_info_ch_list(frame, start=10)

    def setup_grid_top_ch_list(self, parent, start=0):
        entry, label = \
            blocks.setup_entry_gen(parent,
                                   font=self.e_font,
                                   text_var=self.entry_chl_chan,
                                   l_text="Channel to inspect",
                                   start=start)
        entry.bind("<<Activate>>", blocks.f_with_event(self.list_ch_claims))

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Resolve online",
                                b_command=self.resolve_ch_list,
                                l_text="Confirm that the channel exists",
                                start=start+1)

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="List channel claims",
                                b_command=self.list_ch_claims,
                                l_text=("List claims from the specified "
                                        "channel, "
                                        "starting from the newest one,\n"
                                        "and going back in time"),
                                start=start+2)

        spin_num, label = \
            blocks.setup_spin_page(parent,
                                   s_text_var=self.spin_chl_num,
                                   s_command=self.list_ch_claims,
                                   l_text=("Number of claims to display; "
                                           "use 0 to display all"),
                                   start=start+3)
        spin_num.set(0)
        spin_num["from_"] = 0.0
        spin_num["to"] = 100E3

    def setup_grid_check_ch_list(self, parent, start=0):
        blocks.setup_check_ch_list(parent,
                                   blocks_var=self.chck_chl_blk,
                                   cid_var=self.chck_chl_cid,
                                   type_var=self.chck_chl_type,
                                   chname_var=self.chck_chl_chname,
                                   title_var=self.chck_chl_title,
                                   reverse_var=self.chck_chl_reverse,
                                   start=start)

    def setup_info_ch_list(self, parent, start=0):
        desc = ttk.Label(parent,
                         text=("The 'size' corresponds to the size "
                               "of the downloaded blobs; "
                               "if all media files were to exist\n"
                               "the files would take double the space "
                               "on the hard drive.\n"
                               "The 'duration' considers only those "
                               "claims that have a duration, such as "
                               "video and audio files."))
        desc.grid(row=start, column=0, columnspan=2, sticky=tk.W)

        info = ttk.Label(parent, textvariable=self.label_chl_info)
        info.grid(row=start+1, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_ch_list(self, parent):
        self.textbox_ch_list = blocks.setup_textbox(parent,
                                                    font=self.txt_lst_font)


class SubscribedChsPage:
    """Mixin class to provide the list command for subscribed channels."""
    def setup_page_subscr_chs(self, parent):
        self.setup_top_ch_subs_list(parent)
        self.setup_textbox_ch_subs_list(parent)

    def setup_top_ch_subs_list(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_ch_subs(frame, start=0)
        self.setup_grid_rad_ch_subs(frame, start=3)
        self.setup_grid_spin_subs(frame, start=7)
        self.setup_info_ch_subs(frame, start=8)

    def setup_grid_top_ch_subs(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="List subscribed channels",
                                b_command=self.list_subscr_chs,
                                l_text=("(a) The subscribed channels "
                                        "reside in the wallet file\n"
                                        "but they are resolved online "
                                        "to confirm that they exist"),
                                start=start)

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="List subscribed channels claims",
                                b_command=self.list_subscr_chs_claims,
                                l_text=("(b) The newest claims "
                                        "for each channel will be shown"),
                                start=start+1)

        spin_num, label = \
            blocks.setup_spin_page(parent,
                                   s_text_var=self.spin_subs_claim_num,
                                   s_command=self.list_subscr_chs_claims,
                                   l_text=("(b) Number of claims to show "
                                           "per channel.\n"
                                           "It will take various minutes "
                                           "to load the full list\n"
                                           "if the number of channels "
                                           "and claims is large."),
                                   start=start+2)
        spin_num.set(5)
        spin_num["from_"] = 1
        spin_num["to"] = 20

    def setup_grid_rad_ch_subs(self, parent, start=0):
        frame = ttk.Frame(parent, relief="groove", borderwidth=2)
        frame.grid(row=start, column=1, sticky=tk.W + tk.E + tk.N)

        blocks.setup_radio_ch_subs_shared(frame,
                                          shared_var=self.rad_subs_shared,
                                          start=0)

        frame2 = ttk.Frame(parent, relief="groove", borderwidth=2)
        frame2.grid(row=start+1, column=1, sticky=tk.W + tk.E + tk.N)

        blocks.setup_radio_ch_subs_valid(frame2,
                                         show_var=self.rad_subs_show,
                                         start=0)

        chck_cid = ttk.Checkbutton(parent,
                                   variable=self.check_subs_claim_id,
                                   text=("Show claim ID "
                                         "(40-character string) "
                                         "of the channel (a)\n"
                                         "or the individual claims (b)."))
        chck_cid.grid(row=start+2, column=1, sticky=tk.W)

        chck_t = ttk.Checkbutton(parent,
                                 variable=self.check_subs_title,
                                 text=("Show the claim 'title' "
                                       "instead of the claim 'name' (b)."))
        chck_t.grid(row=start+3, column=1, sticky=tk.W)

    def setup_grid_spin_subs(self, parent, start=0):
        spin_num, label = \
            blocks.setup_spin_page(parent,
                                   s_text_var=self.spin_subs_threads,
                                   s_command=self.list_subscr_chs,
                                   l_text=("Number of threads to resolve "
                                           "the channels; "
                                           "use 0 to avoid threads"),
                                   start=start)
        spin_num.set(32)
        spin_num["from_"] = 0
        spin_num["to"] = 256

    def setup_info_ch_subs(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Channel subscriptions reside "
                               "in the wallet file in our local computer, "
                               "and optionally on Odysee servers,\n"
                               "if synchronization has been enabled "
                               "in the configuration file for 'lbrynet'."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_ch_subs_list(self, parent):
        self.textbox_ch_subs_list = \
            blocks.setup_textbox(parent,
                                 font=self.txt_lst_font)


class ListPubChsPage:
    """Mixin class to provide the created channels page."""
    def setup_page_pub_chs(self, parent):
        self.setup_top_p_chs(parent)
        self.setup_textbox_p_chs(parent)

    def setup_top_p_chs(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_cl_ch(frame, start=0)
        self.setup_grid_check_chs(frame, start=1)

    def setup_grid_top_cl_ch(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="List created channels",
                                b_command=self.list_pub_chs,
                                l_text=("In the default wallet"),
                                start=start)

    def setup_grid_check_chs(self, parent, start=0):
        blocks.setup_check_chs_claims(parent,
                                      spent_var=self.chck_ch_spent,
                                      update_var=self.chck_ch_upd,
                                      cid_var=self.chck_ch_cid,
                                      addr_var=self.chck_ch_addr,
                                      acc_var=self.chck_ch_acc,
                                      amount_var=self.chck_ch_amount,
                                      reverse_var=self.chck_pub_rev,
                                      start=start)

    def setup_textbox_p_chs(self, parent):
        self.textbox_p_chs = blocks.setup_textbox(parent,
                                                  font=self.txt_lst_font)
