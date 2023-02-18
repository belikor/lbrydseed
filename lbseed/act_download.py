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
"""Methods to download something with the interface."""
import lbrytools as lbryt


def i_download_chs(resolved_chs,
                   ddir=None, own_dir=False, save_file=True,
                   repost=True,
                   print_msg=True,
                   server="http://localhost:5279"):
    """Download claims from channels."""
    if print_msg:
        print("Download claims from channels")
        print(80 * "-")

    n_channels = len(resolved_chs)

    for num, resolved_ch in enumerate(resolved_chs, start=1):
        claim_input = resolved_ch["claim_input"]
        number = resolved_ch["number"]
        claim = resolved_ch["claim"]

        if not claim:
            info = claim_input[:]
        else:
            info = claim["canonical_url"]
            channel = claim["canonical_url"].split("lbry://")[1]

        if num > 1:
            print(80 * "-")

        print(f"Channel {num}/{n_channels}, {info}")

        if number > 0 and claim:
            lbryt.ch_download_latest(channel=channel,
                                     number=number,
                                     repost=repost,
                                     ddir=ddir, own_dir=own_dir,
                                     save_file=save_file,
                                     server=server)
        elif number == 0:
            print(f"number={number}, skipping channel")
        else:
            print("Not a valid channel, skipping")

        if num < n_channels:
            print()


def i_download_claims(resolved_claims,
                      ddir=None, own_dir=False, save_file=True,
                      repost=True,
                      print_msg=True,
                      server="http://localhost:5279"):
    """Download individual claims."""
    if print_msg:
        print("Download claims")
        print(80 * "-")

    n_claims = len(resolved_claims)

    for num, resolved_claim in enumerate(resolved_claims, start=1):
        claim_input = resolved_claim["claim_input"]
        claim = resolved_claim["claim"]

        if not claim:
            info = claim_input[:]
        else:
            info = claim["canonical_url"]

        print(f"Claim {num}/{n_claims}, {info}")

        if claim:
            lbryt.download_single(cid=claim["claim_id"],
                                  repost=repost,
                                  ddir=ddir, own_dir=own_dir,
                                  save_file=save_file,
                                  server=server)
        else:
            print("Not a valid claim, skipping")

        if num < n_claims:
            print()
