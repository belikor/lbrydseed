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


class Application(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_widgets(parent)

    def setup_widgets(self, parent):
        self.ftmono = tk.font.Font(family="monospace", size=10)
        note = ttk.Notebook(parent)
        page1 = ttk.Frame(note)
        page2 = ttk.Frame(note)
        page3 = ttk.Frame(note)
        note.add(page1, text="Download")
        note.add(page2, text="List")
        note.add(page3, text="Delete")
        self.setup_page1(page1)
        self.setup_page2(page2)
        self.setup_page3(page3)
        note.pack()

    def setup_page1(self, parent):
        self.setup_top(parent)
        self.setup_textbox(parent)

    def setup_top(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top(frame, start=0)
        self.setup_grid_low(frame, start=2)
        self.setup_info(frame, start=7)

    def setup_grid_top(self, parent, start=0):
        self.server_var = tk.StringVar()
        self.server_var.set("http://localhost:5279")

        entry = ttk.Entry(parent, textvariable=self.server_var,
                          font=self.ftmono)
        entry.grid(row=start, column=0, sticky=tk.W + tk.E)
        le = ttk.Label(parent,
                       text=("Address of the 'lbrynet' daemon. "
                             "It defaults to localhost:5279"))
        le.grid(row=start, column=1, sticky=tk.W, padx=2)

        self.down_dir_var = tk.StringVar()
        self.down_dir_var.set(res.get_download_dir(server=self.server_var.get()))

        entry_dir = ttk.Entry(parent, textvariable=self.down_dir_var,
                              font=self.ftmono)
        entry_dir.grid(row=start+1, column=0, sticky=tk.W + tk.E)
        ledir = ttk.Label(parent,
                          text=("Download directory. "
                                "It defaults to your home directory."))
        ledir.grid(row=start+1, column=1, sticky=tk.W, padx=2)

    def setup_grid_low(self, parent, start=0):
        _width = 26
        b_validate = ttk.Button(parent, text="Validate input",
                                width=_width,
                                command=self.validate)
        b_validate.grid(row=start, column=0)
        b_validate.focus()
        lv = ttk.Label(parent,
                       text="Verify that the input can be read correctly")
        lv.grid(row=start, column=1, sticky=tk.W, padx=2)

        b_resolve = ttk.Button(parent, text="Resolve online",
                               width=_width,
                               command=self.resolve)
        b_resolve.grid(row=start+1, column=0)
        lr = ttk.Label(parent,
                       text="Confirm that the channels exist")
        lr.grid(row=start+1, column=1, sticky=tk.W, padx=2)

        b_download = ttk.Button(parent, text="Download claims",
                                width=_width,
                                command=self.start_download)
        b_download.grid(row=start+2, column=0)
        lr = ttk.Label(parent,
                       text=("Start downloading the newest claims "
                             "from the channels"))
        lr.grid(row=start+2, column=1, sticky=tk.W, padx=2)

        self.own_dir_var = tk.BooleanVar()
        self.own_dir_var.set(True)
        chk_owndir = ttk.Checkbutton(parent,
                                     variable=self.own_dir_var,
                                     text=("Place the downloaded file "
                                           "inside a subdirectory"))
        chk_owndir.grid(row=start+3, column=1, sticky=tk.W)

        self.save_var = tk.BooleanVar()
        self.save_var.set(True)
        chk_save = ttk.Checkbutton(parent,
                                   variable=self.save_var,
                                   text=("Save media and its blobs; "
                                         "otherwise only the first blob"))
        chk_save.grid(row=start+4, column=1, sticky=tk.W)

    def setup_info(self, parent, start):
        info = ttk.Label(parent,
                         text=("Add a channel, a comma, "
                               "and the number of items to download "
                               "from this channel"))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox(self, parent):
        hsrl = ttk.Scrollbar(parent, orient="horizontal")
        hsrl.pack(side=tk.BOTTOM, fill=tk.X)
        vsrl = ttk.Scrollbar(parent)
        vsrl.pack(side=tk.RIGHT, fill=tk.Y)

        self.textbox = tk.Text(parent,
                               xscrollcommand=hsrl.set,
                               yscrollcommand=vsrl.set,
                               font="monospace",
                               width=60, height=10,
                               wrap=tk.NONE)
        self.textbox.bind("<Tab>", self.focus_next_widget)

        self.textbox.pack(side="top", fill="both", expand=True)

        hsrl.config(command=self.textbox.xview)
        vsrl.config(command=self.textbox.yview)

        channels = ["@my-favorite-channel, 5",
                    "@OdyseeHelp#b, 2",
                    "@lbry:3f, 4"]
        channels = "\n".join(channels)

        self.textbox.insert("1.0", channels)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def validate(self, print_msg=True):
        text = self.textbox.get("1.0", tk.END)
        channels, numbers = vd.validate_input(text, print_msg=print_msg)
        return channels, numbers

    def resolve(self, print_msg=True):
        channels, numbers = self.validate(print_msg=False)

        if not res.server_exists(server=self.server_var.get()):
            return False

        ddir = self.down_dir_var.get()
        if not os.path.exists(ddir):
            nddir = res.get_download_dir(server=self.server_var.get())
            self.down_dir_var.set(nddir)
            print(f"Directory does not exist: {ddir}")
            print(f"Default directory: {nddir}")

        info = res.resolve_ch(channels, numbers, print_msg=print_msg,
                              server=self.server_var.get())
        return channels, numbers, info

    def start_download(self):
        if not res.server_exists(server=self.server_var.get()):
            return False

        channels, numbers, info = self.resolve(print_msg=False)
        actions.download_ch(channels, numbers, info,
                            ddir=self.down_dir_var.get(),
                            own_dir=self.own_dir_var.get(),
                            save_file=self.save_var.get(),
                            proceed=True,
                            server=self.server_var.get())

        print(40 * "-")
        print("Done")

    def setup_page2(self, parent):
        self.setup_top2(parent)
        self.setup_textbox2(parent)

    def setup_top2(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top2(frame, start=0)
        self.setup_grid_low2(frame, start=3)

    def setup_grid_top2(self, parent, start=0):
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

    def setup_grid_low2(self, parent, start=0):
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

    def setup_textbox2(self, parent):
        hsrl2 = ttk.Scrollbar(parent, orient="horizontal")
        hsrl2.pack(side=tk.BOTTOM, fill=tk.X)
        vsrl2 = ttk.Scrollbar(parent)
        vsrl2.pack(side=tk.RIGHT, fill=tk.Y)

        self.textbox2 = tk.Text(parent,
                                xscrollcommand=hsrl2.set,
                                yscrollcommand=vsrl2.set,
                                font="monospace 8",
                                width=60, height=10,
                                wrap=tk.NONE)
        self.textbox2.bind("<Tab>", self.focus_next_widget)

        self.textbox2.pack(side="top", fill="both", expand=True)

        hsrl2.config(command=self.textbox2.xview)
        vsrl2.config(command=self.textbox2.yview)

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

        self.textbox2.replace("1.0", tk.END, content)
        print(40 * "-")
        print("Done")

    def setup_page3(self, parent):
        self.setup_top3(parent)
        self.setup_textbox3(parent)
        
    def setup_top3(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top3(frame, start=0)
        self.setup_grid_low3(frame, start=2)
        self.setup_info3(frame, start=5)

    def setup_grid_top3(self, parent, start=0):
        _width = 26
        b_resolve3 = ttk.Button(parent, text="Resolve online",
                                width=_width,
                                command=self.resolve_claims)
        b_resolve3.grid(row=start, column=0)
        lr3 = ttk.Label(parent,
                        text="Confirm that the claims exist")
        lr3.grid(row=start, column=1, sticky=tk.W, padx=2)

        b_del = ttk.Button(parent, text="Delete claims", 
                           width=_width, 
                           command=self.del_claims)
        b_del.grid(row=start+1, column=0)
        ldel = ttk.Label(parent,
                         text="Delete locally downloaded claims")
        ldel.grid(row=start+1, column=1, sticky=tk.W, padx=2)

    def setup_grid_low3(self, parent, start=0):
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

    def setup_info3(self, parent, start=0):
        info = ttk.Label(parent,
                         text=("Add one claim per row; this should be "
                               "a 'claim_name' or a 'claim_id' "
                               "(40-character string)"))
        info.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox3(self, parent):
        hsrl3 = ttk.Scrollbar(parent, orient="horizontal")
        hsrl3.pack(side=tk.BOTTOM, fill=tk.X)
        vsrl3 = ttk.Scrollbar(parent)
        vsrl3.pack(side=tk.RIGHT, fill=tk.Y)

        self.textbox3 = tk.Text(parent,
                                xscrollcommand=hsrl3.set,
                                yscrollcommand=vsrl3.set,
                                font="monospace",
                                width=60, height=10,
                                wrap=tk.NONE)
        self.textbox3.bind("<Tab>", self.focus_next_widget)

        self.textbox3.pack(side="top", fill="both", expand=True)

        hsrl3.config(command=self.textbox3.xview)
        vsrl3.config(command=self.textbox3.yview)

        claims = ["some-claim-name",
                  "this-is-a-fake-claim",
                  "abcd0000efgh0000ijkl0000mopq0000rstu0000"]
        claims = "\n".join(claims)

        self.textbox3.insert("1.0", claims)

    def resolve_claims(self, print_msg=True):
        if not res.server_exists(server=self.server_var.get()):
            return False

        text = self.textbox3.get("1.0", tk.END)
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

