#!/usr/bin/env python3
# --------------------------------------------------------------------------- #
# The MIT License (MIT)                                                       #
#                                                                             #
# Copyright (c) 2022 Eliud Cabrera Castillo <e.cabrera-castillo@tum.de>       #
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
"""Methods to list subscribed channels with the interface."""

import tempfile

import lbrytools as lbryt


def list_ch_subs(action="subscriptions",
                 number=4,
                 shared="shared",
                 show="show_all", filtering="valid",
                 notifications=True,
                 threads=32,
                 claim_id=False, title=False,
                 server="http://localhost:5279"):
    """Print all subscribed channels to a temporary file and read that file."""
    if shared in ("shared"):
        database = True
    elif shared in ("local"):
        database = False

    if show in ("show_all"):
        show_all = True
        valid = False
    elif show in ("show_valid"):
        show_all = False
        valid = True
    elif show in ("show_invalid"):
        show_all = False
        valid = False

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        if action in ("subscriptions"):
            lbryt.list_ch_subs(shared=database,
                               show_all=show_all, filtering="valid",
                               valid=valid, notifications=True,
                               threads=threads,
                               claim_id=claim_id,
                               file=fp.name, fdate=False, sep=";",
                               server=server)
        elif action in ("latest_claims"):
            lbryt.list_ch_subs_latest(number=number,
                                      claim_id=claim_id,
                                      typ=True, title=title,
                                      sanitize=True,
                                      shared=database,
                                      show_all=show_all, filtering="valid",
                                      valid=valid, notifications=True,
                                      threads=threads,
                                      start=1, end=0,
                                      file=fp.name, fdate=False, sep=";",
                                      server=server)
        fp.seek(0)
        content = fp.read()

    return content
