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


def list_peers(channel=None, number=2, threads=32,
               claim_id=False, typ=True, title=False,
               sanitize=True,
               server="http://localhost:5279"):
    """Print peers for claims into a temporary file and read that file."""
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        peers_info = lbryt.list_peers(channel=channel, number=number,
                                      threads=threads,
                                      print_msg=False,
                                      claim_id=claim_id, typ=typ, title=title,
                                      sanitize=sanitize,
                                      file=fp.name, fdate=False, sep=";",
                                      server=server)
        fp.seek(0)
        lines = fp.read()

    if peers_info["n_streams"] < 1:
        return {"lines": "No downloadable claims in this channel",
                "summary": ""}

    n_claims = peers_info["n_claims"]
    n_streams = peers_info["n_streams"]
    total_size = peers_info["total_size"]
    total_seconds = peers_info["total_duration"]
    streams_with_hosts = peers_info["streams_with_hosts"]
    total_peers = peers_info["total_peers"]
    n_nodes = len(peers_info["unique_nodes"])

    if peers_info["local_node"]:
        n_nodes = f"{n_nodes} + 1"

    peer_ratio = peers_info["peer_ratio"]
    hosting_coverage = peers_info["hosting_coverage"] * 100

    total_size_gb = total_size / (1024**3)
    days = (total_seconds / 3600) / 24
    hr = total_seconds // 3600
    mi = (total_seconds % 3600) // 60
    sec = (total_seconds % 3600) % 60
    duration = f"{hr} h {mi} min {sec} s, or {days:.4f} days"

    out = [f"Channel: {channel}",
           f"Claims searched: {n_claims}",
           f"Downloadable streams: {n_streams}",
           f"- Streams that have at least one host: {streams_with_hosts}",
           f"- Size of streams: {total_size_gb:.4f} GiB",
           f"- Duration of streams: {duration}",
           "",
           f"Total peers in all searched claims: {total_peers}",
           f"Total unique peers (nodes) hosting streams: {n_nodes}",
           f"Average number of peers per stream: {peer_ratio:.4f}",
           f"Hosting coverage: {hosting_coverage:.2f}%"]

    summary = "\n".join(out)

    return {"lines": lines,
            "summary": summary}
