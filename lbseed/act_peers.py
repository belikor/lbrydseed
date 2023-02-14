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
"""Methods to find peers for claims with the interface."""
import tempfile

import lbrytools as lbryt


def i_list_m_peers(resolved_claims,
                   threads=32,
                   claim_id=False, typ=True, title=False,
                   pars=False, sanitize=True,
                   server="http://localhost:5279"):
    """Print peers for claims into a temporary file and read that file."""
    in_claims = []

    for resolved_claim in resolved_claims:
        if not resolved_claim:
            continue

        in_claims.append(resolved_claim)

    if not in_claims:
        return {"summary": "Invalid list of claims",
                "lines": "At least one claim must exist"}

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        peers_info = lbryt.list_m_peers(claims=in_claims,
                                        resolve=False,
                                        threads=threads, inline=not pars,
                                        print_msg=False,
                                        claim_id=claim_id, typ=typ,
                                        title=title,
                                        sanitize=sanitize,
                                        file=fp.name, fdate=False, sep=";",
                                        server=server)
        fp.seek(0)
        lines = fp.read()

    summary = peers_info["summary"]

    return {"summary": summary,
            "lines": lines}


def i_list_ch_peers(channel, number=2, threads=32,
                    claim_id=False, typ=True, title=False,
                    pars=False, sanitize=True,
                    server="http://localhost:5279"):
    """Print peers for claims into a temporary file and read that file."""
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        peers_info = lbryt.list_ch_peers(channel=channel, number=number,
                                         threads=threads, inline=not pars,
                                         print_msg=False,
                                         claim_id=claim_id, typ=typ,
                                         title=title,
                                         sanitize=sanitize,
                                         file=fp.name, fdate=False, sep=";",
                                         server=server)
        fp.seek(0)
        lines = fp.read()

    summary = peers_info["summary"]

    return {"summary": summary,
            "lines": lines}


def i_list_chs_peers(resolved_chs,
                     ch_threads=8, cl_threads=32,
                     server="http://localhost:5279"):
    """Print peers for claims into a temporary file and read that file."""
    in_channels = []

    for resolved_ch in resolved_chs:
        # claim_input = resolved_ch["claim_input"]
        number = resolved_ch["number"]
        claim = resolved_ch["claim"]

        if not claim:
            continue

        channel = claim["canonical_url"].split("lbry://")[1]

        in_channels.append([channel, number])

    if not in_channels:
        return {"summary": "Invalid list of channels",
                "lines": "At least one channel must exist"}

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        ch_peers_info = lbryt.list_chs_peers(channels=in_channels,
                                             number=None, shuffle=False,
                                             ch_threads=ch_threads,
                                             claim_threads=cl_threads,
                                             file=fp.name, fdate=False,
                                             sep=";",
                                             server=server)
        fp.seek(0)
        lines = fp.read()

        summary = ch_peers_info["summary"]

    return {"summary": summary,
            "lines": lines}


def i_list_subs_peers(number=2,
                      shared="shared", show="show_all",
                      ch_thrs=32, c_thrs=16,
                      server="http://localhost:5279"):
    """Print peers for claims from subscribed channels."""
    if shared in ("shared"):
        database = True
    elif shared in ("local"):
        database = False

    if show in ("show_valid"):
        valid = True
    elif show in ("show_all"):
        valid = False

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        ch_peers_info = lbryt.list_ch_subs_peers(number=number, shuffle=False,
                                                 start=1, end=0,
                                                 shared=database, valid=valid,
                                                 ch_threads=ch_thrs,
                                                 claim_threads=c_thrs,
                                                 file=fp.name, fdate=False,
                                                 sep=";",
                                                 server=server)
        fp.seek(0)
        lines = fp.read()

        summary = ch_peers_info["summary"]

    return {"summary": summary,
            "lines": lines}


def i_seeding_ratio(frame=None, plot_hst_var=True,
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
