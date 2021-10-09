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

import lbseed.resolve as res
import lbseed.validate as vd
import lbseed.actions as actions


def setup_textbox(parent, font="monospace",
                  tab_function=None):
    hsrl = ttk.Scrollbar(parent, orient="horizontal")
    hsrl.pack(side=tk.BOTTOM, fill=tk.X)
    vsrl = ttk.Scrollbar(parent)
    vsrl.pack(side=tk.RIGHT, fill=tk.Y)

    textbox = tk.Text(parent,
                      xscrollcommand=hsrl.set,
                      yscrollcommand=vsrl.set,
                      font=font,
                      width=60, height=10,
                      wrap=tk.NONE)
    textbox.bind("<Tab>", tab_function)

    textbox.pack(side="top", fill="both", expand=True)

    hsrl.config(command=textbox.xview)
    vsrl.config(command=textbox.yview)
    return textbox


def setup_download_entry(parent,
                         server_var=None, dir_var=None,
                         font=None, start=0):
    entry = ttk.Entry(parent, textvariable=server_var,
                      font=font)
    entry.grid(row=start, column=0, sticky=tk.W + tk.E)
    le = ttk.Label(parent,
                   text=("Address of the 'lbrynet' daemon. "
                         "It defaults to localhost:5279"))
    le.grid(row=start, column=1, sticky=tk.W, padx=2)

    entry_dir = ttk.Entry(parent, textvariable=dir_var,
                          font=font)
    entry_dir.grid(row=start+1, column=0, sticky=tk.W + tk.E)
    ledir = ttk.Label(parent,
                      text=("Download directory. "
                            "It defaults to your home directory."))
    ledir.grid(row=start+1, column=1, sticky=tk.W, padx=2)


def setup_download_check(parent, own_dir_var=None, save_var=None,
                         start=0):
    chk_owndir = ttk.Checkbutton(parent,
                                 variable=own_dir_var,
                                 text=("Place the downloaded file "
                                       "inside a subdirectory"))
    chk_owndir.grid(row=start, column=1, sticky=tk.W)

    chk_save = ttk.Checkbutton(parent,
                               variable=save_var,
                               text=("Save media and its blobs; "
                                     "otherwise only the first blob"))
    chk_save.grid(row=start+1, column=1, sticky=tk.W)


def info_claims(parent, start=0):
    info = ttk.Label(parent,
                     text=("Add one claim per row; this should be "
                           "a 'claim_name' or a 'claim_id' "
                           "(40-character string)"))
    info.grid(row=start, column=0, columnspan=2, sticky=tk.W)


def set_up_default_channels():
    channels = ["@my-favorite-channel, 5",
                "@OdyseeHelp#b, 2",
                "@lbry:3f, 4"]
    channels = "\n".join(channels)
    return channels


def set_up_default_claims():
    claims = ["this-is-a-fake-claim",
              "odysee-rss",
              "abcd0000efgh0000ijkl0000mopq0000rstu0000",
              "de458915e3a3c5a894f45785b0bf9b9a67739f79"]
    claims = "\n".join(claims)
    return claims


