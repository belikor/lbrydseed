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

from lbseed.blocks_base import focus_next_widget
from lbseed.blocks_base import f_with_event
from lbseed.blocks_base import set_up_default_channels
from lbseed.blocks_base import set_up_default_claims
from lbseed.blocks_base import setup_entry_gen
from lbseed.blocks_base import setup_button_gen
from lbseed.blocks_base import setup_spin_gen
from lbseed.blocks_base import setup_combo_gen
from lbseed.blocks_base import setup_textbox

from lbseed.blocks_down_del import setup_check_download
from lbseed.blocks_down_del import setup_radio_delete
from lbseed.blocks_down_del import info_claims

from lbseed.blocks_list import setup_check_list
from lbseed.blocks_list import setup_radio_list
from lbseed.blocks_list import setup_check_ch_list

from lbseed.blocks_subscribed import setup_radio_ch_subs_shared
from lbseed.blocks_subscribed import setup_radio_ch_subs_valid
from lbseed.blocks_subscribed import setup_radio_ch_subs_valid2

from lbseed.blocks_claims import setup_check_chs_claims
from lbseed.blocks_claims import setup_check_claims

from lbseed.blocks_supports import setup_check_support
from lbseed.blocks_supports import setup_radio_support

True if focus_next_widget else False
True if f_with_event else False
True if set_up_default_channels else False
True if set_up_default_claims else False
True if setup_entry_gen else False
True if setup_button_gen else False
True if setup_spin_gen else False
True if setup_combo_gen else False
True if setup_textbox else False

True if setup_check_download else False
True if setup_radio_delete else False
True if info_claims else False

True if setup_check_list else False
True if setup_radio_list else False
True if setup_check_ch_list else False

True if setup_radio_ch_subs_shared else False
True if setup_radio_ch_subs_valid else False
True if setup_radio_ch_subs_valid2 else False

True if setup_check_chs_claims else False
True if setup_check_claims else False

True if setup_check_support else False
True if setup_radio_support else False


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
