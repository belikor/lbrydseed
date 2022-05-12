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
"""Mixin classes that add peer pages to the main interface.

These classes should not be instantiatied directly. They are just used
in a multiple inheritance, or mixin pattern, to provide the necessary
building command to build the specific page in the main interface.

::
    class ListChPeersPage:
        def setup_page_ch_peers(self, parent):
            ...

    class Application(ttk.Frame, ListChPeersPage):
        def __init__(self, root):
            page_ch_peers = ttk.Frame(root)
            self.setup_page_ch_peers(page_ch_peers)
"""

import tkinter as tk
import tkinter.ttk as ttk

import lbseed.blocks as blocks


class ListChPeersPage:
    """Mixing class to provide the list of peers for a channel."""
    def setup_page_ch_peers(self, parent):
        self.setup_top_ch_peers(parent)
        self.setup_textbox_ch_peers(parent)

    def setup_top_ch_peers(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_ch_peers(frame, start=0)
        self.setup_grid_top_ch_peers_opt(frame, start=5)
        self.setup_info_ch_peers(frame, start=8)

    def setup_grid_top_ch_peers(self, parent, start=0):
        entry, label = \
            blocks.setup_entry_gen(parent,
                                   font=self.e_font,
                                   text_var=self.entry_chl_chan,
                                   l_text="Channel to inspect",
                                   start=start)
        entry.bind("<<Activate>>", blocks.f_with_event(self.list_ch_peers))

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Resolve online",
                                b_command=self.resolve_ch_list,
                                l_text="Confirm that the channel exists",
                                start=start+1)

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="List channel peers",
                                b_command=self.list_ch_peers,
                                l_text=("List peers for the claims "
                                        "from the specified channel, "
                                        "starting from the newest one,\n"
                                        "and going back in time"),
                                start=start+2)

        blocks.setup_spin_gen(parent,
                              frm=0, to=100E3, incr=1,
                              default=50,
                              s_text_var=self.spin_ch_peers_num,
                              s_command=self.list_ch_peers,
                              l_text=("Number of claims to display; "
                                      "use 0 to display all"),
                              start=start+3)

        blocks.setup_spin_gen(parent,
                              frm=0, to=256, incr=1,
                              default=32,
                              s_text_var=self.spin_ch_peers_threads,
                              s_command=self.list_ch_peers,
                              l_text=("Number of threads to process "
                                      "claims in parallel "
                                      "and find peers; "
                                      "use 0 to avoid threads"),
                              start=start+4)

    def setup_grid_top_ch_peers_opt(self, parent, start=0):
        chck_cid = ttk.Checkbutton(parent,
                                   variable=self.chck_ch_peers_cid,
                                   text="Show claim ID (40-character string)")
        chck_cid.grid(row=start, column=1, sticky=tk.W)

        chck_typ = ttk.Checkbutton(parent,
                                   variable=self.chck_ch_peers_type,
                                   text=("Show the type of claim, "
                                         "and media, if available"))
        chck_typ.grid(row=start+1, column=1, sticky=tk.W)

        chck_title = ttk.Checkbutton(parent,
                                     variable=self.chck_ch_peers_title,
                                     text=("Show the claim 'title' "
                                           "instead of the claim 'name'"))
        chck_title.grid(row=start+2, column=1, sticky=tk.W)

    def setup_info_ch_peers(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Only downloadable claims (streams) "
                               "can be shared in the network, "
                               "and are able to have peers.\n"
                               "Other types of claims "
                               "(reposts, playlists, livestreams, etc.) "
                               "will not count toward total number of peers\n"
                               "nor size nor duration.\n"
                               "When hosted is 'True' we have the first "
                               "or second blobs of the stream, "
                               "so we are one of the peers\n"
                               "hosting the file in the network. "
                               "When listing the unique peers, the + 1 "
                               "indicates that we are one\n"
                               "of those peers."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_ch_peers(self, parent):
        self.textbox_ch_peers = blocks.setup_textbox(parent,
                                                     font=self.txt_lst_font)


class ListChsPeersPage:
    """Mixing class to provide the list of peers for various channels."""
    def setup_page_chs_peers(self, parent):
        self.setup_top_chs_peers(parent)
        frame1 = ttk.Frame(parent)
        frame1.pack(padx=4, pady=4, fill="both", expand=False)
        frame2 = ttk.Frame(parent)
        frame2.pack(padx=4, pady=4, fill="both", expand=True)
        self.setup_textbox_chs_peers(frame1)
        self.setup_textbox_chs_peers_out(frame2)

    def setup_top_chs_peers(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_chs_peers(frame, start=0)
        self.setup_info_chs_peers(frame, start=5)

    def setup_grid_top_chs_peers(self, parent, start=0):
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
                                b_text="List channels peers",
                                b_command=self.list_chs_peers,
                                l_text=("List peers for the claims "
                                        "from the specified channels, "
                                        "starting from the newest claims,\n"
                                        "and going back in time"),
                                start=start+2)

        blocks.setup_spin_gen(parent,
                              frm=0, to=256, incr=1,
                              default=16,
                              s_text_var=self.spin_chs_ch_threads,
                              s_command=self.list_chs_peers,
                              l_text=("Number of threads to process "
                                      "channels in parallel; "
                                      "use 0 to avoid threads"),
                              start=start+3)

        blocks.setup_spin_gen(parent,
                              frm=0, to=256, incr=1,
                              default=32,
                              s_text_var=self.spin_chs_cl_threads,
                              s_command=self.list_chs_peers,
                              l_text=("Number of threads to process "
                                      "claims in parallel "
                                      "and find peers; "
                                      "use 0 to avoid threads"),
                              start=start+4)

    def setup_info_chs_peers(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Add a channel, a comma, "
                               "and the number of claims to get "
                               "peer information about.\n\n"
                               "Only downloadable claims (streams) "
                               "can be shared in the network, "
                               "and are able to have peers.\n"
                               "Other types of claims "
                               "(reposts, playlists, livestreams, etc.) "
                               "will not count toward total number of peers\n"
                               "nor size nor duration.\n"
                               "When listing the unique peers, the + 1 "
                               "indicates that we are one of those peers."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_chs_peers(self, parent):
        channels = blocks.set_up_default_channels()
        self.textbox_chs_peers = blocks.setup_textbox(parent,
                                                      height=10,
                                                      font=self.txt_font)
        self.textbox_chs_peers.insert("1.0", channels)

    def setup_textbox_chs_peers_out(self, parent):
        self.textbox_chs_peers_out = \
            blocks.setup_textbox(parent,
                                 font=self.txt_lst_font)
        self.textbox_chs_peers_out.insert("1.0", "(peer information)")


class ListSubsPeersPage:
    """Mixing class to provide the list of peers for a channel."""
    def setup_page_subs_peers(self, parent):
        self.setup_top_subs_peers(parent)
        self.setup_textbox_subs_peers(parent)

    def setup_top_subs_peers(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_subs_peers(frame, start=0)
        self.setup_grid_top_subs_peers_opt(frame, start=4)
        self.setup_info_subs_peers(frame, start=6)

    def setup_grid_top_subs_peers(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="List subscribed channels peers",
                                b_command=self.list_subs_peers,
                                l_text=("List peers for claims belonging to "
                                        "our subscribed channels,\n"
                                        "starting from the newest claims, "
                                        "and going back in time"),
                                start=start)

        blocks.setup_spin_gen(parent,
                              frm=0, to=100E3, incr=1,
                              default=50,
                              s_text_var=self.spin_ch_peers_num,
                              s_command=self.list_subs_peers,
                              l_text=("Number of claims to search "
                                      "for peers in each subscribed "
                                      "channel"),
                              start=start+1)

        blocks.setup_spin_gen(parent,
                              frm=0, to=256, incr=1,
                              default=32,
                              s_text_var=self.spin_subs_ch_threads,
                              s_command=self.list_subs_peers,
                              l_text=("Number of threads to process "
                                      "channels in parallel; "
                                      "use 0 to avoid threads"),
                              start=start+2)

        blocks.setup_spin_gen(parent,
                              frm=0, to=256, incr=1,
                              default=16,
                              s_text_var=self.spin_subs_cl_threads,
                              s_command=self.list_subs_peers,
                              l_text=("Number of threads to process "
                                      "claims in parallel "
                                      "and find peers; "
                                      "use 0 to avoid threads"),
                              start=start+3)

    def setup_grid_top_subs_peers_opt(self, parent, start=0):
        frame = ttk.Frame(parent, relief="groove", borderwidth=2)
        frame.grid(row=start, column=1, sticky=tk.W + tk.E + tk.N)

        blocks.setup_radio_ch_subs_shared(frame,
                                          shared_var=self.rad_subs_pr_shared,
                                          start=0)

        frame2 = ttk.Frame(parent, relief="groove", borderwidth=2)
        frame2.grid(row=start+1, column=1, sticky=tk.W + tk.E + tk.N)

        blocks.setup_radio_ch_subs_valid2(frame2,
                                          show_var=self.rad_subs_pr_show,
                                          start=0)

    def setup_info_subs_peers(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Only downloadable claims (streams) "
                               "can be shared in the network, "
                               "and are able to have peers.\n"
                               "Other types of claims "
                               "(reposts, playlists, livestreams, etc.) "
                               "will not count toward total number of peers\n"
                               "nor size nor duration.\n"
                               "When listing the unique peers, the + 1 "
                               "indicates that we are one of those peers.\n"
                               "Channels that have become 'invalid' "
                               "(removed from the network) "
                               "will appear surrounded by '[brackets]',\n"
                               "so we should remove them "
                               "from our subscriptions."))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_subs_peers(self, parent):
        self.textbox_subs_peers = blocks.setup_textbox(parent,
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
