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
import lbseed.resolve as res
import lbseed.validate as val
import lbseed.actions as actions


class Application(ttk.Frame,
                  pages.Variables,
                  pages.ConfigPage,
                  pages.TrendPage, pages.SearchPage,
                  pages.DownloadChPage, pages.DownloadSinglePage,
                  pages.ListPage, pages.ListInvalidPage, pages.ListChPage,
                  pages.ListChSubsPage,
                  pages.DeleteSinglePage, pages.DeleteChPage,
                  pages.SupportListPage, pages.SupportAddPage, pages.SeedPage,
                  pages.ControllingClaimsPage):
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

        page_cfg = ttk.Frame(self.note)
        self.note.add(page_cfg, text="General")

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
        page_list = ttk.Frame(self.note_sub_list)
        page_list_inv = ttk.Frame(self.note_sub_list)
        page_ch_claims = ttk.Frame(self.note_sub_list)
        page_ch_subs = ttk.Frame(self.note_sub_list)
        self.note_sub_list.add(page_list, text="List downloaded claims")
        self.note_sub_list.add(page_list_inv, text="List invalid claims")
        self.note_sub_list.add(page_ch_claims, text="List channel claims")
        self.note_sub_list.add(page_ch_subs, text="Subscribed channels")
        self.note_sub_list.pack(fill="both", expand=True)

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

        page_s_adv = ttk.Frame(self.note)
        self.note.add(page_s_adv, text="Advanced")

        note_sub_adv = ttk.Notebook(page_s_adv)
        page_seed_ratio = ttk.Frame(note_sub_adv)
        page_claims = ttk.Frame(note_sub_adv)
        note_sub_adv.add(page_seed_ratio, text="Seeding ratio")
        note_sub_adv.add(page_claims, text="Controlling claims")
        note_sub_adv.pack(fill="both", expand=True)

        self.note.select(page_s_d)

        # Built from the mixin `Page` classes
        self.setup_page_cfg(page_cfg)
        self.setup_page_dch(page_dch)
        self.setup_page_d(page_d)
        self.setup_page_list(page_list)
        self.setup_page_list_inv(page_list_inv)
        self.setup_page_ch_claims(page_ch_claims)
        self.setup_page_ch_subs(page_ch_subs)
        self.setup_page_del(page_del)
        self.setup_page_delch(page_delch)
        self.setup_page_supports(page_supports)
        self.setup_page_add_supports(page_add_supports)
        self.setup_page_trend(page_trend)
        self.setup_page_search(page_search)
        self.setup_page_seed(page_seed_ratio)
        self.setup_plot()
        self.setup_page_controlling(page_claims)

    def update_checkbox(self, event):
        page = self.note_sub_d.tab(self.note_sub_d.select())["text"]
        if page == "Download channel":
            self.chck_enable_dch(force_second_var=False)
        elif page == "Download single":
            self.chck_enable_d(force_second_var=False)

    def update_search_checkbox(self, event):
        page = self.note_sub_search.tab(self.note_sub_search.select())["text"]
        if page == "Trending claims":
            if self.chck_tr_claim_t.get() in ("stream", "repost"):
                self.activate_tr_checks()
                self.switch_tr_all()
            elif self.chck_tr_claim_t.get() in ("channel", "collection",
                                                "livestream"):
                self.deactivate_tr_checks()
                self.switch_tr_various()
        elif page == "Search":
            if self.chck_tr_claim_t.get() in ("stream", "repost"):
                self.activate_sr_checks()
                self.switch_sr_all()
            elif self.chck_tr_claim_t.get() in ("channel", "collection",
                                                "livestream"):
                self.deactivate_sr_checks()
                self.switch_sr_various()

    def print_done(self, print_msg=True):
        if print_msg:
            print(40 * "-")
            print("Done")

    def validate_ch(self, print_msg=True):
        """Validate the textbox with channels and numbers."""
        page = self.note.tab(self.note.select())["text"]

        if page == "Download":
            text = self.textbox_dch.get("1.0", tk.END)
        elif page == "Delete":
            text = self.textbox_delch.get("1.0", tk.END)
        channels, numbers = val.validate_input(text,
                                               assume_channel=True,
                                               number_float=False,
                                               print_msg=print_msg)

        self.print_done(print_msg=print_msg)

        return channels, numbers

    def resolve_ch(self, print_msg=True):
        """Resolve the channels in the textbox online."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        channels, numbers = self.validate_ch(print_msg=False)

        ddir = res.check_download_dir(ddir=self.entry_d_dir.get(),
                                      server=self.server_var.get())
        self.entry_d_dir.set(ddir)

        info = res.resolve_ch(channels, numbers, print_msg=print_msg,
                              server=self.server_var.get())

        self.print_done(print_msg=print_msg)

        return channels, numbers, info

    def download_ch(self):
        """Download the claims from the channels in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        channels, numbers, info = self.resolve_ch(print_msg=False)
        actions.download_ch(channels, numbers, info,
                            repost=self.check_d_repost.get(),
                            ddir=self.entry_d_dir.get(),
                            own_dir=self.check_d_own_dir.get(),
                            save_file=self.check_d_save.get(),
                            proceed=True,
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
                                repost=self.check_d_repost.get(),
                                ddir=self.entry_d_dir.get(),
                                own_dir=self.check_d_own_dir.get(),
                                save_file=self.check_d_save.get(),
                                server=self.server_var.get())

        self.print_done(print_msg=True)

    def list_claims(self, invalid=False):
        """Print the claims in the textbox."""
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

    def list_inv_claims(self):
        self.list_claims(invalid=True)

    def resolve_ch_list(self, print_msg=True):
        """Resolve the channel to make sure it exists."""
        channel = self.entry_chl_chan.get()

        if not channel:
            self.print_done(print_msg=True)
            return False

        if not channel.startswith("@"):
            channel = "@" + channel
            self.entry_chl_chan.set(channel)

        ch = res.resolve_ch([channel], numbers=None,
                            print_msg=print_msg,
                            server=self.server_var.get())

        ch = ch[0]
        if "NOT_FOUND" in ch:
            self.print_done(print_msg=True)
            return False

        channel = ch.lstrip("lbry://")
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

    def list_ch_subs(self):
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

    def list_ch_subs_claims(self):
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

    def delete_claims(self):
        """Delete the claims in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        claims = self.resolve_claims(print_msg=False)
        actions.delete_claims(claims, what=self.del_what_var.get(),
                              server=self.server_var.get())

        self.print_done(print_msg=True)

    def delete_ch(self):
        """Delete the claims from the channels in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        channels, numbers, info = self.resolve_ch(print_msg=False)
        actions.clean_ch(channels, numbers, info,
                         what=self.del_what_var.get(),
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

    def controlling_claims(self):
        content = \
            actions.show_claims_bids(show_controlling=self.check_c_contr.get(),
                                     show_non_controlling=self.check_c_non_contr.get(),
                                     skip_repost=self.check_c_skip_repost.get(),
                                     channels_only=self.check_c_ch_only.get(),
                                     show_claim_id=self.check_c_cid.get(),
                                     show_repost_status=self.check_c_is_repost.get(),
                                     show_competing=self.check_c_competing.get(),
                                     show_reposts=self.check_c_reposts.get(),
                                     compact=self.check_c_compact.get(),
                                     server=self.server_var.get())

        self.textbox_controlling.replace("1.0", tk.END, content)
        self.print_done(print_msg=True)

    def validate_g_claims(self, print_msg=True):
        """Validate the textbox with claims and numbers."""
        text = self.textbox_add_support.get("1.0", tk.END)
        claims, supports = val.validate_input(text,
                                              assume_channel=False,
                                              number_float=True,
                                              print_msg=print_msg)

        self.print_done(print_msg=print_msg)

        return claims, supports

    def resolve_g_claims(self, print_msg=True):
        """Resolve the claims in the textbox online."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        if self.check_s_supp_inv.get():
            claims, supports = self.validate_g_claims(print_msg=True)
            print("Assuming the claims are 'invalid' claims, "
                  "so they won't be resolved online.")
        else:
            claims, supports = self.validate_g_claims(print_msg=False)
            claims, supports = \
                res.resolve_claims_pairs(claims, supports,
                                         show_support=True,
                                         print_msg=print_msg,
                                         server=self.server_var.get())

        self.print_done(print_msg=print_msg)

        return claims, supports

    def add_supports(self):
        """Add supports to claims, either channels or streams."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        claims, supports = self.resolve_g_claims(print_msg=False)

        actions.add_supports(claims, supports,
                             support_style=self.rad_s_support.get(),
                             invalid=self.check_s_supp_inv.get(),
                             server=self.server_var.get())

        self.print_done(print_msg=True)

    def show_trending_claims(self):
        """Get the trending claims."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        content = actions.print_trending(page=self.spin_page.get(),
                                         claim_id=self.chck_tr_cid.get(),
                                         claim_type=self.chck_tr_claim_t.get(),
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
                                        claim_type=self.chck_tr_claim_t.get(),
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
