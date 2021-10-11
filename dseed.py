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
                         dir_var=None,
                         font=None, start=0):
    entry_dir = ttk.Entry(parent, textvariable=dir_var,
                          font=font)
    entry_dir.grid(row=start, column=0, sticky=tk.W + tk.E)
    ledir = ttk.Label(parent,
                      text=("Download directory. "
                            "It defaults to your home directory."))
    ledir.grid(row=start, column=1, sticky=tk.W, padx=2)


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


def set_up_default_channels(clean_up=False):
    channels = ["@my-favorite-channel, 5",
                "@OdyseeHelp#b, 4",
                "@lbry:3f, 6"]

    if clean_up:
        channels = ["@OdyseeHelp, 2",
                    "@my-favorite-channel-vmv, 15",
                    "@lbry, 1",
                    "@The-Best-Channel-ABC, 5"]

    channels = "\n".join(channels)
    return channels


def set_up_default_claims(clean_up=False):
    claims = ["this-is-a-fake-claim",
              "livestream-tutorial:b",
              "abcd0000efgh0000ijkl0000mopq0000rstu0000",
              "8e16d91185aa4f1cd797f93d7714de2a22622759",
              "LBRYPlaylists#d"]

    if clean_up:
        claims = ["abcd0000efgh0000ijkl0000mopq0000rstu0000",
                  "LBRYPlaylists#d",
                  "this-is-a-fake-claim",
                  "livestream-tutorial:b",
                  "8e16d91185aa4f1cd797f93d7714de2a22622759"]

    claims = "\n".join(claims)
    return claims


def setup_delete_radio(parent, del_what_var=None,
                       start=0):
    media = ttk.Radiobutton(parent,
                            text="Delete media (keep seeding the claim)",
                            variable=del_what_var, value="media")
    blobs = ttk.Radiobutton(parent,
                            text="Delete blobs (keep media in download directory)",
                            variable=del_what_var, value="blobs")
    both = ttk.Radiobutton(parent,
                           text="Delete both (completely remove the claim)",
                           variable=del_what_var, value="both")
    media.grid(row=start, column=1, sticky=tk.W)
    blobs.grid(row=start+1, column=1, sticky=tk.W)
    both.grid(row=start+2, column=1, sticky=tk.W)


