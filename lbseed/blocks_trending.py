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
"""Basic building blocks for the GUI that are used in trending pages."""
import tkinter as tk
import tkinter.ttk as ttk


def setup_radio_trend_claims(parent,
                             claim_type_var=None,
                             activate_func=None,
                             deactivate_func=None,
                             start=0, col=1):
    """Setup the radiobuttons to determine what to search."""
    r_stream = ttk.Radiobutton(parent,
                               text=("Search stream claims "
                                     "(downloadable content)"),
                               variable=claim_type_var, value="stream",
                               command=activate_func)

    r_channel = ttk.Radiobutton(parent,
                                text=("Search channel claims"),
                                variable=claim_type_var, value="channel",
                                command=deactivate_func)

    r_repost = ttk.Radiobutton(parent,
                               text=("Search repost claims"),
                               variable=claim_type_var, value="repost",
                               command=activate_func)

    r_collect = ttk.Radiobutton(parent,
                                text=("Search collection claims (playlists)"),
                                variable=claim_type_var, value="collection",
                                command=deactivate_func)

    r_live = ttk.Radiobutton(parent,
                             text=("Search livestream claims "
                                   "(may not be live at the moment)"),
                             variable=claim_type_var, value="livestream",
                             command=deactivate_func)

    r_stream.grid(row=start, column=col, sticky=tk.W)
    r_channel.grid(row=start+1, column=col, sticky=tk.W)
    r_repost.grid(row=start+2, column=col, sticky=tk.W)
    r_collect.grid(row=start+3, column=col, sticky=tk.W)
    r_live.grid(row=start+4, column=col, sticky=tk.W)

    return r_stream, r_channel, r_repost, r_collect, r_live


def setup_check_trend(parent,
                      all_var=None,
                      all_command=None,
                      video_var=None,
                      audio_var=None,
                      doc_var=None,
                      image_var=None,
                      bin_var=None,
                      model_var=None,
                      not_all_command=None,
                      start=0, col=1):
    """Setup the checkbuttons for trending."""
    chck_all = ttk.Checkbutton(parent,
                               variable=all_var,
                               text=("All types of claims"),
                               command=all_command)
    chck_all.grid(row=start, column=col, sticky=tk.W)

    chck_vid = ttk.Checkbutton(parent,
                               variable=video_var,
                               text=("Search video streams"),
                               command=not_all_command)
    chck_vid.grid(row=start+1, column=col, sticky=tk.W)

    chck_audio = ttk.Checkbutton(parent,
                                 variable=audio_var,
                                 text=("Search audio streams"),
                                 command=not_all_command)
    chck_audio.grid(row=start+2, column=col, sticky=tk.W)

    chck_doc = ttk.Checkbutton(parent,
                               variable=doc_var,
                               text=("Search document streams"),
                               command=not_all_command)
    chck_doc.grid(row=start+3, column=col, sticky=tk.W)

    chck_img = ttk.Checkbutton(parent,
                               variable=image_var,
                               text=("Search image streams"),
                               command=not_all_command)
    chck_img.grid(row=start+4, column=col, sticky=tk.W)

    chck_bin = ttk.Checkbutton(parent,
                               variable=bin_var,
                               text=("Search binary streams"),
                               command=not_all_command)
    chck_bin.grid(row=start+5, column=col, sticky=tk.W)

    chck_model = ttk.Checkbutton(parent,
                                 variable=model_var,
                                 text=("Search model streams"),
                                 command=not_all_command)
    chck_model.grid(row=start+6, column=col, sticky=tk.W)

    return (chck_all,
            chck_vid, chck_audio, chck_doc, chck_img, chck_bin, chck_model)


def info_search(parent, start=0):
    """Setup information for trending and search."""
    # unicode \u275A is a monospace black box
    info = ttk.Label(parent,
                     text=("The information shown will be "
                           "(1) the type of claim, "
                           "(2) the type of stream (downloadable), \n"
                           "(3) the media type (downloadable), "
                           "(4) the channel name (if available), "
                           "(5) the fee for accessing\n"
                           "the claim, and (6) the name of the claim "
                           "(or the name of the channel "
                           "for channel claims).\n"
                           "\n"
                           "Many claims contain emojis and long unicode "
                           "'grapheme clusters';\n"
                           "to avoid problems with these symbols, they "
                           "are replaced by the symbol '\u275A'.\n"
                           "In order to download these claims "
                           "use their claim ID."))
    info.grid(row=start, column=0, columnspan=2, sticky=tk.W)
