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
"""Small application to download claims from LBRY channels."""
import platform
import sys
import tkinter as tk
import tkinter.font
import tkinter.ttk as ttk

import lbseed.pages as pages
import lbseed.variables as var
import lbseed.resolve as res
import lbseed.validate as val
import lbseed.actions as actions


class Application(ttk.Frame,
                  var.Variables,
                  pages.SettingsPage, pages.StatusPage,
                  pages.DownloadChPage, pages.DownloadSinglePage,
                  pages.ListDownPage, pages.ListDownInvalidPage,
                  pages.ListChClaimsPage, pages.SubscribedChsPage,
                  pages.ListPubChsPage, pages.ListPubClaimsPage,
                  pages.ControllingClaimsPage,
                  pages.ListChPeersPage, pages.ListChsPeersPage,
                  pages.ListSubsPeersPage, pages.SeedPage,
                  pages.DeleteSinglePage, pages.DeleteChPage,
                  pages.SupportListPage, pages.SupportAddPage,
                  pages.TrendPage, pages.SearchPage):
    def __init__(self, root):
        # Initialize and show the main frame
        super().__init__(root)  # Frame(root)
        self.pack(fill="both", expand=True)  # Frame.pack()

        self.setup_vars()  # Initialized from `Variables` class
        self.setup_widgets(parent=self)  # the new Frame is the main container

    def setup_widgets(self, parent):
        # Virtual event used in some widgets
        parent.event_add("<<Activate>>", "<Return>", "<KP_Enter>")

        self.note = ttk.Notebook(parent)
        self.note.pack(fill="both", expand=True)

        page_s_gen = ttk.Frame(self.note)
        self.note.add(page_s_gen, text="General")

        self.note_sub_gen = ttk.Notebook(page_s_gen)
        page_settings = ttk.Frame(self.note_sub_gen)
        page_status = ttk.Frame(self.note_sub_gen)
        self.note_sub_gen.add(page_settings, text="Settings")
        self.note_sub_gen.add(page_status, text="Status")
        self.note_sub_gen.pack(fill="both", expand=True)

        page_s_d = ttk.Frame(self.note)
        self.note.add(page_s_d, text="Download")

        self.note_sub_d = ttk.Notebook(page_s_d)
        page_dch = ttk.Frame(self.note_sub_d)
        page_d = ttk.Frame(self.note_sub_d)
        self.note_sub_d.add(page_dch, text="Download channel")
        self.note_sub_d.add(page_d, text="Download single")
        self.note_sub_d.pack(fill="both", expand=True)

        self.note_sub_d.bind("<<NotebookTabChanged>>", self.update_checkbox)

        page_s_list = ttk.Frame(self.note)
        self.note.add(page_s_list, text="List claims")

        self.note_sub_list = ttk.Notebook(page_s_list)
        page_down_list = ttk.Frame(self.note_sub_list)
        page_down_list_inv = ttk.Frame(self.note_sub_list)
        page_ch_claims = ttk.Frame(self.note_sub_list)
        page_subscr_chs = ttk.Frame(self.note_sub_list)
        page_pub_chs = ttk.Frame(self.note_sub_list)
        page_pub_claims = ttk.Frame(self.note_sub_list)
        page_ctr_claims = ttk.Frame(self.note_sub_list)
        self.note_sub_list.add(page_down_list, text="Downloaded claims")
        self.note_sub_list.add(page_down_list_inv, text="Invalid claims")
        self.note_sub_list.add(page_ch_claims, text="Channel claims")
        self.note_sub_list.add(page_subscr_chs, text="Subscribed channels")
        self.note_sub_list.add(page_pub_chs, text="Created channels")
        self.note_sub_list.add(page_pub_claims, text="Published claims")
        self.note_sub_list.add(page_ctr_claims, text="Controlling claims")
        self.note_sub_list.pack(fill="both", expand=True)

        page_s_peers = ttk.Frame(self.note)
        self.note.add(page_s_peers, text="Peers")

        self.note_sub_peers = ttk.Notebook(page_s_peers)
        page_ch_peers = ttk.Frame(self.note_sub_peers)
        page_chs_peers = ttk.Frame(self.note_sub_peers)
        page_subs_peers = ttk.Frame(self.note_sub_peers)
        page_seed_ratio = ttk.Frame(self.note_sub_peers)
        self.note_sub_peers.add(page_ch_peers, text="Channel peers")
        self.note_sub_peers.add(page_chs_peers, text="Multiple channel peers")
        self.note_sub_peers.add(page_subs_peers, text="Subscription peers")
        self.note_sub_peers.add(page_seed_ratio, text="Seeding ratio")
        self.note_sub_peers.pack(fill="both", expand=True)

        page_s_del = ttk.Frame(self.note)
        self.note.add(page_s_del, text="Delete")

        note_sub_del = ttk.Notebook(page_s_del)
        page_del = ttk.Frame(note_sub_del)
        page_delch = ttk.Frame(note_sub_del)
        note_sub_del.add(page_del, text="Delete single")
        note_sub_del.add(page_delch, text="Clean up channel")
        note_sub_del.pack(fill="both", expand=True)

        page_s_sup = ttk.Frame(self.note)
        self.note.add(page_s_sup, text="Supports")

        note_sub_sup = ttk.Notebook(page_s_sup)
        page_supports = ttk.Frame(note_sub_sup)
        page_add_supports = ttk.Frame(note_sub_sup)
        note_sub_sup.add(page_supports, text="List supports")
        note_sub_sup.add(page_add_supports, text="Add or remove support")
        note_sub_sup.pack(fill="both", expand=True)

        page_s_search = ttk.Frame(self.note)
        self.note.add(page_s_search, text="Search")

        self.note_sub_search = ttk.Notebook(page_s_search)
        page_trend = ttk.Frame(self.note_sub_search)
        page_search = ttk.Frame(self.note_sub_search)
        self.note_sub_search.add(page_trend, text="Trending claims")
        self.note_sub_search.add(page_search, text="Search")
        self.note_sub_search.pack(fill="both", expand=True)

        self.note_sub_search.bind("<<NotebookTabChanged>>",
                                  self.update_search_checkbox)

        # page_s_other = ttk.Frame(self.note)
        # self.note.add(page_s_other, text="Other")
        # lb_other = ttk.Label(page_s_other,
        #                      text=("Functions that don't fit "
        #                            "a better category will be placed here"))
        # lb_other.pack(pady=4)

        self.note.select(page_s_d)

        # Built from the mixin `Page` classes
        self.setup_page_settings(page_settings)
        self.setup_page_status(page_status)

        self.setup_page_dch(page_dch)
        self.setup_page_d(page_d)

        self.setup_page_down_list(page_down_list)
        self.setup_page_down_list_inv(page_down_list_inv)
        self.setup_page_ch_claims(page_ch_claims)
        self.setup_page_subscr_chs(page_subscr_chs)
        self.setup_page_pub_chs(page_pub_chs)
        self.setup_page_pub_claims(page_pub_claims)
        self.setup_page_controlling(page_ctr_claims)

        self.setup_page_ch_peers(page_ch_peers)
        self.setup_page_chs_peers(page_chs_peers)
        self.setup_page_subs_peers(page_subs_peers)
        self.setup_page_seed(page_seed_ratio)
        self.setup_plot()

        self.setup_page_del(page_del)
        self.setup_page_delch(page_delch)

        self.setup_page_supports(page_supports)
        self.setup_page_add_supports(page_add_supports)

        self.setup_page_trend(page_trend)
        self.setup_page_search(page_search)

    def print_done(self, print_msg=True):
        if print_msg:
            print(40 * "-")
            print("Done")

    def get_lbry_settings(self):
        """Get the settings of the current lbrynet daemon."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        content = actions.get_lbrynet_settings(server=self.server_var.get())

        self.textbox_settings["state"] = "normal"
        self.textbox_settings.replace("1.0", tk.END, content)
        self.textbox_settings["state"] = "disabled"
        self.print_done(print_msg=True)

    def get_lbry_status(self):
        """Get the status of the currently running daemon."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        content = actions.get_lbrynet_status(server=self.server_var.get())

        self.textbox_status["state"] = "normal"
        self.textbox_status.replace("1.0", tk.END, content)
        self.textbox_status["state"] = "disabled"
        self.print_done(print_msg=True)

    def update_checkbox(self, event):
        page = self.note_sub_d.tab(self.note_sub_d.select())["text"]
        if page == "Download channel":
            self.chck_enable_dch(force_second_var=False)
        elif page == "Download single":
            self.chck_enable_d(force_second_var=False)

    def validate_ch(self, print_msg=True):
        """Validate the textbox with channels and numbers."""
        page = self.note.tab(self.note.select())["text"]

        if page == "Download":
            text = self.textbox_dch.get("1.0", tk.END)
        elif page == "Delete":
            text = self.textbox_delch.get("1.0", tk.END)
        elif page == "Peers":
            text = self.textbox_chs_peers.get("1.0", tk.END)

        validated_chs = val.validate_input(text,
                                           assume_channel=True,
                                           number_float=False,
                                           print_msg=print_msg)

        self.print_done(print_msg=print_msg)

        return validated_chs

    def resolve_ch(self, print_msg=True):
        """Resolve the channels in the textbox online."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        validated_chs = self.validate_ch(print_msg=False)

        ddir = res.check_download_dir(ddir=self.entry_d_dir.get(),
                                      server=self.server_var.get())
        self.entry_d_dir.set(ddir)

        resolved_chs = res.resolve_ch(validated_chs, print_msg=print_msg,
                                      server=self.server_var.get())

        self.print_done(print_msg=print_msg)

        return resolved_chs

    def download_ch(self):
        """Download the claims from the channels in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        resolved_chs = self.resolve_ch(print_msg=False)
        actions.download_ch(resolved_chs,
                            ddir=self.entry_d_dir.get(),
                            own_dir=self.check_d_own_dir.get(),
                            save_file=self.check_d_save.get(),
                            repost=self.check_d_repost.get(),
                            server=self.server_var.get())

        self.print_done(print_msg=True)

    def resolve_claims(self, print_msg=True):
        """Resolve the claims in the textbox online."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        page = self.note.tab(self.note.select())["text"]

        if page == "Download":
            ddir = res.check_download_dir(ddir=self.entry_d_dir.get(),
                                          server=self.server_var.get())
            self.entry_d_dir.set(ddir)
            text = self.textbox_d.get("1.0", tk.END)
        elif page == "Delete":
            text = self.textbox_del.get("1.0", tk.END)

        claims = res.resolve_claims(text,
                                    repost=self.check_d_repost.get(),
                                    print_msg=print_msg,
                                    server=self.server_var.get())

        self.print_done(print_msg=print_msg)

        return claims

    def download_claims(self):
        """Download the claims in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        claims = self.resolve_claims(print_msg=False)
        actions.download_claims(claims,
                                ddir=self.entry_d_dir.get(),
                                own_dir=self.check_d_own_dir.get(),
                                save_file=self.check_d_save.get(),
                                repost=self.check_d_repost.get(),
                                server=self.server_var.get())

        self.print_done(print_msg=True)

    def list_d_claims(self, invalid=False):
        """Print the downloaded claims in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        if self.entry_chan.get():
            self.check_lst_show_ch.set(True)

        content, number, size, seconds = \
            actions.print_claims(blocks=self.check_lst_blks.get(),
                                 cid=self.check_lst_cid.get(),
                                 blobs=self.check_lst_blobs.get(),
                                 size=self.check_lst_size.get(),
                                 show_channel=self.check_lst_show_ch.get(),
                                 show_out=self.rad_lst_name.get(),
                                 channel=self.entry_chan.get(),
                                 invalid=invalid,
                                 reverse=self.check_lst_reverse.get(),
                                 server=self.server_var.get())

        if not content:
            content = "No claims found"

        text = actions.list_text_size(number, size, seconds)

        if not invalid:
            self.textbox_list.replace("1.0", tk.END, content)
            self.label_lst_info.set(text)
        else:
            self.textbox_list_inv.replace("1.0", tk.END, content)
            self.label_lst_inv_info.set(text)
        self.print_done(print_msg=True)

    def list_d_claims_inv(self):
        """Print the invalid downloaded claims in the textbox."""
        self.list_d_claims(invalid=True)

    def resolve_ch_list(self, print_msg=True):
        """Resolve the channel to make sure it exists."""
        channel = self.entry_chl_chan.get()

        if not channel:
            self.print_done(print_msg=True)
            return False

        if not channel.startswith("@"):
            channel = "@" + channel
            self.entry_chl_chan.set(channel)

        validated_chs = [{"claim": channel,
                          "number": False}]
        resolved_chs = res.resolve_ch(validated_chs, print_msg=print_msg,
                                      server=self.server_var.get())

        resolved_ch = resolved_chs[0]
        if "NOT_FOUND" in resolved_ch["info"]:
            self.print_done(print_msg=True)
            return False

        channel = resolved_ch["info"].lstrip("lbry://")
        self.print_done(print_msg=print_msg)

        return channel

    def list_ch_claims(self):
        """Print the channel claims in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        channel = self.resolve_ch_list(print_msg=True)
        if not channel:
            return False

        content, number, size, seconds = \
            actions.print_ch_claims(channel,
                                    number=self.spin_chl_num.get(),
                                    blocks=self.chck_chl_blk.get(),
                                    claim_id=self.chck_chl_cid.get(),
                                    typ=self.chck_chl_type.get(),
                                    ch_name=self.chck_chl_chname.get(),
                                    title=self.chck_chl_title.get(),
                                    start=1, end=0,
                                    reverse=self.chck_chl_reverse.get(),
                                    server=self.server_var.get())

        text = actions.list_text_size(number, size, seconds)

        self.textbox_ch_list.replace("1.0", tk.END, content)
        self.label_chl_info.set(text)
        self.print_done(print_msg=True)

    def list_subscr_chs(self):
        """Print the subscribed channels in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        content = \
            actions.list_ch_subs(action="subscriptions",
                                 shared=self.rad_subs_shared.get(),
                                 show=self.rad_subs_show.get(),
                                 threads=self.spin_subs_threads.get(),
                                 claim_id=self.check_subs_claim_id.get())

        self.textbox_ch_subs_list.replace("1.0", tk.END, content)
        self.print_done(print_msg=True)

    def list_subscr_chs_claims(self):
        """Print the subscribed channels' latest claims in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        if self.spin_subs_claim_num.get() <= 0:
            self.spin_subs_claim_num.set(1)
            print("Number of claims set to: 1")

        content = \
            actions.list_ch_subs(action="latest_claims",
                                 number=self.spin_subs_claim_num.get(),
                                 shared=self.rad_subs_shared.get(),
                                 show=self.rad_subs_show.get(),
                                 threads=self.spin_subs_threads.get(),
                                 claim_id=self.check_subs_claim_id.get(),
                                 title=self.check_subs_title.get())

        self.textbox_ch_subs_list.replace("1.0", tk.END, content)
        self.print_done(print_msg=True)

    def list_pub_chs(self, print_msg=True):
        """Print the channels defined in the wallet in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        output = actions.list_pub_chs(is_spent=self.chck_ch_spent.get(),
                                      updates=self.chck_ch_upd.get(),
                                      claim_id=self.chck_ch_cid.get(),
                                      addresses=self.chck_ch_addr.get(),
                                      accounts=self.chck_ch_acc.get(),
                                      amounts=self.chck_ch_amount.get(),
                                      reverse=self.chck_pub_rev.get(),
                                      server=self.server_var.get())

        summary = output["summary"]
        if summary:
            content = summary + "\n" + output["content"]
        else:
            content = output["content"]

        self.textbox_p_chs.replace("1.0", tk.END, content)
        self.print_done(print_msg=print_msg)

        return output["channels"]

    def fill_ch_list(self, print_msg=True):
        """Print the claims defined in the wallet in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        channels = self.list_pub_chs(print_msg=False)

        combo_values = ["All", "Anonymous"]
        for ch in channels:
            combo_values.append(ch["name"])

        self.combo_pub_ch["values"] = combo_values
        self.print_done(print_msg=print_msg)

    def list_pub_claims(self):
        """Print the claims defined in the wallet in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        self.fill_ch_list(print_msg=False)

        output = actions.list_pub_claims(is_spent=self.chck_ch_spent.get(),
                                         select=self.chck_pub_ch.get(),
                                         updates=self.chck_ch_upd.get(),
                                         claim_id=self.chck_ch_cid.get(),
                                         addresses=self.chck_ch_addr.get(),
                                         typ=self.chck_pub_types.get(),
                                         amounts=self.chck_ch_amount.get(),
                                         title=self.chck_pub_title.get(),
                                         reverse=self.chck_pub_rev.get(),
                                         server=self.server_var.get())

        summary = output["summary"]
        if summary:
            content = summary + "\n" + output["content"]
        else:
            content = output["content"]

        self.textbox_p_claims.replace("1.0", tk.END, content)
        self.print_done(print_msg=True)

    def controlling_claims(self):
        """Print the information of the controlling claims."""
        content = \
            actions.ctrl_claims(show_contr=self.check_c_contr.get(),
                                show_non_contr=self.check_c_non_contr.get(),
                                skip_repost=self.check_c_skip_repost.get(),
                                channels_only=self.check_c_ch_only.get(),
                                show_claim_id=self.check_c_cid.get(),
                                show_repost_st=self.check_c_is_repost.get(),
                                show_competing=self.check_c_compete.get(),
                                show_reposts=self.check_c_reposts.get(),
                                compact=self.check_c_compact.get(),
                                server=self.server_var.get())

        self.textbox_controlling.replace("1.0", tk.END, content)
        self.print_done(print_msg=True)

    def list_ch_peers(self):
        """Print the peers of the claims of a channel."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        channel = self.resolve_ch_list(print_msg=True)
        if not channel:
            return False

        output = \
            actions.list_peers(channel=self.entry_chl_chan.get(),
                               number=self.spin_ch_peers_num.get(),
                               threads=self.spin_ch_peers_threads.get(),
                               claim_id=self.chck_ch_peers_cid.get(),
                               typ=self.chck_ch_peers_type.get(),
                               title=self.chck_ch_peers_title.get(),
                               server=self.server_var.get())

        content = output["summary"] + "\n"
        content += 80 * "-" + "\n"
        content += output["lines"]
        self.textbox_ch_peers.replace("1.0", tk.END, content)
        self.print_done(print_msg=True)

    def list_chs_peers(self):
        """Print the peers from the channels listed in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        resolved_chs = self.resolve_ch(print_msg=False)

        output = \
            actions.list_ch_peers(resolved_chs,
                                  ch_threads=self.spin_chs_ch_threads.get(),
                                  claim_threads=self.spin_chs_cl_threads.get(),
                                  server=self.server_var.get())

        content = output["summary"]
        content += 80 * "-" + "\n"
        content += output["lines"]
        self.textbox_chs_peers_out.replace("1.0", tk.END, content)
        self.print_done(print_msg=True)

    def list_subs_peers(self):
        """Print peers from our list of subscribed channels."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        if self.spin_ch_peers_num.get() <= 0:
            self.spin_ch_peers_num.set(1)
            print("Number of claims set to: 1")

        output = \
            actions.list_subs_peers(number=self.spin_ch_peers_num.get(),
                                    shared=self.rad_subs_pr_shared.get(),
                                    show=self.rad_subs_pr_show.get(),
                                    ch_threads=self.spin_subs_ch_threads.get(),
                                    c_threads=self.spin_subs_cl_threads.get(),
                                    server=self.server_var.get())

        content = output["summary"]
        content += 80 * "-" + "\n"
        content += output["lines"]
        self.textbox_subs_peers.replace("1.0", tk.END, content)
        self.print_done(print_msg=True)

    def seeding_ratio(self):
        """Print estimated seeding ratio from the log files."""
        frame = None

        if self.check_seed_plot.get():
            if not hasattr(self, "top_plot"):
                # This is normally not called because the plot toplevel
                # is already set up by `SeedPage.setup_page_seed`
                frame = self.setup_plot()
                frame.deiconify()
            elif hasattr(self, "top_plot"):
                if self.top_plot.children:
                    # We remove the content before reusing the toplevel
                    frame = self.remove_plot()
                else:
                    # The toplevel is empty, so we just use it
                    frame = self.top_plot
                frame.deiconify()

        content = \
            actions.seeding_ratio(frame=frame,
                                  plot_hst_var=self.check_seed_plot.get(),
                                  server=self.server_var.get())

        self.textbox_seed.replace("1.0", tk.END, content)
        self.print_done(print_msg=True)

    def delete_claims(self):
        """Delete the claims in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        claims = self.resolve_claims(print_msg=False)
        actions.delete_claims(claims,
                              what=self.rad_delete_what.get(),
                              server=self.server_var.get())

        self.print_done(print_msg=True)

    def delete_ch(self):
        """Delete the claims from the channels in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        resolved_chs = self.resolve_ch(print_msg=False)
        actions.clean_ch(resolved_chs,
                         what=self.rad_delete_what.get(),
                         server=self.server_var.get())

        self.print_done(print_msg=True)

    def list_supports(self):
        """List supported claims, either channels or streams."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        content = \
            actions.list_supports(show_ch=self.check_s_ch.get(),
                                  show_claims=self.check_s_claims.get(),
                                  show_cid=self.check_s_cid.get(),
                                  show_combined=self.check_s_combine.get(),
                                  show_invalid=self.check_s_invalid.get(),
                                  server=self.server_var.get())

        self.textbox_supports.replace("1.0", tk.END, content)
        self.print_done(print_msg=True)

    def validate_g_claims(self, print_msg=True):
        """Validate the textbox with claims and numbers."""
        text = self.textbox_add_support.get("1.0", tk.END)
        validated_claims = val.validate_input(text,
                                              assume_channel=False,
                                              number_float=True,
                                              print_msg=print_msg)

        self.print_done(print_msg=print_msg)

        return validated_claims

    def resolve_g_claims(self, print_msg=True):
        """Resolve the claims in the textbox online."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        if self.check_s_supp_inv.get():
            validated_claims = self.validate_g_claims(print_msg=True)
            print("Assuming the claims are 'invalid' claims, "
                  "so they won't be resolved online.")
        else:
            validated_claims = self.validate_g_claims(print_msg=False)
            resolved_claims = \
                res.resolve_claims_supports(validated_claims,
                                            show_support=True,
                                            print_msg=print_msg,
                                            server=self.server_var.get())

        self.print_done(print_msg=print_msg)

        return resolved_claims

    def add_supports(self):
        """Add supports to claims, either channels or streams."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        resolved_claims = self.resolve_g_claims(print_msg=False)

        actions.add_supports(resolved_claims,
                             support_style=self.rad_s_support.get(),
                             invalid=self.check_s_supp_inv.get(),
                             server=self.server_var.get())

        self.print_done(print_msg=True)

    def update_search_checkbox(self, event):
        page = self.note_sub_search.tab(self.note_sub_search.select())["text"]
        if page == "Trending claims":
            if self.rad_tr_claim.get() in ("stream", "repost"):
                self.activate_tr_checks()
                self.switch_tr_all()
            elif self.rad_tr_claim.get() in ("channel", "collection",
                                             "livestream"):
                self.deact_tr_checks()
                self.switch_tr_various()
        elif page == "Search":
            if self.rad_tr_claim.get() in ("stream", "repost"):
                self.activate_sr_checks()
                self.switch_sr_all()
            elif self.rad_tr_claim.get() in ("channel", "collection",
                                             "livestream"):
                self.deact_sr_checks()
                self.switch_sr_various()

    def show_trending_claims(self):
        """Get the trending claims."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        content = actions.print_trending(page=self.spin_page.get(),
                                         claim_id=self.chck_tr_cid.get(),
                                         claim_type=self.rad_tr_claim.get(),
                                         video_stream=self.chck_tr_vid.get(),
                                         audio_stream=self.chck_tr_audio.get(),
                                         doc_stream=self.chck_tr_doc.get(),
                                         img_stream=self.chck_tr_img.get(),
                                         bin_stream=self.chck_tr_bin.get(),
                                         model_stream=self.chck_tr_model.get(),
                                         server=self.server_var.get())

        self.label_tr_info.set("Page: " + str(self.spin_page.get()))
        self.textbox_trend.replace("1.0", tk.END, content)
        self.print_done(print_msg=True)

    def show_search(self):
        """Show the results of a search."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        content = actions.return_search(page=self.spin_page.get(),
                                        text=self.search_entry.get(),
                                        tags=self.search_entry_tags.get(),
                                        claim_id=self.chck_tr_cid.get(),
                                        claim_type=self.rad_tr_claim.get(),
                                        video_stream=self.chck_tr_vid.get(),
                                        audio_stream=self.chck_tr_audio.get(),
                                        doc_stream=self.chck_tr_doc.get(),
                                        img_stream=self.chck_tr_img.get(),
                                        bin_stream=self.chck_tr_bin.get(),
                                        model_stream=self.chck_tr_model.get(),
                                        server=self.server_var.get())

        self.label_sch_info.set("Page: " + str(self.spin_page.get()))
        self.textbox_search.replace("1.0", tk.END, content)
        self.print_done(print_msg=True)


def main(argv=None):
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.title("lbrydseed")

    # Set up icon for all top levels
    root.iconphoto(True, tk.PhotoImage(file="lbrydseed.png"))
    # root.tk.call("wm", "iconphoto", root._w,
    #              tk.PhotoImage(file="lbrydseed.png"))

    # The quit method is explicit because we create a second toplevel,
    # and it causes problems when we try to close the window
    root.protocol("WM_DELETE_WINDOW", root.quit)

    theme = ttk.Style()
    if "linux" in platform.system().lower():
        theme.theme_use("clam")

    app = Application(root=root)
    app.mainloop()


if __name__ == "__main__":
    sys.exit(main())
