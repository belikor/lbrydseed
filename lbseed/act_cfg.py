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
"""Methods to show settings and status of the lbrynet daemon."""
import tempfile

import lbrytools as lbryt


def list_lbrynet_settings(server="http://localhost:5279"):
    """Get the settings for the lbrynet daemon."""
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        output = lbryt.list_lbrynet_settings(file=fp.name, fdate=False,
                                             server=server)

        fp.seek(0)
        content = fp.read()

    if not output:
        content = "(no settings)"

    return content


def list_lbrynet_status(server="http://localhost:5279"):
    """Get lbrynet status."""
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        output = lbryt.list_lbrynet_status(file=fp.name, fdate=False,
                                           server=server)

        fp.seek(0)
        content = fp.read()

    if not output:
        content = "(no status)"

    return content
