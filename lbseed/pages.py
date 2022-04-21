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
"""Mixin classes that add the different pages to the main graphical interface.

These classes should not be instantiatied directly. They are just used
in a multiple inheritance, or mixin pattern, to provide the necessary
building command to build the specific page in the main interface.

::
    class DownloadSinglePage:
        def setup_page_dch(self, parent):
            ...

    class Application(ttk.Frame, DownloadSinglePage):
        def __init__(self, root):
            page_dch = ttk.Frame(root)
            self.setup_page_dch(page_dch)
"""
from lbseed.pages_base import SettingsPage, StatusPage
from lbseed.pages_down import DownloadChPage, DownloadSinglePage
from lbseed.pages_lists import (ListDownPage, ListDownInvalidPage,
                                ListChClaimsPage, SubscribedChsPage)
from lbseed.pages_peers import (ListChPeersPage, ListChsPeersPage,
                                ListSubsPeersPage)
from lbseed.pages_del import DeleteSinglePage, DeleteChPage
from lbseed.pages_support import SupportListPage, SupportAddPage
from lbseed.pages_search import TrendPage, SearchPage
from lbseed.pages_adv import SeedPage, ControllingClaimsPage


# Use the classes to prevent warnings by code checkers (flake8)
True if SettingsPage else False
True if StatusPage else False

True if DownloadChPage else False
True if DownloadSinglePage else False

True if ListDownPage else False
True if ListDownInvalidPage else False
True if ListChClaimsPage else False
True if SubscribedChsPage else False

True if ListChPeersPage else False
True if ListChsPeersPage else False
True if ListSubsPeersPage else False

True if DeleteSinglePage else False
True if DeleteChPage else False

True if SupportListPage else False
True if SupportAddPage else False

True if TrendPage else False
True if SearchPage else False

True if SeedPage else False
True if ControllingClaimsPage else False
