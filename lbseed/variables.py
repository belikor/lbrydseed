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
"""Mixin classes that add the variables to the main graphical interface.

These classes should not be instantiated directly. They are just used
in a multiple inheritance, or mixin pattern, to provide the necessary
variables that will be used in the main interface by different
graphical elements like entry fields, checkboxes, radiobuttons, etc.

::
    class Application(ttk.Frame, Variables):
    def __init__(self, root):
        self.setup_vars()
"""
import tkinter as tk

import lbseed.resolve as res


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
        self.spin_lst_threads = tk.IntVar(value=32)


class VarsListChClaims:
    """Mixin class to provide variables for the list channel claims page."""
    def setup_list_ch_vars(self):
        self.entry_chl_chan = tk.StringVar(value="@lbry:3f")
        self.spin_chl_num = tk.IntVar(value=0)
        self.chck_chl_create = tk.BooleanVar(value=False)
        self.chck_chl_height = tk.BooleanVar(value=False)
        self.chck_chl_rels = tk.BooleanVar(value=True)
        self.chck_chl_cid = tk.BooleanVar(value=False)
        self.chck_chl_type = tk.BooleanVar(value=True)
        self.chck_chl_chname = tk.BooleanVar(value=False)
        self.chck_chl_sizes = tk.BooleanVar(value=True)
        self.chck_chl_fees = tk.BooleanVar(value=True)
        self.chck_chl_title = tk.BooleanVar(value=False)
        self.chck_chl_reverse = tk.BooleanVar(value=True)


class VarsSubscribedChs:
    """Mixin class to provide variables for the subscribed channels page."""
    def setup_subscribed_chs_vars(self):
        self.spin_subs_claim_num = tk.IntVar(value=5)
        self.rad_subs_shared = tk.StringVar(value="shared")
        self.rad_subs_show = tk.StringVar(value="show_valid")
        self.check_subs_claim_id = tk.BooleanVar(value=False)
        self.check_subs_title = tk.BooleanVar(value=True)
        self.spin_subs_threads = tk.IntVar(value=32)


class VarsPublished:
    """Mixin class to provide variables to the published claims."""
    def setup_published_vars(self):
        self.chck_ch_spent = tk.BooleanVar(value=False)
        self.chck_ch_upd = tk.BooleanVar(value=False)
        self.chck_ch_cid = tk.BooleanVar(value=False)
        self.chck_ch_addr = tk.BooleanVar(value=False)
        self.chck_ch_acc = tk.BooleanVar(value=False)
        self.chck_ch_amount = tk.BooleanVar(value=True)
        self.chck_pub_rev = tk.BooleanVar(value=True)

        self.chck_pub_ch = tk.StringVar(value=None)
        self.chck_pub_types = tk.BooleanVar(value=True)
        self.chck_pub_title = tk.BooleanVar(value=False)


class VarsControlling:
    """Mixin class to provide variables for the controlling claims page."""
    def setup_controlling_vars(self):
        self.check_c_contr = tk.BooleanVar(value=False)
        self.check_c_non_contr = tk.BooleanVar(value=True)
        self.check_c_skip_repost = tk.BooleanVar(value=False)
        self.check_c_ch_only = tk.BooleanVar(value=False)
        self.check_c_compact = tk.BooleanVar(value=True)
        self.check_c_cid = tk.BooleanVar(value=False)
        self.check_c_is_repost = tk.BooleanVar(value=True)
        self.check_c_compete = tk.BooleanVar(value=True)
        self.check_c_reposts = tk.BooleanVar(value=True)


class VarsComments:
    """Mixin class to provide variables for the seeding page."""
    def setup_comments_vars(self):
        srv = "https://comments.odysee.com/api/v2"
        self.cmnt_server_def = tk.StringVar(value=srv)
        self.cmnt_server = tk.StringVar(value=srv)
        self.comment_claim = None
        self.comments = []
        self.cmnt_list = tk.StringVar()
        self.cmnt_index = tk.IntVar(value=0)
        self.comment_id = None

        author = "(None)"
        self.last_cmnt_author = tk.StringVar(value=author)
        self.cmb_rep_author = tk.StringVar(value=author)
        self.rad_rep_opt = tk.StringVar(value="create")
        self.rad_rep_curr = tk.StringVar(value="reply")
        self.last_rad_rep_opt = tk.StringVar(value="create")
        self.last_cmnt = tk.StringVar()
        self.lab_rep_status = tk.StringVar(value="Status: no claim lodaded")


