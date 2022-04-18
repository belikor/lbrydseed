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
"""Methods to list claims with the interface."""
import tempfile

import lbrytools as lbryt


def print_claims(blocks=False, cid=False, blobs=True, size=True,
                 show_channel=False,
                 show_out="name", channel=None,
                 invalid=False,
                 reverse=False,
                 server="http://localhost:5279"):
    """Print all downloaded claims to a temporary file and read that file."""
    if show_out in ("name"):
        name = True
        title = False
        path = False
    elif show_out in ("title"):
        name = False
        title = True
        path = False
    elif show_out in ("path"):
        name = False
        title = False
        path = True

    output = lbryt.sort_items_size(reverse=False, invalid=invalid,
                                   server=server)
    if not output:
        return False, 0, 0, 0

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        lbryt.print_items(output["claims"],
                          show="all",
                          blocks=blocks, cid=cid, blobs=blobs, size=size,
                          typ=False, ch=show_channel, ch_online=False,
                          name=name, title=title, path=path,
                          sanitize=True,
                          start=1, end=0, channel=channel,
                          reverse=reverse,
                          file=fp.name, fdate=False, sep=";",
                          server=server)
        fp.seek(0)
        content = fp.read()
    return content, len(output["claims"]), output["size"], output["duration"]


def print_ch_claims(channel,
                    number=0,
                    blocks=False, claim_id=False,
                    typ=False, ch_name=False,
                    title=False,
                    start=1, end=0,
                    reverse=False,
                    last_height=99_000_900,
                    server="http://localhost:5279"):
    """Print all or a certain number of claims for a specified channel."""
    if number:
        output = lbryt.ch_search_n_claims(channel,
                                          number=number,
                                          last_height=last_height,
                                          reverse=False,
                                          server=server)
    else:
        output = lbryt.ch_search_all_claims(channel,
                                            last_height=last_height,
                                            reverse=False,
                                            server=server)

    if not output:
        return False, 0, 0, 0

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        lbryt.print_sch_claims(output["claims"],
                               blocks=blocks, claim_id=claim_id,
                               typ=typ, ch_name=ch_name,
                               title=title, sanitize=True,
                               start=start, end=end,
                               reverse=reverse,
                               file=fp.name, fdate=False, sep=";")
        fp.seek(0)
        content = fp.read()
    return content, len(output["claims"]), output["size"], output["duration"]


def list_text_size(number, size, seconds):
    """Calculate size and duration of the claims."""
    size_gb = size/(1024**3)
    hrs = seconds / 3600
    days = hrs / 24

    hr = seconds // 3600
    mi = (seconds % 3600) // 60
    sec = (seconds % 3600) % 60

    text = (f"Claims: {number}; "
            f"total size: {size_gb:.4f} GB; "
            f"total duration: {hr} h {mi} min {sec} s, "
            f"or {days:.4f} days")

    return text


def list_pub_chs(wallet_id="default_wallet", is_spent=False,
                 updates=False, claim_id=False, addresses=True,
                 accounts=False, amounts=True,
                 reverse=False,
                 server="http://localhost:5279"):
    """Print all created channels in the wallet."""
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        output = lbryt.list_channels(wallet_id=wallet_id,
                                     is_spent=is_spent,
                                     updates=updates, claim_id=claim_id,
                                     addresses=addresses,
                                     accounts=accounts, amounts=amounts,
                                     reverse=reverse, sanitize=True,
                                     file=fp.name, fdate=False, sep=";",
                                     server=server)
        fp.seek(0)
        content = fp.read()

    n_claims = output["summary"]["n_claims"]
    t_base_amount = output["summary"]["base_amount"]
    total_amount = output["summary"]["total_amount"]

    out = [f"Total claims in channels: {n_claims}",
           f"Total base stake on all channels: {t_base_amount:14.8f}",
           f"Total stake on all channels:      {total_amount:14.8f}",
           80 * "-"]
    text = "\n".join(out)

    output = {"summary": text,
              "content": content,
              "channels": output["channels"]}

    return output