def setup_grid_button_val_res(parent,
                              validate_func=None,
                              resolve_func=None,
                              start=0):
    _width = 26
    b_validate = ttk.Button(parent, text="Validate input",
                            width=_width,
                            command=validate_func)
    b_validate.grid(row=start, column=0)
    b_validate.focus()
    lv = ttk.Label(parent,
                   text="Verify that the input can be read correctly")
    lv.grid(row=start, column=1, sticky=tk.W, padx=2)

    b_resolve = ttk.Button(parent, text="Resolve online",
                           width=_width,
                           command=resolve_func)
    b_resolve.grid(row=start+1, column=0)
    lr = ttk.Label(parent,
                   text="Confirm that the channels exist")
    lr.grid(row=start+1, column=1, sticky=tk.W, padx=2)


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
        self.del_what_var = tk.StringVar()
        self.del_what_var.set("media")

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
        self.setup_page_cfg(page_cfg)
        self.setup_page_dch(page_dch)
        self.setup_page_d(page_d)
        self.setup_page_list(page_list)
        self.setup_page_del(page_del)
        self.setup_page_delch(page_delch)
        note.pack()

    def setup_page_cfg(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_top_config(frame,
                              server_var=self.server_var,
                              font="Monospace 10", start=0)

    def setup_top_config(self, parent, server_var=None, font=None, start=0):
        _width = 26
        entry = ttk.Entry(parent, textvariable=server_var, font=font,
                          width=_width)
        entry.grid(row=start, column=0, sticky=tk.W + tk.E)
        le = ttk.Label(parent,
                       text=("Address of the 'lbrynet' daemon. "
                             "It defaults to localhost:5279"))
        le.grid(row=start, column=1, sticky=tk.W, padx=2)

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
        setup_download_entry(parent,
                             dir_var=self.down_dir_var,
                             font="Monospace 10", start=start)

    def setup_grid_button_dch(self, parent, start=0):
        setup_grid_button_val_res(parent,
                                  validate_func=self.validate_ch,
                                  resolve_func=self.resolve_ch,
                                  start=start)

        _width = 26
        b_download = ttk.Button(parent, text="Download claims",
                                width=_width,
                                command=self.download_cha)
        b_download.grid(row=start+2, column=0)
        lr = ttk.Label(parent,
                       text=("Start downloading the newest claims "
                             "from the channels"))
        lr.grid(row=start+2, column=1, sticky=tk.W, padx=2)

    def setup_grid_check_dch(self, parent, start=0):
        setup_download_check(parent, own_dir_var=self.own_dir_var,
                             save_var=self.save_var,
                             start=start)

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
        title = self.note.tab(self.note.select())["text"]

        if title == "Download channel":
            text = self.textbox_dch.get("1.0", tk.END)
        elif title == "Clean up channels":
            text = self.textbox_delch.get("1.0", tk.END)
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
        setup_download_entry(parent,
                             dir_var=self.down_dir_var,
                             font="Monospace 10", start=start)

    def setup_grid_button_d(self, parent, start=0):
        _width = 26
        b_resolve = ttk.Button(parent, text="Resolve online",
                               width=_width,
                               command=self.resolve_claims)
        b_resolve.grid(row=start, column=0)
        lr = ttk.Label(parent,
                       text="Confirm that the claims exist")
        lr.grid(row=start, column=1, sticky=tk.W, padx=2)

        b_download = ttk.Button(parent, text="Download claims",
                                width=_width,
                                command=self.download_claims)
        b_download.grid(row=start+1, column=0)
        l2 = ttk.Label(parent,
                       text="Start downloading the claims")
        l2.grid(row=start+1, column=1, sticky=tk.W, padx=2)

    def setup_grid_check_d(self, parent, start=0):
        setup_download_check(parent, own_dir_var=self.own_dir_var,
                             save_var=self.save_var,
                             start=start)

    def setup_info_d(self, parent, start=0):
        info_claims(parent, start=start)

    def setup_textbox_d(self, parent):
        claims = set_up_default_claims()
        self.textbox_d = setup_textbox(parent, font="monospace",
                                       tab_function=self.focus_next_widget)
        self.textbox_d.insert("1.0", claims)

    def resolve_claims(self, print_msg=True):
        if not res.server_exists(server=self.server_var.get()):
            return False

        title = self.note.tab(self.note.select())["text"]

        if title == "Download single":
            text = self.textbox_d.get("1.0", tk.END)
        elif title == "Delete single":
            text = self.textbox_del.get("1.0", tk.END)
        claims = res.resolve_claims(text, print_msg=print_msg,
                                    server=self.server_var.get())
        return claims

    def download_claims(self):
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

    def setup_page_list(self, parent):
        self.setup_top_list(parent)
        self.setup_textbox_list(parent)

    def setup_top_list(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_list(frame, start=0)
        self.setup_grid_check_list(frame, start=2)

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

    def setup_grid_check_list(self, parent, start=0):
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

    def setup_grid_radio_del(self, parent, start=0):
        setup_delete_radio(parent, del_what_var=self.del_what_var, start=start)

    def setup_info_del(self, parent, start=0):
        info_claims(parent, start=start)

    def setup_textbox_del(self, parent):
        claims = set_up_default_claims(clean_up=True)
        self.textbox_del = setup_textbox(parent, font="monospace",
                                         tab_function=self.focus_next_widget)
        self.textbox_del.insert("1.0", claims)

    def del_claims(self):
        if not res.server_exists(server=self.server_var.get()):
            return False

        claims = self.resolve_claims(print_msg=False)
        actions.delete_claims(claims, what=self.del_what_var.get(),
                              server=self.server_var.get())
        print(40 * "-")
        print("Done")

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
        setup_grid_button_val_res(parent,
                                  validate_func=self.validate_ch,
                                  resolve_func=self.resolve_ch,
                                  start=start)

        _width = 26
        b_clean = ttk.Button(parent, text="Clean up claims",
                             width=_width,
                             command=self.delete_ch)
        b_clean.grid(row=start+2, column=0)
        lb = ttk.Label(parent,
                       text=("Start deleting claims "
                             "from the oldest to the newest"))
        lb.grid(row=start+2, column=1, sticky=tk.W, padx=2)

    def setup_grid_radio_delch(self, parent, start=0):
        setup_delete_radio(parent, del_what_var=self.del_what_var, start=start)

    def setup_info_delch(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Add a channel, a comma, "
                               "and the number of items to keep "
                               "from this channel; older items "
                               "will be removed"))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_delch(self, parent):
        channels = set_up_default_channels(clean_up=True)
        self.textbox_delch = setup_textbox(parent, font="monospace",
                                           tab_function=self.focus_next_widget)
        self.textbox_delch.insert("1.0", channels)

    def delete_ch(self):
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
    app = Application(root)

    them = ttk.Style()
    if "linux" in platform.system().lower():
        them.theme_use("clam")

    app.master.title("lbrydseed")
    app.mainloop()


if __name__ == "__main__":
    sys.exit(main())
