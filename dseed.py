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

import lbseed.res_download as rs
import lbseed.validate as vd


class Application(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_widgets(parent)

    def setup_widgets(self, parent):
        self.ftmono = tk.font.Font(family="monospace", size=10)
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
        self.down_dir_var.set(rs.get_download_dir(server=self.server_var.get()))

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

        if not rs.server_exists(server=self.server_var.get()):
            return False

        ddir = self.down_dir_var.get()
        if not os.path.exists(ddir):
            nddir = rs.get_download_dir(server=self.server_var.get())
            self.down_dir_var.set(nddir)
            print(f"Directory does not exist: {ddir}")
            print(f"Default directory: {nddir}")

        info = rs.resolve_ch(channels, numbers, print_msg=print_msg,
                             server=self.server_var.get())
        return channels, numbers, info

    def start_download(self):
        if not rs.server_exists(server=self.server_var.get()):
            return False

        channels, numbers, info = self.resolve(print_msg=False)
        rs.download_ch(channels, numbers, info,
                       ddir=self.down_dir_var.get(),
                       own_dir=self.own_dir_var.get(),
                       save_file=self.save_var.get(),
                       proceed=True,
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

