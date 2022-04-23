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

from lbseed.blocks_trending import setup_radio_trend_claims
from lbseed.blocks_trending import setup_check_trend
from lbseed.blocks_trending import info_search

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

True if setup_radio_trend_claims else False
True if setup_check_trend else False
True if info_search else False


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
