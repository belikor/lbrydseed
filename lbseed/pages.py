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

import lbseed.resolve as res
from .pages_base import (ConfigPage,
                         ListChPeersPage, ListChsPeersPage,
                         ListSubsPeersPage,
                         DeleteSinglePage, DeleteChPage,
                         SupportListPage, SupportAddPage)
from .pages_down import DownloadChPage, DownloadSinglePage
from .pages_lists import (ListPage, ListInvalidPage, ListChPage,
                          ListChSubsPage)
from .pages_adv import (SeedPage, ControllingClaimsPage,
                        TrendPage, SearchPage)


class Variables:
    """Mixin class to provide variables to the application."""
    def setup_vars(self):
        self.e_font = tk.font.Font(family="monospace", size=10)
        self.b_width = 26
        self.txt_font = tk.font.Font(family="monospace")
        self.txt_lst_font = tk.font.Font(family="monospace", size=9)

        self.server_var = tk.StringVar()
        self.server_var.set("http://localhost:5279")

        self.entry_d_dir = tk.StringVar()
        server = res.get_download_dir(server=self.server_var.get())
        self.entry_d_dir.set(server)
        self.check_d_repost = tk.BooleanVar()
        self.check_d_repost.set(True)
        self.check_d_own_dir = tk.BooleanVar()
        self.check_d_own_dir.set(True)
        self.check_d_save = tk.BooleanVar()
        self.check_d_save.set(True)

        self.entry_chan = tk.StringVar()

        self.del_what_var = tk.StringVar()
        self.del_what_var.set("media")

        self.check_lst_blks = tk.BooleanVar()
        self.check_lst_blks.set(False)
        self.check_lst_cid = tk.BooleanVar()
        self.check_lst_cid.set(False)
        self.check_lst_blobs = tk.BooleanVar()
        self.check_lst_blobs.set(True)
        self.check_lst_size = tk.BooleanVar()
        self.check_lst_size.set(True)
        self.check_lst_show_ch = tk.BooleanVar()
        self.check_lst_show_ch.set(True)
        self.rad_lst_name = tk.StringVar()
        self.rad_lst_name.set("name")
        self.check_lst_reverse = tk.BooleanVar()
        self.check_lst_reverse.set(True)
        self.label_lst_info = tk.StringVar()
        self.label_lst_info.set("Claims: 0; "
                                "total size: 0 GB; "
                                "total duration: 0 h")
        self.label_lst_inv_info = tk.StringVar()
        self.label_lst_inv_info.set("Claims: 0; "
                                    "total size: 0 GB; "
                                    "total duration: 0 h")

        self.rad_subs_shared = tk.StringVar()
        self.rad_subs_shared.set("shared")
        self.rad_subs_show = tk.StringVar()
        self.rad_subs_show.set("show_valid")
        self.spin_subs_threads = tk.IntVar()
        self.spin_subs_threads.set(32)
        self.spin_subs_claim_num = tk.IntVar()
        self.spin_subs_claim_num.set(5)
        self.check_subs_claim_id = tk.BooleanVar()
        self.check_subs_claim_id.set(False)
        self.check_subs_title = tk.BooleanVar()
        self.check_subs_title.set(True)

        self.spin_ch_peers_num = tk.IntVar()
        self.spin_ch_peers_num.set(50)
        self.chck_ch_peers_cid = tk.BooleanVar()
        self.chck_ch_peers_cid.set(False)
        self.chck_ch_peers_type = tk.BooleanVar()
        self.chck_ch_peers_type.set(True)
        self.chck_ch_peers_title = tk.BooleanVar()
        self.chck_ch_peers_title.set(False)

        self.spin_ch_threads = tk.IntVar()
        self.spin_ch_threads.set(16)
        self.spin_claim_threads = tk.IntVar()
        self.spin_claim_threads.set(32)

        self.spin_ch_subs_threads = tk.IntVar()
        self.spin_ch_subs_threads.set(32)
        self.spin_c_subs_threads = tk.IntVar()
        self.spin_c_subs_threads.set(16)
        self.rad_subs_pr_shared = tk.StringVar()
        self.rad_subs_pr_shared.set("shared")
        self.rad_subs_pr_show = tk.StringVar()
        self.rad_subs_pr_show.set("show_all")

        self.check_s_ch = tk.BooleanVar()
        self.check_s_ch.set(False)
        self.check_s_claims = tk.BooleanVar()
        self.check_s_claims.set(True)
        self.check_s_cid = tk.BooleanVar()
        self.check_s_cid.set(False)
        self.check_s_combine = tk.BooleanVar()
        self.check_s_combine.set(True)
        self.check_s_invalid = tk.BooleanVar()
        self.check_s_invalid.set(False)

        self.rad_s_support = tk.StringVar()
        self.rad_s_support.set("create")
        self.check_s_supp_inv = tk.BooleanVar()
        self.check_s_supp_inv.set(False)

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

        self.spin_page = tk.IntVar()
        self.spin_page.set(1)
        self.chck_tr_claim_t = tk.StringVar()
        self.chck_tr_claim_t.set("stream")

        self.chck_tr_cid = tk.BooleanVar()
        self.chck_tr_cid.set(False)
        self.chck_tr_all = tk.BooleanVar()
        self.chck_tr_all.set(False)
        self.chck_tr_vid = tk.BooleanVar()
        self.chck_tr_vid.set(True)
        self.chck_tr_audio = tk.BooleanVar()
        self.chck_tr_audio.set(False)
        self.chck_tr_doc = tk.BooleanVar()
        self.chck_tr_doc.set(True)
        self.chck_tr_img = tk.BooleanVar()
        self.chck_tr_img.set(False)
        self.chck_tr_bin = tk.BooleanVar()
        self.chck_tr_bin.set(False)
        self.chck_tr_model = tk.BooleanVar()
        self.chck_tr_model.set(False)
        self.label_tr_info = tk.StringVar()
        self.label_tr_info.set("Page: -")

        self.search_entry = tk.StringVar()
        self.search_entry.set("text to search")
        self.search_entry_tags = tk.StringVar()
        self.label_sch_info = tk.StringVar()
        self.label_sch_info.set("Page: -")

        self.entry_chl_chan = tk.StringVar()
        self.entry_chl_chan.set("@lbry:3f")
        self.spin_chl_num = tk.IntVar()
        self.spin_chl_num.set(0)
        self.chck_chl_blk = tk.BooleanVar()
        self.chck_chl_blk.set(False)
        self.chck_chl_cid = tk.BooleanVar()
        self.chck_chl_cid.set(False)
        self.chck_chl_type = tk.BooleanVar()
        self.chck_chl_type.set(False)
        self.chck_chl_chname = tk.BooleanVar()
        self.chck_chl_chname.set(False)
        self.chck_chl_title = tk.BooleanVar()
        self.chck_chl_title.set(False)
        self.chck_chl_reverse = tk.BooleanVar()
        self.chck_chl_reverse.set(True)
        self.label_chl_info = tk.StringVar()
        self.label_chl_info.set("Claims: 0; "
                                "total size: 0 GB; "
                                "total duration: 0 h")


# Use the classes to prevent warnings by code checkers (flake8)
True if ConfigPage else False
True if ListChPeersPage else False
True if ListChsPeersPage else False
True if ListSubsPeersPage else False
True if DeleteSinglePage else False
True if DeleteChPage else False
True if SupportListPage else False
True if SupportAddPage else False

True if DownloadChPage else False
True if DownloadSinglePage else False

True if ListPage else False
True if ListInvalidPage else False
True if ListChPage else False
True if ListChSubsPage else False

True if SeedPage else False
True if ControllingClaimsPage else False
True if TrendPage else False
True if SearchPage else False
