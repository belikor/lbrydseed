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
"""Basic building blocks for the GUI that are used various times.

This contains basic methods for creating standard objects
with basic properties.
"""
import tkinter as tk
import tkinter.ttk as ttk


def focus_next_widget(event):
    """Callback to focus on next widget when pressing <Tab>."""
    event.widget.tk_focusNext().focus()
    return "break"


def f_with_event(function):
    """Decorate a function so that it accepts an event."""
    def function_with_event(event, **kwargs):
        function(**kwargs)
    return function_with_event


def set_up_default_channels(clean_up=False):
    """Block of text to populate a Text widget."""
    sep = ";"

    channels = ["@OdyseeHelp#b" + f"{sep}" + " 4",
                "@my-favorite-channel" + f"{sep}" + " 5",
                "@Odysee" + f"{sep}" + " 5",
                "@lbrytech" + f"{sep}" + " 3",
                "@ch-doesnt-exist" + f"{sep}" + " 2",
                "1487afc813124abbeb0629d2172be0f01ccec3bf"
                + f"{sep}" + " 2",
                "@lbry:3f" + f"{sep}" + " 6"]

    if clean_up:
        channels = ["@OdyseeHelp:b" + f"{sep}" + " 2",
                    "@lbrytech" + f"{sep}" + " 3",
                    "@my-favorite-channel" + f"{sep}" + " 15",
                    "@lbry#3f" + f"{sep}" + " 1",
                    "@Odysee" + f"{sep}" + " 2",
                    "1487afc813124abbeb0629d2172be0f01ccec3bf"
                    + f"{sep}" + " 0",
                    "@ch-doesnt-exist" + f"{sep}" + " 5"]

    channels = "\n".join(channels)
    return channels


def set_up_default_claims(clean_up=False):
    """Block of text to populate a Text widget."""
    claims = ["this-is-a-fake-claim",
              "livestream-tutorial:b",
              "abcd0000efgh0000ijkl0000mopq0000rstu0000",
              "blockchain-turns-5",
              "8e16d91185aa4f1cd797f93d7714de2a22622759",
              "LBRYPlaylists#d",
              "@lbrytech#19/ieee#e"]

    if clean_up:
        claims = ["abcd0000efgh0000ijkl0000mopq0000rstu0000",
                  "LBRYPlaylists#d",
                  "this-is-a-fake-claim",
                  "blockchain-turns-5",
                  "livestream-tutorial:b",
                  "8e16d91185aa4f1cd797f93d7714de2a22622759",
                  "@lbrytech#19/ieee#e"]

    claims = "\n".join(claims)
    return claims


def setup_entry_gen(parent,
                    font=None,
                    text_var=None,
                    l_text="Side text",
                    start=0):
    """Setup for a generic entry field with a label next to it."""
    entry = ttk.Entry(parent,
                      textvariable=text_var,
                      font=font)
    entry.grid(row=start, column=0, sticky=tk.W + tk.E)
    entry.bind("<<Activate>>", focus_next_widget)

    label = ttk.Label(parent, text=l_text)
    label.grid(row=start, column=1, sticky=tk.W, padx=2)

    return entry, label


def setup_button_gen(parent,
                     width=26,
                     b_text="Button text",
                     b_command=None,
                     l_text="Side text",
                     start=0):
    """Setup for a generic button with a label next to it."""
    button = ttk.Button(parent,
                        text=b_text,
                        width=width,
                        command=b_command)
    button.grid(row=start, column=0)
    button.bind("<<Activate>>", f_with_event(b_command))

    label = ttk.Label(parent, text=l_text)
    label.grid(row=start, column=1, sticky=tk.W, padx=2)

    return button, label


def setup_spin_gen(parent,
                   frm=1.0, to=20.0, incr=1.0,
                   default=1,
                   s_text_var=None,
                   s_command=None,
                   l_text="Label spin",
                   start=0):
    """Setup a generic spinbox to choose an integer, like a page."""
    spin = ttk.Spinbox(parent,
                       from_=frm, to=to, increment=incr,
                       textvariable=s_text_var)
    spin.set(default)
    spin.grid(row=start, column=0, sticky=tk.W + tk.E)
    spin.bind("<<Activate>>", f_with_event(s_command))

    label = ttk.Label(parent, text=l_text)
    label.grid(row=start, column=1, sticky=tk.W, padx=2)

    return spin, label


def setup_combo_gen(parent,
                    width=20,
                    variable=None,
                    def_list=None,
                    def_value=None,
                    l_text="Side text",
                    start=0):
    """Set up generic combobox with default list."""
    combo = ttk.Combobox(parent,
                         textvariable=variable,
                         width=width)
    combo.grid(row=start, column=0, sticky=tk.W + tk.E)
    combo["values"] = def_list
    combo.set(def_value)

    label = ttk.Label(parent, text=l_text)
    label.grid(row=start, column=1, sticky=tk.W, padx=2)

    return combo, label


def setup_listbox_gen(parent,
                      font="monospace",
                      width=70, height=12,
                      list_var=None):
    """Setup for listboxes, including scrollbars and Listbox widget."""
    hsrl = ttk.Scrollbar(parent, orient="horizontal")
    hsrl.pack(side=tk.BOTTOM, fill=tk.X)
    vsrl = ttk.Scrollbar(parent)
    vsrl.pack(side=tk.RIGHT, fill=tk.Y)

    lstbox = tk.Listbox(parent,
                        xscrollcommand=hsrl.set,
                        yscrollcommand=vsrl.set,
                        font=font,
                        width=width, height=height,
                        listvariable=list_var)

    lstbox.pack(side="top", fill="both", expand=True)

    hsrl.config(command=lstbox.xview)
    vsrl.config(command=lstbox.yview)
    return lstbox


def setup_textbox(parent,
                  font="monospace",
                  width=70, height=12):
    """Setup for the textboxes, including scrollbars and Text widget."""
    hsrl = ttk.Scrollbar(parent, orient="horizontal")
    hsrl.pack(side=tk.BOTTOM, fill=tk.X)
    vsrl = ttk.Scrollbar(parent)
    vsrl.pack(side=tk.RIGHT, fill=tk.Y)

    textbox = tk.Text(parent,
                      xscrollcommand=hsrl.set,
                      yscrollcommand=vsrl.set,
                      font=font,
                      width=width, height=height,
                      wrap=tk.NONE)
    textbox.bind("<Tab>", focus_next_widget)

    textbox.pack(side="top", fill="both", expand=True)

    hsrl.config(command=textbox.xview)
    vsrl.config(command=textbox.yview)
    return textbox