class Application(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_widgets(parent)

    def setup_widgets(self, parent):
        self.ftmono = tk.font.Font(family="monospace", size=10)
        self.server_var = tk.StringVar()
        self.server_var.set("http://localhost:5279")
        self.down_dir_var = tk.StringVar()
        self.down_dir_var.set(res.get_download_dir(server=self.server_var.get()))
        self.own_dir_var = tk.BooleanVar()
        self.own_dir_var.set(True)
        self.save_var = tk.BooleanVar()
        self.save_var.set(True)

        note = ttk.Notebook(parent)
        page1 = ttk.Frame(note)
        page2 = ttk.Frame(note)
        page3 = ttk.Frame(note)
        page4 = ttk.Frame(note)
        note.add(page1, text="Download channel")
        note.add(page2, text="Download single")
        note.add(page3, text="List")
        note.add(page4, text="Delete single")
        self.setup_page1(page1)
        self.setup_page2(page2)
        self.setup_page3(page3)
        self.setup_page4(page4)
        note.pack()

    def setup_page1(self, parent):
        self.setup_top_dch(parent)
        self.setup_textbox_dch(parent)

    def setup_top_dch(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_dch(frame, start=0)
        self.setup_grid_low_dch(frame, start=2)
        self.setup_info_dch(frame, start=7)

    def setup_grid_top_dch(self, parent, start=0):
        setup_download_entry(parent, server_var=self.server_var,
                             dir_var=self.down_dir_var,
                             font="Monospace 10", start=start)

    def setup_grid_low_dch(self, parent, start=0):
        _width = 26
        b_validate = ttk.Button(parent, text="Validate input",
                                width=_width,
                                command=self.validate_ch)
        b_validate.grid(row=start, column=0)
        b_validate.focus()
        lv = ttk.Label(parent,
                       text="Verify that the input can be read correctly")
        lv.grid(row=start, column=1, sticky=tk.W, padx=2)

        b_resolve = ttk.Button(parent, text="Resolve online",
                               width=_width,
                               command=self.resolve_ch)
        b_resolve.grid(row=start+1, column=0)
        lr = ttk.Label(parent,
                       text="Confirm that the channels exist")
        lr.grid(row=start+1, column=1, sticky=tk.W, padx=2)

        b_download = ttk.Button(parent, text="Download claims",
                                width=_width,
                                command=self.download_cha)
        b_download.grid(row=start+2, column=0)
        lr = ttk.Label(parent,
                       text=("Start downloading the newest claims "
                             "from the channels"))
        lr.grid(row=start+2, column=1, sticky=tk.W, padx=2)

        setup_download_check(parent, own_dir_var=self.own_dir_var,
                             save_var=self.save_var,
                             start=start+3)

    def setup_info_dch(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Add a channel, a comma, "
                               "and the number of items to download "
                               "from this channel"))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_dch(self, parent):
        channels = set_up_default_channels()
        self.textbox_dch = setup_textbox(parent, font="monospace",
                                         tab_function=self.focus_next_widget)
        self.textbox_dch.insert("1.0", channels)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def validate_ch(self, print_msg=True):
        text = self.textbox_dch.get("1.0", tk.END)
        channels, numbers = vd.validate_input(text, print_msg=print_msg)
        return channels, numbers

    def resolve_ch(self, print_msg=True):
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
        return channels, numbers, info

    def download_cha(self):
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

    def setup_page2(self, parent):
        pass

    def setup_page3(self, parent):
        self.setup_top_list(parent)
        self.setup_textbox_list(parent)

    def setup_top_list(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_list(frame, start=0)
        self.setup_grid_low_list(frame, start=3)

    def setup_grid_top_list(self, parent, start=0):
        _width = 26
        b_list = ttk.Button(parent, text="List claims",
                            width=_width,
                            command=self.list_claims)
        b_list.grid(row=start, column=0)
        llist = ttk.Label(parent,
                          text="List all locally downloaded claims")
        llist.grid(row=start, column=1, sticky=tk.W, padx=2)

        self.entry_chan = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=self.entry_chan,
                          font=self.ftmono)
        entry.grid(row=start+1, column=0, sticky=tk.W + tk.E)
        le = ttk.Label(parent,
                       text="Filter by channel name")
        le.grid(row=start+1, column=1, sticky=tk.W, padx=2)

    def setup_grid_low_list(self, parent, start=0):
        self.check_cid = tk.BooleanVar()
        self.check_cid.set(False)
        chck_cid = ttk.Checkbutton(parent,
                                   variable=self.check_cid,
                                   text="Show 'claim_id'")
        chck_cid.grid(row=start, column=1, sticky=tk.W)

        self.check_blobs = tk.BooleanVar()
        self.check_blobs.set(True)
        chck_blobs = ttk.Checkbutton(parent,
                                     variable=self.check_blobs,
                                     text="Show number of blobs")
        chck_blobs.grid(row=start+1, column=1, sticky=tk.W)

        self.show_ch = tk.BooleanVar()
        self.show_ch.set(True)
        chck_ch = ttk.Checkbutton(parent,
                                  variable=self.show_ch,
                                  text="Show channel of the claim")
        chck_ch.grid(row=start+2, column=1, sticky=tk.W)

        self.check_name = tk.BooleanVar()
        self.check_name.set(True)
        chck_name = ttk.Checkbutton(parent,
                                    variable=self.check_name,
                                    text="Show 'claim_name'")
        chck_name.grid(row=start+3, column=1, sticky=tk.W)

    def setup_textbox_list(self, parent):
        self.textbox_list = setup_textbox(parent, font="monospace 8",
                                          tab_function=self.focus_next_widget)

    def list_claims(self):
        if not res.server_exists(server=self.server_var.get()):
            return False

        if self.entry_chan.get():
            self.show_ch.set(True)

        content = actions.print_claims(cid=self.check_cid.get(),
                                       blobs=self.check_blobs.get(),
                                       show_channel=self.show_ch.get(),
                                       channel=self.entry_chan.get(),
                                       name=self.check_name.get(),
                                       server=self.server_var.get())

        self.textbox_list.replace("1.0", tk.END, content)
        print(40 * "-")
        print("Done")

    def setup_page4(self, parent):
        self.setup_top_del(parent)
        self.setup_textbox_del(parent)
        
    def setup_top_del(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_del(frame, start=0)
        self.setup_grid_low_del(frame, start=2)
        self.setup_info_del(frame, start=5)

    def setup_grid_top_del(self, parent, start=0):
        _width = 26
        b_resolve_del = ttk.Button(parent, text="Resolve online",
                                   width=_width,
                                   command=self.resolve_claims)
        b_resolve_del.grid(row=start, column=0)
        lrdel = ttk.Label(parent,
                          text="Confirm that the claims exist")
        lrdel.grid(row=start, column=1, sticky=tk.W, padx=2)

        b_del = ttk.Button(parent, text="Delete claims", 
                           width=_width, 
                           command=self.del_claims)
        b_del.grid(row=start+1, column=0)
        ldel = ttk.Label(parent,
                         text="Delete locally downloaded claims")
        ldel.grid(row=start+1, column=1, sticky=tk.W, padx=2)

    def setup_grid_low_del(self, parent, start=0):
        self.del_what_var = tk.StringVar()
        self.del_what_var.set("media")

        media = ttk.Radiobutton(parent,
                                text="Delete media (keep seeding the claim)",
                                variable=self.del_what_var, value="media")
        blobs = ttk.Radiobutton(parent,
                                text="Delete blobs (keep media in download directory)",
                                variable=self.del_what_var, value="blobs")
        both = ttk.Radiobutton(parent,
                               text="Delete both (completely remove the claim)",
                               variable=self.del_what_var, value="both")
        media.grid(row=start, column=1, sticky=tk.W)
        blobs.grid(row=start+1, column=1, sticky=tk.W)
        both.grid(row=start+2, column=1, sticky=tk.W)

    def setup_info_del(self, parent, start=0):
        info_claims(parent, start=start)

    def setup_textbox_del(self, parent):
        claims = set_up_default_claims()
        self.textbox_del = setup_textbox(parent, font="monospace",
                                         tab_function=self.focus_next_widget)
        self.textbox_del.insert("1.0", claims)

    def resolve_claims(self, print_msg=True):
        if not res.server_exists(server=self.server_var.get()):
            return False

        text = self.textbox_del.get("1.0", tk.END)
        claims = res.resolve_claims(text, print_msg=print_msg,
                                    server=self.server_var.get())
        return claims

    def del_claims(self):
        if not res.server_exists(server=self.server_var.get()):
            return False

        claims = self.resolve_claims(print_msg=False)
        actions.delete_claims(claims, what=self.del_what_var.get(),
                              server=self.server_var.get())
        print(40 * "-")
        print("Done")


def main(argv=None):
    root = tk.Tk()
    app = Application(root)

    them = ttk.Style()
    if "linux" in platform.system().lower():
        them.theme_use("clam")

    app.master.title("lbrydseed")
    app.mainloop()


if __name__ == "__main__":
    sys.exit(main())

