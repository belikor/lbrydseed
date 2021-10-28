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


def setup_check_download(parent,
                         save_var=None,
                         own_dir_var=None,
                         enable_command=None,
                         start=0):
    """Setup for the checkbuttons to modify the download of claims."""
    chk_save = ttk.Checkbutton(parent,
                               variable=save_var,
                               text=("Save the media file "
                                     "(mp4, mkv, mp3, etc.), "
                                     "otherwise only the blobs "
                                     "will be downloaded.\n"
                                     "Only the blobs are necessary to seed "
                                     "the content."),
                               command=enable_command)
    chk_save.grid(row=start, column=1, sticky=tk.W)

    chk_owndir = ttk.Checkbutton(parent,
                                 variable=own_dir_var,
                                 text=("Place the media file "
                                       "inside a subdirectory named after "
                                       "the channel"))
    chk_owndir.grid(row=start+1, column=1, sticky=tk.W, pady=2)

    return chk_save, chk_owndir


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


def setup_check_controlling(parent,
                            contr_var=None,
                            non_contr_var=None,
                            skip_repost_var=None,
                            ch_only_var=None,
                            start=0):
    """Setup the checkbuttons to show controlling claims."""
    chck_contr = ttk.Checkbutton(parent,
                                 variable=contr_var,
                                 text=("Show controlling claims "
                                       "(highest bids)"))
    chck_contr.grid(row=start, column=1, sticky=tk.W)

    chck_non_contr = ttk.Checkbutton(parent,
                                     variable=non_contr_var,
                                     text=("Show non-controlling claims "
                                           "(lower bids)"))
    chck_non_contr.grid(row=start+1, column=1, sticky=tk.W)

    chck_repost = ttk.Checkbutton(parent,
                                  variable=skip_repost_var,
                                  text="Skip reposts")
    chck_repost.grid(row=start+2, column=1, sticky=tk.W)

    chck_channel = ttk.Checkbutton(parent,
                                   variable=ch_only_var,
                                   text="Only show channels")
    chck_channel.grid(row=start+3, column=1, sticky=tk.W)


def setup_check_contr_compact(parent,
                              compact_var=None,
                              compact_command=None,
                              cid_var=None,
                              is_repost_var=None,
                              n_competing_var=None,
                              n_reposts_var=None,
                              start=0):
    """Setup the checkbuttons that work only with the compact option."""
    chck_compact = ttk.Checkbutton(parent,
                                   variable=compact_var,
                                   text=("Compact information "
                                         "(one claim per row)"),
                                   command=compact_command)
    chck_compact.grid(row=start, column=1, sticky=tk.W)

    chck_claim_id = ttk.Checkbutton(parent,
                                    variable=cid_var,
                                    text="Show claim ID")
    chck_claim_id.grid(row=start+1, column=1, sticky=tk.W)

    chck_is_repost = ttk.Checkbutton(parent,
                                     variable=is_repost_var,
                                     text="Indicate if the claim is a repost")
    chck_is_repost.grid(row=start+2, column=1, sticky=tk.W)

    chck_competing = ttk.Checkbutton(parent,
                                     variable=n_competing_var,
                                     text=("Show how many competing claims "
                                           "there are with the same name"))
    chck_competing.grid(row=start+3, column=1, sticky=tk.W)

    chck_reposts = ttk.Checkbutton(parent,
                                   variable=n_reposts_var,
                                   text=("Show how many reposts "
                                         "there are of this claim"))
    chck_reposts.grid(row=start+4, column=1, sticky=tk.W)

    return chck_claim_id, chck_is_repost, chck_competing, chck_reposts


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


def setup_radio_support(parent,
                        support_how_var=None,
                        start=0):
    """Setup the radiobuttons to choose how to support claims."""
    r_create = ttk.Radiobutton(parent,
                               text=("Create a new support, regardless "
                                     "of previous supports.\n"
                                     "The number represets our support "
                                     "that will be created, and added\n"
                                     "to the 'existing' support. "
                                     "The number must be larger than 0.\n"
                                     "new_total = existing + ours\n"),
                               variable=support_how_var,
                               value="create")

    r_abandon = ttk.Radiobutton(parent,
                                text=("Abandon or change "
                                      "our support.\n"
                                      "The number represents our support "
                                      "that will be added to "
                                      "the 'base' support.\n"
                                      "If there is a previous support "
                                      "it will be discarded, and a new "
                                      "support will be made.\n"
                                      "If the number is 0, our previous "
                                      "support will be removed completely.\n"
                                      "old_total = base + ours_old\n"
                                      "new_total = base + ours_new\n"),
                                variable=support_how_var,
                                value="abandon_change")

    r_target = ttk.Radiobutton(parent,
                               text=("Target a specific total support.\n"
                                     "The number represents the final "
                                     "support that the claim should have.\n"
                                     "We will add support or reduce "
                                     "our support in order to reach "
                                     "the target.\n"
                                     "The target should be larger than "
                                     "the 'base' support, otherwise\n"
                                     "our existing support "
                                     "will be completely removed.\n"
                                     "old_total = base + ours_old\n"
                                     "target = base + ours_new\n"),
                               variable=support_how_var,
                               value="target")

    r_create.grid(row=start, column=1, sticky=tk.W, pady=4)
    r_abandon.grid(row=start+1, column=1, sticky=tk.W, pady=4)
    r_target.grid(row=start+2, column=1, sticky=tk.W, pady=4)


def info_claims(parent, start=0):
    """Setup instructions when dealing with individual claims."""
    info = ttk.Label(parent,
                     text=("Add one claim per row; this should be "
                           "a claim name or a claim ID "
                           "(40-character string)."))
    info.grid(row=start, column=0, columnspan=2, sticky=tk.W)


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
