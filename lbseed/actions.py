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
"""Methods to actually do something with the interface."""
from lbseed.act_cfg import i_list_lbrynet_settings
from lbseed.act_cfg import i_list_lbrynet_status

from lbseed.act_download import i_download_chs
from lbseed.act_download import i_download_claims

from lbseed.act_list import i_list_d_claims
from lbseed.act_list import i_list_ch_claims
from lbseed.act_list import i_list_ch_subs
from lbseed.act_list import i_list_pub_chs
from lbseed.act_list import i_list_pub_claims
from lbseed.act_list import i_ctrl_claims

from lbseed.act_comments import i_list_comments
from lbseed.act_comments import i_show_comment
from lbseed.act_comments import i_show_no_comment
from lbseed.act_comments import i_act_comment

from lbseed.act_peers import i_list_m_peers
from lbseed.act_peers import i_list_ch_peers
from lbseed.act_peers import i_list_chs_peers
from lbseed.act_peers import i_list_subs_peers
from lbseed.act_peers import i_seeding_ratio

from lbseed.act_delete import i_delete_claims
from lbseed.act_delete import i_delete_chs

from lbseed.act_supports import i_list_supports
from lbseed.act_supports import i_update_supports

from lbseed.act_search import i_list_trending
from lbseed.act_search import i_list_search

True if i_list_lbrynet_settings else False
True if i_list_lbrynet_status else False

True if i_download_chs else False
True if i_download_claims else False

True if i_list_d_claims else False
True if i_list_ch_claims else False
True if i_list_ch_subs else False
True if i_list_pub_chs else False
True if i_list_pub_claims else False
True if i_ctrl_claims else False

True if i_list_comments else False
True if i_show_comment else False
True if i_show_no_comment else False
True if i_act_comment else False

True if i_list_m_peers else False
True if i_list_ch_peers else False
True if i_list_chs_peers else False
True if i_list_subs_peers else False
True if i_seeding_ratio else False

True if i_delete_claims else False
True if i_delete_chs else False

True if i_list_supports else False
True if i_update_supports else False

True if i_list_trending else False
True if i_list_search else False
