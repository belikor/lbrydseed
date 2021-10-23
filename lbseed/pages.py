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
import lbseed.resolve as res


class Variables:
    """Mixin class to provide variables to the application."""
    def setup_vars(self):
        self.e_font = tk.font.Font(family="monospace", size=10)
        self.b_width = 26
        self.txt_font = tk.font.Font(family="monospace")
        self.txt_lst_font = tk.font.Font(family="monospace", size=9)

        self.server_var = tk.StringVar()
        self.server_var.set("http://localhost:5279")
        self.down_dir_var = tk.StringVar()
        server = res.get_download_dir(server=self.server_var.get())
        self.down_dir_var.set(server)
        self.own_dir_var = tk.BooleanVar()
        self.own_dir_var.set(True)
        self.save_var = tk.BooleanVar()
        self.save_var.set(True)

        self.entry_chan = tk.StringVar()

        self.del_what_var = tk.StringVar()
        self.del_what_var.set("media")

        self.check_cid = tk.BooleanVar()
        self.check_cid.set(False)
        self.check_blobs = tk.BooleanVar()
        self.check_blobs.set(True)
        self.check_show_ch = tk.BooleanVar()
        self.check_show_ch.set(True)
        self.check_name = tk.BooleanVar()
        self.check_name.set(True)

        self.check_s_ch = tk.BooleanVar()
        self.check_s_ch.set(False)
        self.check_s_claims = tk.BooleanVar()
        self.check_s_claims.set(True)
        self.check_s_cid = tk.BooleanVar()
        self.check_s_cid.set(False)
        self.check_s_combine = tk.BooleanVar()
        self.check_s_combine.set(True)

        self.check_seed_plot = tk.BooleanVar()
        self.check_seed_plot.set(False)

        self.check_c_contr = tk.BooleanVar()
        self.check_c_contr.set(False)
        self.check_c_non_contr = tk.BooleanVar()
        self.check_c_non_contr.set(True)
        self.check_c_skip_repost = tk.BooleanVar()
        self.check_c_skip_repost.set(False)
        self.check_c_ch_only = tk.BooleanVar()
        self.check_c_ch_only.set(False)
        self.check_c_cid = tk.BooleanVar()
        self.check_c_cid.set(False)
        self.check_c_is_repost = tk.BooleanVar()
        self.check_c_is_repost.set(True)
        self.check_c_competing = tk.BooleanVar()
        self.check_c_competing.set(True)
        self.check_c_reposts = tk.BooleanVar()
        self.check_c_reposts.set(True)
        self.check_c_compact = tk.BooleanVar()
        self.check_c_compact.set(True)


