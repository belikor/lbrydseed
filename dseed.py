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
import os
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
                  pages.DownloadChPage, pages.DownloadSinglePage,
                  pages.ListPage,
                  pages.DeletePage, pages.DeleteChPage):
    def __init__(self, root):
        # Initialize and show the main frame
        super().__init__(root)  # Frame(root)
        self.pack()  # Frame.pack()

        self.setup_vars()  # Initialized from `Variables` class
        self.setup_widgets(parent=self)  # the new Frame is the main container

    def setup_widgets(self, parent):
        # Virtual event used in some widgets
        parent.event_add("<<Activate>>", "<Return>", "<KP_Enter>")

        self.note = ttk.Notebook(parent)
        note = self.note
        page_cfg = ttk.Frame(note)
        page_dch = ttk.Frame(note)
        page_d = ttk.Frame(note)
        page_list = ttk.Frame(note)
        page_del = ttk.Frame(note)
        page_delch = ttk.Frame(note)
        note.add(page_cfg, text="General")
        note.add(page_dch, text="Download channel")
        note.add(page_d, text="Download single")
        note.add(page_list, text="List")
        note.add(page_del, text="Delete single")
        note.add(page_delch, text="Clean up channels")
        note.select(page_dch)

        # Built from the mixin `Page` classes
        self.setup_page_cfg(page_cfg)
        self.setup_page_dch(page_dch)
        self.setup_page_d(page_d)
        self.setup_page_list(page_list)
        self.setup_page_del(page_del)
        self.setup_page_delch(page_delch)
        note.pack()

    def validate_ch(self, print_msg=True):
        """Validate the textbox with channels and numbers."""
        title = self.note.tab(self.note.select())["text"]

        if title == "Download channel":
            text = self.textbox_dch.get("1.0", tk.END)
        elif title == "Clean up channels":
            text = self.textbox_delch.get("1.0", tk.END)
        channels, numbers = val.validate_input(text, print_msg=print_msg)
        if print_msg:
            print(40 * "-")
            print("Done")

        return channels, numbers

    def resolve_ch(self, print_msg=True):
        """Resolve the channels in the textbox online."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        channels, numbers = self.validate_ch(print_msg=False)

        ddir = self.down_dir_var.get()
        if not os.path.exists(ddir):
            nddir = res.get_download_dir(server=self.server_var.get())
            self.down_dir_var.set(nddir)
            print(f"Directory does not exist: {ddir}")
            print(f"Default directory: {nddir}")

        info = res.resolve_ch(channels, numbers, print_msg=print_msg,
                              server=self.server_var.get())
        if print_msg:
            print(40 * "-")
            print("Done")

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
        print(40 * "-")
        print("Done")

    def resolve_claims(self, print_msg=True):
        """Resolve the claims in the textbox online."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        title = self.note.tab(self.note.select())["text"]

        if title == "Download single":
            text = self.textbox_d.get("1.0", tk.END)
        elif title == "Delete single":
            text = self.textbox_del.get("1.0", tk.END)
        claims = res.resolve_claims(text, print_msg=print_msg,
                                    server=self.server_var.get())
        if print_msg:
            print(40 * "-")
            print("Done")

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
        print(40 * "-")
        print("Done")

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
        print(40 * "-")
        print("Done")

    def delete_claims(self):
        """Delete the claims in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        claims = self.resolve_claims(print_msg=False)
        actions.delete_claims(claims, what=self.del_what_var.get(),
                              server=self.server_var.get())
        print(40 * "-")
        print("Done")

    def delete_ch(self):
        """Delete the claims from the channels in the textbox."""
        if not res.server_exists(server=self.server_var.get()):
            return False

        channels, numbers, info = self.resolve_ch(print_msg=False)
        actions.clean_ch(channels, numbers, info,
                         what=self.del_what_var.get(),
                         server=self.server_var.get())
        print(40 * "-")
        print("Done")


def main(argv=None):
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.title("lbrydseed")

    theme = ttk.Style()
    if "linux" in platform.system().lower():
        theme.theme_use("clam")

    app = Application(root=root)
    app.mainloop()


if __name__ == "__main__":
    sys.exit(main())