class VarsPeers:
    """Mixin class to provide variables for the peer pages."""
    def setup_peers_vars(self):
        self.spin_cls_peers_threads = tk.IntVar(value=32)
        self.chck_cls_peers_cid = tk.BooleanVar(value=False)
        self.chck_cls_peers_type = tk.BooleanVar(value=True)
        self.chck_cls_peers_title = tk.BooleanVar(value=False)
        self.chck_peers_pars = tk.BooleanVar(value=False)

        # self.entry_chl_chan = tk.StringVar(value="@lbry:3f")
        self.spin_ch_peers_num = tk.IntVar(value=50)

        self.spin_chs_ch_threads = tk.IntVar(value=16)
        self.spin_chs_cl_threads = tk.IntVar(value=32)

        self.spin_subs_ch_threads = tk.IntVar(value=32)
        self.spin_subs_cl_threads = tk.IntVar(value=16)
        self.rad_subs_pr_shared = tk.StringVar(value="shared")
        self.rad_subs_pr_show = tk.StringVar(value="show_all")


class VarsSeeding:
    """Mixin class to provide variables for the seeding page."""
    def setup_seeding_vars(self):
        self.check_seed_plot = tk.BooleanVar(value=False)


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
        self.spin_s_threads = tk.IntVar(value=32)

        self.rad_s_support = tk.StringVar(value="create")
        self.check_s_supp_inv = tk.BooleanVar(value=False)


class VarsSearching:
    """Mixin class to provide variables for the trending pages."""
    def setup_searching_vars(self):
        self.spin_page = tk.IntVar(value=0)
        self.spin_tr_threads = tk.IntVar(value=32)
        self.rad_tr_claim = tk.StringVar(value="stream")

        self.chck_tr_all = tk.BooleanVar(value=False)
        self.chck_tr_vid = tk.BooleanVar(value=True)
        self.chck_tr_audio = tk.BooleanVar(value=False)
        self.chck_tr_doc = tk.BooleanVar(value=True)
        self.chck_tr_img = tk.BooleanVar(value=False)
        self.chck_tr_bin = tk.BooleanVar(value=False)
        self.chck_tr_model = tk.BooleanVar(value=False)

        self.chck_tr_create = tk.BooleanVar(value=False)
        self.chck_tr_height = tk.BooleanVar(value=False)
        self.chck_tr_release = tk.BooleanVar(value=True)
        self.chck_tr_cid = tk.BooleanVar(value=False)
        self.chck_tr_typ = tk.BooleanVar(value=True)
        self.chck_tr_chname = tk.BooleanVar(value=True)
        self.chck_tr_sizes = tk.BooleanVar(value=True)
        self.chck_tr_fees = tk.BooleanVar(value=True)
        self.chck_tr_title = tk.BooleanVar(value=False)

        self.search_entry = tk.StringVar(value="text to search")
        self.search_entry_tags = tk.StringVar()


class Variables(VarsWidgets,
                VarsSettings,
                VarsDownload,
                VarsListDownload,
                VarsListChClaims,
                VarsSubscribedChs,
                VarsPublished,
                VarsControlling,
                VarsComments,
                VarsPeers,
                VarsSeeding,
                VarsDelete,
                VarsSupports,
                VarsSearching):
    """Mixin class to provide variables to the application."""
    def setup_vars(self):
        super().setup_widget_vars()
        super().setup_settings_vars()
        super().setup_download_vars()
        super().setup_list_d_vars()
        super().setup_list_ch_vars()
        super().setup_subscribed_chs_vars()
        super().setup_published_vars()
        super().setup_controlling_vars()
        super().setup_comments_vars()
        super().setup_peers_vars()
        super().setup_seeding_vars()
        super().setup_delete_vars()
        super().setup_support_vars()
        super().setup_searching_vars()
