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
"""Other methods with the interface."""
import tempfile

import lbrytools as lbryt


def seeding_ratio(frame=None, plot_hst_var=True,
                  server="http://localhost:5279"):
    """List seeding ratio estimate."""
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        lbryt.print_blobs_ratio(data_dir=None,
                                plot_hst=plot_hst_var,
                                file=fp.name, fdate=False, sep=";",
                                tk_frame=frame,
                                server=server)
        fp.seek(0)
        content = fp.read()

    return content


def ctrl_claims(show_contr=False,
                show_non_contr=True,
                skip_repost=False,
                channels_only=False,
                show_claim_id=False,
                show_repost_st=True,
                show_competing=True,
                show_reposts=True,
                compact=False,
                server="http://localhost:5279"):
    """List the claims that we have and share a name with others.

    See if we have the controlling claim with the highest bid.
    """
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        lbryt.claims_bids(show_controlling=show_contr,
                          show_non_controlling=show_non_contr,
                          skip_repost=skip_repost,
                          channels_only=channels_only,
                          show_claim_id=show_claim_id,
                          show_repost_status=show_repost_st,
                          show_competing=show_competing,
                          show_reposts=show_reposts,
                          compact=compact,
                          file=fp.name, fdate=False, sep=";",
                          server=server)
        fp.seek(0)
        content = fp.read()

    return content
