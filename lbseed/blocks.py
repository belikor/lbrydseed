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
from lbseed.blocks_base import focus_next_widget
from lbseed.blocks_base import f_with_event
from lbseed.blocks_base import set_up_default_channels
from lbseed.blocks_base import set_up_default_claims
from lbseed.blocks_base import setup_entry_gen
from lbseed.blocks_base import setup_button_gen
from lbseed.blocks_base import setup_spin_gen
from lbseed.blocks_base import setup_combo_gen
from lbseed.blocks_base import setup_listbox_gen
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

from lbseed.blocks_controlling import setup_check_contr
from lbseed.blocks_controlling import setup_check_contr_compact

from lbseed.blocks_supports import setup_check_support
from lbseed.blocks_supports import setup_radio_support

from lbseed.blocks_search import setup_check_trend_fields
from lbseed.blocks_search import setup_radio_trend_claims
from lbseed.blocks_search import setup_check_trend_typ
from lbseed.blocks_search import info_search

# Use the methods to prevent warnings by code checkers (flake8)
True if focus_next_widget else False
True if f_with_event else False
True if set_up_default_channels else False
True if set_up_default_claims else False
True if setup_entry_gen else False
True if setup_button_gen else False
True if setup_spin_gen else False
True if setup_combo_gen else False
True if setup_listbox_gen else False
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

True if setup_check_contr else False
True if setup_check_contr_compact else False

True if setup_check_support else False
True if setup_radio_support else False

True if setup_check_trend_fields else False
True if setup_radio_trend_claims else False
True if setup_check_trend_typ else False
True if info_search else False
