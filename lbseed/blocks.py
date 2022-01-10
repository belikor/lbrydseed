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


def setup_check_list(parent,
                     blocks_var=None,
                     cid_var=None,
                     blobs_var=None,
                     size_var=None,
                     show_ch_var=None,
                     start=0):
    """Setup the checkbuttons to list various properties."""
    chck_blks = ttk.Checkbutton(parent,
                                variable=blocks_var,
                                text="Show block height")
    chck_blks.grid(row=start, column=1, sticky=tk.W)

    chck_cid = ttk.Checkbutton(parent,
                               variable=cid_var,
                               text="Show claim ID (40-character string)")
    chck_cid.grid(row=start+1, column=1, sticky=tk.W)

    chck_blobs = ttk.Checkbutton(parent,
                                 variable=blobs_var,
                                 text=("Show number of blobs "
                                       "(each blob is 2 MB)"))
    chck_blobs.grid(row=start+2, column=1, sticky=tk.W)

    chck_size = ttk.Checkbutton(parent,
                                variable=size_var,
                                text=("Show length of claim (mm:ss) "
                                      "and total size (MB)"))
    chck_size.grid(row=start+3, column=1, sticky=tk.W)

    chck_ch = ttk.Checkbutton(parent,
                              variable=show_ch_var,
                              text="Show signing channel of the claim")
    chck_ch.grid(row=start+4, column=1, sticky=tk.W)


def setup_radio_list(parent,
                     name_var=None,
                     start=0):
    """Set up the radiobuttons to choose what to display as name."""
    name = ttk.Radiobutton(parent,
                           text="Show claim name",
                           variable=name_var, value="name")
    title = ttk.Radiobutton(parent,
                            text="Show claim title",
                            variable=name_var, value="title")
    path = ttk.Radiobutton(parent,
                           text="Show path of the existing media file",
                           variable=name_var, value="path")
    name.grid(row=start, column=1, sticky=tk.W)
    title.grid(row=start+1, column=1, sticky=tk.W)
    path.grid(row=start+2, column=1, sticky=tk.W)


def setup_check_ch_list(parent,
                        blocks_var=None,
                        cid_var=None,
                        type_var=None,
                        chname_var=None,
                        title_var=None,
                        reverse_var=None,
                        start=0):
    """Setup the checkbuttons to control displaying properties of claims."""
    chck_blocks = ttk.Checkbutton(parent,
                                  variable=blocks_var,
                                  text=("Show the creation block "
                                        "and block height of the claim"))
    chck_blocks.grid(row=start, column=1, sticky=tk.W)

    chck_cid = ttk.Checkbutton(parent,
                               variable=cid_var,
                               text="Show claim ID (40-character string)")
    chck_cid.grid(row=start+1, column=1, sticky=tk.W)

    chck_type = ttk.Checkbutton(parent,
                                variable=type_var,
                                text=("Show the type of claim, stream, "
                                      "and media, if available"))
    chck_type.grid(row=start+2, column=1, sticky=tk.W)

    chck_chname = ttk.Checkbutton(parent,
                                  variable=chname_var,
                                  text=("Show the name of the channel"))
    chck_chname.grid(row=start+3, column=1, sticky=tk.W)

    chck_chname = ttk.Checkbutton(parent,
                                  variable=title_var,
                                  text=("Show the claim 'title' "
                                        "instead of the claim 'name'"))
    chck_chname.grid(row=start+4, column=1, sticky=tk.W)

    chck_reverse = ttk.Checkbutton(parent,
                                   variable=reverse_var,
                                   text=("Show in descending order "
                                         "(newer items first, older last)"))
    chck_reverse.grid(row=start+5, column=1, sticky=tk.W)


def setup_check_support(parent,
                        show_ch_var=None,
                        show_claims_var=None,
                        show_cid_var=None,
                        show_invalid_var=None,
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

    chck_inv = ttk.Checkbutton(parent,
                               variable=show_invalid_var,
                               text="Only show 'invalid' claims")
    chck_inv.grid(row=start+4, column=1, sticky=tk.W)


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


def setup_spin_page(parent,
                    s_text_var=None,
                    s_command=None,
                    l_text="Label spin",
                    start=0):
    """Setup a generic spinbox to choose a page to search."""
    spin = ttk.Spinbox(parent,
                       from_=1.0, to=20.0, increment=1.0,
                       textvariable=s_text_var)
    spin.set("1")
    spin.grid(row=start, column=0, sticky=tk.W + tk.E)
    spin.bind("<<Activate>>", f_with_event(s_command))

    label = ttk.Label(parent, text=l_text)
    label.grid(row=start, column=1, sticky=tk.W, padx=2)

    return spin, label


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
                        support_inv_var=None,
                        support_inv_cmd=None,
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

    chck_inv = ttk.Checkbutton(parent,
                               variable=support_inv_var,
                               text=("Consider the claims as 'invalid'. "
                                     "Invalid claims no longer resolve "
                                     "online\n"
                                     "so their support "
                                     "should be removed or diminished.\n"
                                     "These are shown in the list "
                                     "of supports within '[brackets]'.\n"
                                     "In the textbox, write them "
                                     "without the brackets."),
                               command=support_inv_cmd)

    r_create.grid(row=start, column=1, sticky=tk.W, pady=4)
    r_abandon.grid(row=start+1, column=1, sticky=tk.W, pady=4)
    r_target.grid(row=start+2, column=1, sticky=tk.W, pady=4)
    chck_inv.grid(row=start+3, column=1, sticky=tk.W)

    return r_create, r_abandon, r_target


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


def info_claims(parent, start=0):
    """Setup instructions when dealing with individual claims."""
    info = ttk.Label(parent,
                     text=("Add one claim per row; this should be "
                           "a claim name or a claim ID "
                           "(40-character string)."))
    info.grid(row=start, column=0, columnspan=2, sticky=tk.W)


def info_search(parent, start=0):
    """Setup information for trending and search."""
    # unicode \u275A is a monospace black box
    info = ttk.Label(parent,
                     text=("The information shown will be "
                           "(1) the type of claim, "
                           "(2) the type of stream (downloadable), \n"
                           "(3) the media type (downloadable), "
                           "(4) the channel name (if available), "
                           "and (5) the name of the claim\n"
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
