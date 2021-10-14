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
"""Building blocks for the GUI that are used various times.

Instead of repeating this code in the main application class,
these functions allow us to save on typing, and make changes quickly
in a single plce.
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
    """Block of text to populate a Text widget."""
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


def setup_download_entry(parent,
                         dir_var=None,
                         font=None, start=0):
    """Setup for an entry field with a download directory."""
    entry_dir = ttk.Entry(parent, textvariable=dir_var,
                          font=font)
    entry_dir.grid(row=start, column=0, sticky=tk.W + tk.E)
    entry_dir.bind("<<Activate>>", focus_next_widget)

    ledir = ttk.Label(parent,
                      text=("Download directory. "
                            "It defaults to your home directory."))
    ledir.grid(row=start, column=1, sticky=tk.W, padx=2)


def setup_buttons_val_res(parent,
                          width=26,
                          validate_func=None,
                          resolve_func=None,
                          start=0):
    """Setup for buttons for validating and resolving channels."""
    b_validate = ttk.Button(parent, text="Validate input",
                            width=width,
                            command=validate_func)
    b_validate.grid(row=start, column=0)
    b_validate.bind("<<Activate>>",
                    f_with_event(validate_func))
    b_validate.focus()

    lv = ttk.Label(parent,
                   text="Verify that the input can be read correctly")
    lv.grid(row=start, column=1, sticky=tk.W, padx=2)

    b_resolve = ttk.Button(parent, text="Resolve online",
                           width=width,
                           command=resolve_func)
    b_resolve.grid(row=start+1, column=0)
    b_resolve.bind("<<Activate>>",
                   f_with_event(resolve_func))

    lr = ttk.Label(parent,
                   text="Confirm that the channels exist")
    lr.grid(row=start+1, column=1, sticky=tk.W, padx=2)


def setup_button_resolve_claims(parent,
                                width=26,
                                resolve_func=None,
                                start=0):
    """Setup for buttons for resolving claims."""
    b_resolve = ttk.Button(parent, text="Resolve online",
                           width=width,
                           command=resolve_func)
    b_resolve.grid(row=start, column=0)
    b_resolve.bind("<<Activate>>",
                   f_with_event(resolve_func))

    lr = ttk.Label(parent,
                   text="Confirm that the claims exist")
    lr.grid(row=start, column=1, sticky=tk.W, padx=2)


def setup_download_check(parent,
                         own_dir_var=None,
                         save_var=None,
                         start=0):
    """Setup for the checkbuttons to modify the download of claims."""
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
    """Setup instructions when dealing with individual claims."""
    info = ttk.Label(parent,
                     text=("Add one claim per row; this should be "
                           "a 'claim_name' or a 'claim_id' "
                           "(40-character string)"))
    info.grid(row=start, column=0, columnspan=2, sticky=tk.W)


def setup_check_list(parent,
                     cid_var=None,
                     blobs_var=None,
                     show_ch_var=None,
                     name_var=None,
                     start=0):
    """Setup the checkbuttons to list various properties."""
    chck_cid = ttk.Checkbutton(parent,
                               variable=cid_var,
                               text="Show 'claim_id'")
    chck_cid.grid(row=start, column=1, sticky=tk.W)

    chck_blobs = ttk.Checkbutton(parent,
                                 variable=blobs_var,
                                 text="Show number of blobs")
    chck_blobs.grid(row=start+1, column=1, sticky=tk.W)

    chck_ch = ttk.Checkbutton(parent,
                              variable=show_ch_var,
                              text="Show channel of the claim")
    chck_ch.grid(row=start+2, column=1, sticky=tk.W)

    chck_name = ttk.Checkbutton(parent,
                                variable=name_var,
                                text="Show 'claim_name'")
    chck_name.grid(row=start+3, column=1, sticky=tk.W)


def setup_delete_radio(parent,
                       del_what_var=None,
                       start=0):
    """Setup the radiobuttons to choose how to delete claims."""
    media = ttk.Radiobutton(parent,
                            text=("Delete media "
                                  "(keep seeding the claim)"),
                            variable=del_what_var, value="media")
    blobs = ttk.Radiobutton(parent,
                            text=("Delete blobs "
                                  "(keep media in download directory)"),
                            variable=del_what_var, value="blobs")
    both = ttk.Radiobutton(parent,
                           text=("Delete both "
                                 "(completely remove the claim)"),
                           variable=del_what_var, value="both")
    media.grid(row=start, column=1, sticky=tk.W)
    blobs.grid(row=start+1, column=1, sticky=tk.W)
    both.grid(row=start+2, column=1, sticky=tk.W)


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


def setup_check_support(parent,
                        show_ch_var=None,
                        show_claims_var=None,
                        show_cid_var=None,
                        combine_var=None,
                        start=0):
    """Setup the checkbuttons to list supports."""
    chck_ch = ttk.Checkbutton(parent,
                              variable=show_ch_var,
                              text="Show channel claims")
    chck_ch.grid(row=start, column=1, sticky=tk.W)

    chck_claims = ttk.Checkbutton(parent,
                                  variable=show_claims_var,
                                  text=("Show stream claims "
                                        "(video, audio, document, etc.)"))
    chck_claims.grid(row=start+1, column=1, sticky=tk.W)

    chck_cid = ttk.Checkbutton(parent,
                               variable=show_cid_var,
                               text="Show claim ID")
    chck_cid.grid(row=start+2, column=1, sticky=tk.W)

    chck_combine = ttk.Checkbutton(parent,
                                   variable=combine_var,
                                   text="Show combined trending score")
    chck_combine.grid(row=start+3, column=1, sticky=tk.W)
