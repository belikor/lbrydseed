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
"""Basic building blocks that are used in downloading and deletion pages."""
import tkinter as tk
import tkinter.ttk as ttk


def setup_check_download(parent,
                         repost_var=None,
                         own_dir_var=None,
                         save_var=None,
                         enable_command=None,
                         start=0):
    """Setup for the checkbuttons to modify the download of claims."""
    chk_repost = ttk.Checkbutton(parent,
                                 variable=repost_var,
                                 text=("Download the original claims "
                                       "if the claims are reposts,\n"
                                       "otherwise skip them"))
    chk_repost.grid(row=start, column=1, sticky=tk.W, pady=2)

    chk_save = ttk.Checkbutton(parent,
                               variable=save_var,
                               text=("Save the media file "
                                     "(mp4, mkv, mp3, etc.), "
                                     "otherwise only the blobs "
                                     "will be downloaded.\n"
                                     "Only the blobs are necessary to seed "
                                     "the content."),
                               command=enable_command)
    chk_save.grid(row=start+1, column=1, sticky=tk.W, pady=2)

    chk_owndir = ttk.Checkbutton(parent,
                                 variable=own_dir_var,
                                 text=("Place the media file "
                                       "inside a subdirectory named after "
                                       "the channel"))
    chk_owndir.grid(row=start+2, column=1, sticky=tk.W, pady=2)

    return chk_save, chk_owndir


def setup_radio_delete(parent,
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


def info_claims(parent, start=0):
    """Setup instructions when dealing with individual claims."""
    info = ttk.Label(parent,
                     text=("Add one claim per row; this should be "
                           "a claim name or a claim ID "
                           "(40-character string)."))
    info.grid(row=start, column=0, columnspan=2, sticky=tk.W)