class ConfigPage:
    """Mixin class to provide the configuration page to the application."""
    def setup_page_cfg(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_top_config(frame, start=0)

    def setup_top_config(self, parent, start=0):
        entry = ttk.Entry(parent,
                          textvariable=self.server_var,
                          font=self.e_font,
                          width=self.b_width)
        entry.grid(row=start, column=0, sticky=tk.W + tk.E)
        le = ttk.Label(parent,
                       text=("Address of the 'lbrynet' daemon. "
                             "It defaults to localhost:5279"))
        le.grid(row=start, column=1, sticky=tk.W, padx=2)


class DownloadChPage:
    """Mixin class to provide the download channel page to the application."""
    def setup_page_dch(self, parent):
        self.setup_top_dch(parent)
        self.setup_textbox_dch(parent)

    def setup_top_dch(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_dch(frame, start=0)
        self.setup_grid_button_dch(frame, start=1)
        self.setup_grid_check_dch(frame, start=4)
        self.setup_info_dch(frame, start=6)

    def setup_grid_top_dch(self, parent, start=0):
        blocks.setup_download_entry(parent,
                                    dir_var=self.down_dir_var,
                                    font=self.e_font,
                                    start=start)

    def setup_grid_button_dch(self, parent, start=0):
        blocks.setup_buttons_val_res(parent,
                                     width=self.b_width,
                                     validate_func=self.validate_ch,
                                     resolve_func=self.resolve_ch,
                                     start=start)

        b_download = ttk.Button(parent, text="Download claims",
                                width=self.b_width,
                                command=self.download_ch)
        b_download.grid(row=start+2, column=0)
        b_download.bind("<<Activate>>",
                        blocks.f_with_event(self.download_ch))

        lr = ttk.Label(parent,
                       text=("Start downloading the newest claims "
                             "from the channels"))
        lr.grid(row=start+2, column=1, sticky=tk.W, padx=2)

    def setup_grid_check_dch(self, parent, start=0):
        blocks.setup_download_check(parent,
                                    own_dir_var=self.own_dir_var,
                                    save_var=self.save_var,
                                    start=start)

    def setup_info_dch(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Add a channel, a comma, "
                               "and the number of items to download "
                               "from this channel."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_dch(self, parent):
        channels = blocks.set_up_default_channels()
        self.textbox_dch = blocks.setup_textbox(parent, font=self.txt_font)
        self.textbox_dch.insert("1.0", channels)


class DownloadSinglePage:
    """Mixin class to provide the download single page to the application."""
    def setup_page_d(self, parent):
        self.setup_top_d(parent)
        self.setup_textbox_d(parent)

    def setup_top_d(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_d(frame, start=0)
        self.setup_grid_button_d(frame, start=1)
        self.setup_grid_check_d(frame, start=3)
        self.setup_info_d(frame, start=5)

    def setup_grid_top_d(self, parent, start=0):
        blocks.setup_download_entry(parent,
                                    dir_var=self.down_dir_var,
                                    font=self.e_font,
                                    start=start)

    def setup_grid_button_d(self, parent, start=0):
        blocks.setup_button_resolve_claims(parent,
                                           width=self.b_width,
                                           resolve_func=self.resolve_claims,
                                           start=start)

        b_download = ttk.Button(parent, text="Download claims",
                                width=self.b_width,
                                command=self.download_claims)
        b_download.grid(row=start+1, column=0)
        b_download.bind("<<Activate>>",
                        blocks.f_with_event(self.download_claims))

        l2 = ttk.Label(parent,
                       text="Start downloading the claims")
        l2.grid(row=start+1, column=1, sticky=tk.W, padx=2)

    def setup_grid_check_d(self, parent, start=0):
        blocks.setup_download_check(parent,
                                    own_dir_var=self.own_dir_var,
                                    save_var=self.save_var,
                                    start=start)

    def setup_info_d(self, parent, start=0):
        blocks.info_claims(parent, start=start)

    def setup_textbox_d(self, parent):
        claims = blocks.set_up_default_claims()
        self.textbox_d = blocks.setup_textbox(parent, font=self.txt_font)
        self.textbox_d.insert("1.0", claims)


class ListPage:
    """Mixin class to provide the list page to the application."""
    def setup_page_list(self, parent):
        self.setup_top_list(parent)
        self.setup_textbox_list(parent)

    def setup_top_list(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_list(frame, start=0)
        self.setup_grid_check_list(frame, start=2)

    def setup_grid_top_list(self, parent, start=0):
        b_list = ttk.Button(parent, text="List claims",
                            width=self.b_width,
                            command=self.list_claims)
        b_list.grid(row=start, column=0)
        b_list.bind("<<Activate>>",
                    blocks.f_with_event(self.list_claims))

        llist = ttk.Label(parent,
                          text="List all locally downloaded claims")
        llist.grid(row=start, column=1, sticky=tk.W, padx=2)

        entry = ttk.Entry(parent,
                          textvariable=self.entry_chan,
                          font=self.e_font)
        entry.grid(row=start+1, column=0, sticky=tk.W + tk.E)
        entry.bind("<<Activate>>",
                   blocks.f_with_event(self.list_claims))

        le = ttk.Label(parent,
                       text="Filter by channel name")
        le.grid(row=start+1, column=1, sticky=tk.W, padx=2)

    def setup_grid_check_list(self, parent, start=0):
        blocks.setup_check_list(parent,
                                cid_var=self.check_cid,
                                blobs_var=self.check_blobs,
                                show_ch_var=self.check_show_ch,
                                name_var=self.check_name,
                                start=start)

    def setup_textbox_list(self, parent):
        self.textbox_list = blocks.setup_textbox(parent,
                                                 font=self.txt_lst_font)


class DeletePage:
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
        blocks.setup_button_resolve_claims(parent,
                                           width=self.b_width,
                                           resolve_func=self.resolve_claims,
                                           start=start)

        b_del = ttk.Button(parent, text="Delete claims",
                           width=self.b_width,
                           command=self.delete_claims)
        b_del.grid(row=start+1, column=0)
        b_del.bind("<<Activate>>",
                   blocks.f_with_event(self.delete_claims))

        ldel = ttk.Label(parent,
                         text="Delete locally downloaded claims")
        ldel.grid(row=start+1, column=1, sticky=tk.W, padx=2)

    def setup_grid_radio_del(self, parent, start=0):
        blocks.setup_delete_radio(parent,
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
        blocks.setup_buttons_val_res(parent,
                                     width=self.b_width,
                                     validate_func=self.validate_ch,
                                     resolve_func=self.resolve_ch,
                                     start=start)

        b_clean = ttk.Button(parent, text="Clean up claims",
                             width=self.b_width,
                             command=self.delete_ch)
        b_clean.grid(row=start+2, column=0)
        b_clean.bind("<<Activate>>",
                     blocks.f_with_event(self.delete_ch))

        lb = ttk.Label(parent,
                       text=("Start deleting claims "
                             "from the oldest to the newest"))
        lb.grid(row=start+2, column=1, sticky=tk.W, padx=2)

    def setup_grid_radio_delch(self, parent, start=0):
        blocks.setup_delete_radio(parent,
                                  del_what_var=self.del_what_var,
                                  start=start)

    def setup_info_delch(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Add a channel, a comma, "
                               "and the number of items to keep "
                               "from this channel.\n"
                               "The N newest claims (by publication date) "
                               "will remain while older items "
                               "will be removed."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_delch(self, parent):
        channels = blocks.set_up_default_channels(clean_up=True)
        self.textbox_delch = blocks.setup_textbox(parent, font=self.txt_font)
        self.textbox_delch.insert("1.0", channels)


class SupportPage:
    """Mixin class to provide the support page to the application."""
    def setup_page_supports(self, parent):
        self.setup_top_support(parent)
        self.setup_textbox_support(parent)

    def setup_top_support(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_button_support(frame, start=0)
        self.setup_grid_check_support(frame, start=1)
        self.setup_info_support(frame, start=5)

    def setup_grid_button_support(self, parent, start=0):
        b_clean = ttk.Button(parent, text="List supports",
                             width=self.b_width,
                             command=self.list_supports)
        b_clean.grid(row=start, column=0)
        b_clean.bind("<<Activate>>",
                     blocks.f_with_event(self.list_supports))

        lb = ttk.Label(parent,
                       text=("List claims supported with LBC"))
        lb.grid(row=start, column=1, sticky=tk.W, padx=2)

    def setup_grid_check_support(self, parent, start=0):
        blocks.setup_check_support(parent,
                                   show_ch_var=self.check_s_ch,
                                   show_claims_var=self.check_s_claims,
                                   show_cid_var=self.check_s_cid,
                                   combine_var=self.check_s_combine,
                                   start=start)

    def setup_info_support(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("List the claim, "
                               "the amount of our LBC support, "
                               "the total amount of support, "
                               "and its trending score."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_support(self, parent):
        self.textbox_supports = blocks.setup_textbox(parent,
                                                     font=self.txt_lst_font)


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
        b_seed = ttk.Button(parent, text="Display seeding ratio",
                            width=self.b_width,
                            command=self.seeding_ratio)
        b_seed.grid(row=start, column=0)
        b_seed.bind("<<Activate>>",
                    blocks.f_with_event(self.seeding_ratio))

        lb = ttk.Label(parent,
                       text=("This is an estimation of uploaded and "
                             "downloaded blobs\n"
                             "based on information found in the log files."))
        lb.grid(row=start, column=1, sticky=tk.W, padx=2)

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
        self.setup_info_contr(frame, start=10)

    def setup_grid_button_contr(self, parent, start=0):
        b_cont = ttk.Button(parent, text="Display controlling claims",
                            width=self.b_width,
                            command=self.controlling_claims)
        b_cont.grid(row=start, column=0)
        b_cont.bind("<<Activate>>",
                    blocks.f_with_event(self.controlling_claims))

        lb = ttk.Label(parent,
                       text=('Show our claims, and whether '
                             'we have the "controlling claim"\n'
                             '(claim with the highest bid when compared '
                             'to other claims of the same name)'))
        lb.grid(row=start, column=1, sticky=tk.W, padx=2)

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
