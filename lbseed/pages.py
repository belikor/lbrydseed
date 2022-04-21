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
from lbseed.pages_base import SettingsPage, StatusPage
from lbseed.pages_down import DownloadChPage, DownloadSinglePage
from lbseed.pages_lists import (ListDownPage, ListDownInvalidPage,
                                ListChClaimsPage, SubscribedChsPage)
from lbseed.pages_peers import (ListChPeersPage, ListChsPeersPage,
                                ListSubsPeersPage)
from lbseed.pages_del import DeleteSinglePage, DeleteChPage
from lbseed.pages_support import SupportListPage, SupportAddPage
from lbseed.pages_search import TrendPage, SearchPage
from lbseed.pages_adv import SeedPage, ControllingClaimsPage


class VarsWidgets:
    """Mixin class to provide variables for the widgets."""
    def setup_widget_vars(self):
        self.e_font = tk.font.Font(family="monospace", size=10)
        self.b_width = 26
        self.txt_font = tk.font.Font(family="monospace")
        self.txt_lst_font = tk.font.Font(family="monospace", size=9)


class VarsSettings:
    """Mixin class to provide variables for the settings page."""
    def setup_settings_vars(self):
        self.server_var = tk.StringVar(value="http://localhost:5279")


class VarsDownload:
    """Mixin class to provide variables for the download page."""
    def setup_download_vars(self):
        server = res.get_download_dir(server=self.server_var.get())
        self.entry_d_dir = tk.StringVar(value=server)
        self.check_d_own_dir = tk.BooleanVar(value=True)
        self.check_d_save = tk.BooleanVar(value=True)
        self.check_d_repost = tk.BooleanVar(value=True)


class VarsListDownload:
    """Mixin class to provide variables for the list downlading pages."""
    def setup_list_d_vars(self):
        self.entry_chan = tk.StringVar()
        self.check_lst_blks = tk.BooleanVar(value=False)
        self.check_lst_cid = tk.BooleanVar(value=False)
        self.check_lst_blobs = tk.BooleanVar(value=True)
        self.check_lst_size = tk.BooleanVar(value=True)
        self.check_lst_show_ch = tk.BooleanVar(value=True)
        self.rad_lst_name = tk.StringVar(value="name")
        self.check_lst_reverse = tk.BooleanVar(value=True)

        self.label_lst_info = tk.StringVar()
        self.label_lst_info.set("Claims: 0; "
                                "total size: 0 GB; "
                                "total duration: 0 h")
        self.label_lst_inv_info = tk.StringVar()
        self.label_lst_inv_info.set("Claims: 0; "
                                    "total size: 0 GB; "
                                    "total duration: 0 h")


class VarsListChClaims:
    """Mixin class to provide variables for the list channel claims page."""
    def setup_list_ch_vars(self):
        self.entry_chl_chan = tk.StringVar(value="@lbry:3f")
        self.spin_chl_num = tk.IntVar(value=0)
        self.chck_chl_blk = tk.BooleanVar(value=False)
        self.chck_chl_cid = tk.BooleanVar(value=False)
        self.chck_chl_type = tk.BooleanVar(value=True)
        self.chck_chl_chname = tk.BooleanVar(value=False)
        self.chck_chl_title = tk.BooleanVar(value=False)
        self.chck_chl_reverse = tk.BooleanVar(value=True)
        self.chck_chl_reverse.set(True)
        self.label_chl_info = tk.StringVar()
        self.label_chl_info.set("Claims: 0; "
                                "total size: 0 GB; "
                                "total duration: 0 h")


class VarsSubscribedChs:
    """Mixin class to provide variables for the subscribed channels page."""
    def setup_subscribed_chs_vars(self):
        self.spin_subs_claim_num = tk.IntVar(value=5)
        self.rad_subs_shared = tk.StringVar(value="shared")
        self.rad_subs_show = tk.StringVar(value="show_valid")
        self.check_subs_claim_id = tk.BooleanVar(value=False)
        self.check_subs_title = tk.BooleanVar(value=True)
        self.spin_subs_threads = tk.IntVar(value=32)


class VarsPeers:
    """Mixin class to provide variables for the peer pages."""
    def setup_peers_vars(self):
        # self.entry_chl_chan = tk.StringVar(value="@lbry:3f")
        self.spin_ch_peers_num = tk.IntVar(value=50)
        self.spin_ch_peers_threads = tk.IntVar(value=32)
        self.chck_ch_peers_cid = tk.BooleanVar(value=False)
        self.chck_ch_peers_type = tk.BooleanVar(value=True)
        self.chck_ch_peers_title = tk.BooleanVar(value=False)

        self.spin_chs_ch_threads = tk.IntVar(value=16)
        self.spin_chs_cl_threads = tk.IntVar(value=32)

        self.spin_subs_ch_threads = tk.IntVar(value=32)
        self.spin_subs_cl_threads = tk.IntVar(value=16)
        self.rad_subs_pr_shared = tk.StringVar(value="shared")
        self.rad_subs_pr_show = tk.StringVar(value="show_all")


class VarsDelete:
    """Mixin class to provide variables for the deleting pages."""
    def setup_delete_vars(self):
        self.rad_delete_what = tk.StringVar(value="media")


class VarsSupports:
    """Mixin class to provide variables for the support pages."""
    def setup_support_vars(self):
        self.check_s_ch = tk.BooleanVar(value=False)
        self.check_s_claims = tk.BooleanVar(value=True)
        self.check_s_cid = tk.BooleanVar(value=False)
        self.check_s_combine = tk.BooleanVar(value=True)
        self.check_s_invalid = tk.BooleanVar(value=False)

        self.rad_s_support = tk.StringVar(value="create")
        self.check_s_supp_inv = tk.BooleanVar(value=False)


class Variables(VarsWidgets,
                VarsSettings,
                VarsDownload,
                VarsListDownload,
                VarsListChClaims,
                VarsSubscribedChs,
                VarsPeers,
                VarsDelete,
                VarsSupports):
    """Mixin class to provide variables to the application."""
    def setup_vars(self):
        super().setup_widget_vars()
        super().setup_settings_vars()
        super().setup_download_vars()
        super().setup_list_d_vars()
        super().setup_list_ch_vars()
        super().setup_subscribed_chs_vars()
        super().setup_peers_vars()
        super().setup_delete_vars()
        super().setup_support_vars()

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


# Use the classes to prevent warnings by code checkers (flake8)
True if SettingsPage else False
True if StatusPage else False

True if DownloadChPage else False
True if DownloadSinglePage else False

True if ListDownPage else False
True if ListDownInvalidPage else False
True if ListChClaimsPage else False
True if SubscribedChsPage else False

True if ListChPeersPage else False
True if ListChsPeersPage else False
True if ListSubsPeersPage else False

True if DeleteSinglePage else False
True if DeleteChPage else False

True if SupportListPage else False
True if SupportAddPage else False

True if TrendPage else False
True if SearchPage else False

True if SeedPage else False
True if ControllingClaimsPage else False
