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


def list_d_claims(blocks=False, cid=False, blobs=True, size=True,
                  show_channel=False,
                  show_out="name", channel=None,
                  invalid=False,
                  reverse=False,
                  threads=32,
                  sanitize=True,
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

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        claims_info = \
            lbryt.print_summary(show="all",
                                blocks=blocks, cid=cid, blobs=blobs,
                                size=size,
                                typ=False, ch=show_channel,
                                ch_online=False,
                                name=name, title=title, path=path,
                                sanitize=sanitize,
                                start=1, end=0, channel=channel,
                                invalid=invalid,
                                reverse=reverse,
                                threads=threads,
                                file=fp.name, fdate=False, sep=";",
                                server=server)
        fp.seek(0)
        lines = fp.read()

    summary = claims_info["summary"]

    return {"summary": summary,
            "lines": lines}


def list_ch_claims(channel,
                   number=0,
                   blocks=False, claim_id=False,
                   typ=False, ch_name=False,
                   title=False,
                   start=1, end=0,
                   sanitize=True,
                   reverse=False,
                   last_height=99_000_900,
                   server="http://localhost:5279"):
    """Print all or a certain number of claims for a specified channel."""
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        claims_info = \
            lbryt.list_ch_claims(channel,
                                 number=number,
                                 blocks=blocks, claim_id=claim_id,
                                 typ=typ, ch_name=ch_name,
                                 title=title,
                                 start=start, end=end,
                                 sanitize=sanitize,
                                 reverse=reverse,
                                 last_height=last_height,
                                 file=fp.name, fdate=False, sep=";",
                                 server=server)
        fp.seek(0)
        lines = fp.read()

    summary = claims_info["summary"]

    return {"summary": summary,
            "lines": lines}


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
            lbryt.list_ch_subs_latest(number=number, override=False,
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


def list_pub_claims(wallet_id="default_wallet", is_spent=False,
                    select=None,
                    updates=False, claim_id=False, addresses=False,
                    typ=False, amounts=True,
                    title=False,
                    reverse=False,
                    server="http://localhost:5279"):
    """Print created claims in the wallet."""
    if select in ("All", "Anonymous"):
        if select in "All":
            channel = None
            channel_id = None
            anon = False
        elif select in "Anonymous":
            channel = None
            channel_id = None
            anon = True
    else:
        channel = select
        channel_id = None
        anon = False

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        output = lbryt.list_claims(wallet_id=wallet_id,
                                   is_spent=is_spent,
                                   channel=channel, channel_id=channel_id,
                                   anon=anon,
                                   updates=updates, claim_id=claim_id,
                                   addresses=addresses,
                                   typ=typ, amounts=amounts, ch_name=False,
                                   title=title,
                                   reverse=reverse, sanitize=True,
                                   file=fp.name, fdate=False, sep=";",
                                   server=server)
        fp.seek(0)
        content = fp.read()

    n_chs = output["summary"]["n_channels"]
    t_n_claims = output["summary"]["n_ch_claims"]
    t_GB = output["summary"]["chs_size"]
    t_hr = output["summary"]["chs_hr"]
    t_mi = output["summary"]["chs_min"]
    t_sec = output["summary"]["chs_sec"]
    t_days = output["summary"]["chs_days"]
    t_n_anon_claims = output["summary"]["n_anon_claims"]
    t_anon_GB = output["summary"]["anon_size"]
    t_anon_hr = output["summary"]["anon_hr"]
    t_anon_mi = output["summary"]["anon_min"]
    t_anon_sec = output["summary"]["anon_sec"]
    t_anon_days = output["summary"]["anon_days"]

    out1 = [f"Total unique channels: {n_chs}",
            f"Total claims in channels: {t_n_claims}",
            f"Total download size: {t_GB:.4f} GiB",
            f"Total duration: {t_hr} h {t_mi} min {t_sec} s, "
            f"or {t_days:.4f} days"]

    out2 = [f"Anonymous unique claims: {t_n_anon_claims}",
            f"Total download size of anonymous claims: {t_anon_GB:.4f} GiB",
            "Total duration of anonymous claims: "
            f"{t_anon_hr} h {t_anon_mi} min {t_anon_sec} s, "
            f"or {t_anon_days:.4f} days"]

    out = []

    if t_n_claims > 0:
        out += out1

        if t_n_anon_claims > 0:
            out += [40 * "-"]

    if t_n_anon_claims > 0:
        out += out2

    if out:
        out += [80 * "-"]

    text = "\n".join(out)

    output = {"summary": text,
              "content": content,
              "ch_claims": output["ch_claims"]}

    return output


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
