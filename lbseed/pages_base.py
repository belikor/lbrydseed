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


class ConfigPage:
    """Mixin class to provide the configuration page to the application."""
    def setup_page_cfg(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_top_config(frame, start=0)

    def setup_top_config(self, parent, start=0):
        entry, label = \
            blocks.setup_entry_gen(parent,
                                   font=self.e_font,
                                   text_var=self.server_var,
                                   l_text=("Address of the 'lbrynet' daemon. "
                                           "It defaults to localhost:5279"),
                                   start=start)
        entry["width"] = self.b_width


class DeleteSinglePage:
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
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Resolve online",
                                b_command=self.resolve_claims,
                                l_text="Confirm that the claims exist",
                                start=start)

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Delete claims",
                                b_command=self.delete_claims,
                                l_text="Delete locally downloaded claims",
                                start=start+1)

    def setup_grid_radio_del(self, parent, start=0):
        blocks.setup_radio_delete(parent,
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
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Validate input",
                                b_command=self.validate_ch,
                                l_text=("Verify that the input "
                                        "can be read correctly"),
                                start=start)

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Resolve online",
                                b_command=self.resolve_ch,
                                l_text="Confirm that the channels exist",
                                start=start+1)

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Clean up claims",
                                b_command=self.delete_ch,
                                l_text=("Start deleting claims "
                                        "from the oldest to the newest"),
                                start=start+2)

    def setup_grid_radio_delch(self, parent, start=0):
        blocks.setup_radio_delete(parent,
                                  del_what_var=self.del_what_var,
                                  start=start)

    def setup_info_delch(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Add a channel, a comma, "
                               "and the number of items to keep "
                               "from this channel.\n"
                               "The N newest claims (by publication date) "
                               "will remain while older items "
                               "will be removed.\n"
                               "If the number is 0, it will remove "
                               "all downloaded items from the channel."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_delch(self, parent):
        channels = blocks.set_up_default_channels(clean_up=True)
        self.textbox_delch = blocks.setup_textbox(parent, font=self.txt_font)
        self.textbox_delch.insert("1.0", channels)


class SupportListPage:
    """Mixin class to provide the support page to the application."""
    def setup_page_supports(self, parent):
        self.setup_top_support(parent)
        self.setup_textbox_support(parent)

    def setup_top_support(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_button_support(frame, start=0)
        self.setup_grid_check_support(frame, start=1)
        self.setup_info_support(frame, start=6)

    def setup_grid_button_support(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="List supports",
                                b_command=self.list_supports,
                                l_text="List claims supported with LBC",
                                start=start)

    def setup_grid_check_support(self, parent, start=0):
        blocks.setup_check_support(parent,
                                   show_ch_var=self.check_s_ch,
                                   show_claims_var=self.check_s_claims,
                                   show_cid_var=self.check_s_cid,
                                   show_invalid_var=self.check_s_invalid,
                                   combine_var=self.check_s_combine,
                                   start=start)

    def setup_info_support(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("List the claim, "
                               "the amount of our support, "
                               "the total amount of support, "
                               "and its trending score.\n"
                               "Supports will appear only after they "
                               "have been confirmed in the blockchain.\n"
                               "Claims that have become 'invalid' "
                               "(removed by their authors) will appear\n"
                               "surrounded by '[brackets]'. "
                               "It is best to remove the support completely "
                               "from these claims."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_support(self, parent):
        self.textbox_supports = blocks.setup_textbox(parent,
                                                     font=self.txt_lst_font)


class SupportAddPage:
    """Mixin class to provide methods to create supports."""
    def setup_page_add_supports(self, parent):
        self.setup_top_add_support(parent)
        self.setup_textbox_add_support(parent)

    def setup_top_add_support(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_button_add_sup(frame, start=0)
        self.setup_grid_radio_support(frame, start=3)
        self.setup_info_support_add(frame, start=7)

    def setup_grid_button_add_sup(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Validate input",
                                b_command=self.validate_g_claims,
                                l_text=("Verify that the input "
                                        "can be read correctly"),
                                start=start)

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Resolve online",
                                b_command=self.resolve_g_claims,
                                l_text="Confirm that the claims exist",
                                start=start+1)

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Add or remove support",
                                b_command=self.add_supports,
                                l_text=("Create a new support, "
                                        "add or remove support"),
                                start=start+2)

    def setup_grid_radio_support(self, parent, start=0):
        (self.r_s_create,
         self.r_s_abandon,
         self.r_s_target) = \
             blocks.setup_radio_support(parent,
                                        support_how_var=self.rad_s_support,
                                        support_inv_var=self.check_s_supp_inv,
                                        support_inv_cmd=self.test_support_inv,
                                        start=start)

    def test_support_inv(self):
        if self.check_s_supp_inv.get():
            self.rad_s_support.set("abandon_change")
            self.r_s_create["state"] = "disabled"
            self.r_s_abandon["state"] = "normal"
            self.r_s_target["state"] = "disabled"
        else:
            self.rad_s_support.set("create")
            self.r_s_create["state"] = "normal"
            self.r_s_abandon["state"] = "normal"
            self.r_s_target["state"] = "normal"

    def setup_info_support_add(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Each claim has a 'base' support "
                               "that is provided by the author, "
                               "and by other users.\n"
                               "We don't control this 'base' support, "
                               "we can only add to it.\n"
                               "total = base + ours\n"
                               "\n"
                               "Add a claim, a comma, "
                               "and then a number that represents "
                               "a support.\n"
                               "The minimum amount is 0.00000001; "
                               "all quantities are converted internally "
                               "to use 8 decimal digits.\n"
                               "Supports will appear only after they "
                               "have been confirmed in the blockchain."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_add_support(self, parent):
        claims = ["mass-psychosis-how-an-entire-population, 100",
                  "@lbry:3f, 50",
                  "@my-favorite-channel, 5.1234",
                  "abcd0000efgh0000ijkl0000mopq0000rstu0000, 3.33",
                  "livestream-tutorial:b, 10.00005678",
                  "8e16d91185aa4f1cd797f93d7714de2a22622759, 4.4405"]

        claims = "\n".join(claims)
        self.textbox_add_support = blocks.setup_textbox(parent)
        self.textbox_add_support.insert("1.0", claims)
