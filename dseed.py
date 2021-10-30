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
                  pages.TrendPage,
                  pages.DownloadChPage, pages.DownloadSinglePage,
                  pages.ListPage,
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

        page_list = ttk.Frame(self.note)
        self.note.add(page_list, text="List claims")

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

        note_sub_search = ttk.Notebook(page_s_search)
        page_trend = ttk.Frame(note_sub_search)
        note_sub_search.add(page_trend, text="Trending claims")
        note_sub_search.pack(fill="both", expand=True)

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
        self.setup_page_del(page_del)
        self.setup_page_delch(page_delch)
        self.setup_page_supports(page_supports)
        self.setup_page_add_supports(page_add_supports)
        self.setup_page_trend(page_trend)
        self.setup_page_seed(page_seed_ratio)
        self.setup_plot()
        self.setup_page_controlling(page_claims)

    def update_checkbox(self, event):
        page = self.note_sub_d.tab(self.note_sub_d.select())["text"]
        if page == "Download channel":
            self.chck_enable_dch(force_second_var=False)
        elif page == "Download single":
            self.chck_enable_d(force_second_var=False)

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

        ddir = res.check_download_dir(ddir=self.down_dir_var.get(),
                                      server=self.server_var.get())
        self.down_dir_var.set(ddir)

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
                            ddir=self.down_dir_var.get(),
                            own_dir=self.own_dir_var.get(),
                            save_file=self.save_var.get(),
                            proceed=True,
                            server=self.server_var.get())

        self.print_done(print_msg=True)

    def resolve_claims(self, print_msg=True):
        """Resolve the claims in the textbox online."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        page = self.note.tab(self.note.select())["text"]

        if page == "Download":
            ddir = res.check_download_dir(ddir=self.down_dir_var.get(),
                                          server=self.server_var.get())
            self.down_dir_var.set(ddir)
            text = self.textbox_d.get("1.0", tk.END)
        elif page == "Delete":
            text = self.textbox_del.get("1.0", tk.END)
        claims = res.resolve_claims(text, print_msg=print_msg,
                                    server=self.server_var.get())

        self.print_done(print_msg=print_msg)

        return claims

    def download_claims(self):
        """Download the claims in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        claims = self.resolve_claims(print_msg=False)
        actions.download_claims(claims,
                                ddir=self.down_dir_var.get(),
                                own_dir=self.own_dir_var.get(),
                                save_file=self.save_var.get(),
                                server=self.server_var.get())

        self.print_done(print_msg=True)

    def list_claims(self):
        """Print the claims in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        if self.entry_chan.get():
            self.check_show_ch.set(True)

        content = actions.print_claims(cid=self.check_cid.get(),
                                       blobs=self.check_blobs.get(),
                                       show_channel=self.check_show_ch.get(),
                                       channel=self.entry_chan.get(),
                                       name=self.check_name.get(),
                                       server=self.server_var.get())

        self.textbox_list.replace("1.0", tk.END, content)
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
            actions.list_supports(show_ch_var=self.check_s_ch.get(),
                                  show_claims_var=self.check_s_claims.get(),
                                  show_cid_var=self.check_s_cid.get(),
                                  combine_var=self.check_s_combine.get(),
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
