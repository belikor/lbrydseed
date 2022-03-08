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


def download_ch(channels, numbers, info,
                repost=True,
                ddir=None, own_dir=False, save_file=True,
                proceed=False,
                print_msg=True,
                server="http://localhost:5279"):
    """Download claims from channels."""
    if print_msg:
        print("Download claims from channels")
        print(80 * "-")

    n_channels = len(channels)

    for num, group in enumerate(zip(channels, numbers, info), start=1):
        channel = group[0]
        number = group[1]
        information = group[2]

        if "NOT_FOUND" in information or "not a valid url" in information:
            continue

        print(f"Channel {num}/{n_channels}, '{information}'")

        # msg = {"method": "getch",
        #        "params": {"channel": channel,
        #                   "number": number,
        #                   "download_directory": ddir,
        #                   "save_file": True}}

        # If the `getch` method is implemented
        # if proceed and not external_lib:
        #     print(f"lbrynet getch '{channel}' --number={number}")
        #     output = requests.post(server, json=msg).json()

        lbryt.ch_download_latest(channel=channel,
                                 number=number,
                                 repost=repost,
                                 ddir=ddir, own_dir=own_dir,
                                 save_file=save_file,
                                 server=server)
        if num < n_channels:
            print()


def download_claims(claims,
                    repost=True,
                    ddir=None, own_dir=False, save_file=True,
                    print_msg=True,
                    server="http://localhost:5279"):
    """Download individual claims."""
    if print_msg:
        print("Download claims")
        print(80 * "-")

    n_claims = len(claims)

    for num, claim in enumerate(claims, start=1):
        if not claim:
            continue

        name = claim["name"]
        print(f"Claim {num}/{n_claims}, {name}")
        lbryt.download_single(cid=claim["claim_id"],
                              repost=repost,
                              ddir=ddir, own_dir=own_dir,
                              save_file=save_file,
                              server=server)
        if num < n_claims:
            print()
