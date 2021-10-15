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
"""Methods to resolve and download claims of channels."""
import tempfile

try:
    import lbrytools as lbryt
    external_lib = True
except ModuleNotFoundError:
    external_lib = False


def download_ch(channels, numbers, info,
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
                                 ddir=ddir, own_dir=own_dir,
                                 save_file=save_file,
                                 server=server)
        if num < n_channels:
            print()


def download_claims(claims,
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
        print(f"Claim {num}/{n_claims}, '{name}'")
        lbryt.download_single(cid=claim["claim_id"],
                              ddir=ddir, own_dir=own_dir,
                              save_file=save_file,
                              server=server)
        if num < n_claims:
            print()


def print_claims(cid=True, blobs=True, show_channel=False,
                 name=True, channel=None,
                 server="http://localhost:5279"):
    """Print all downloaded claims to a temporary file and read that file."""
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        lbryt.print_summary(show="all",
                            title=False, typ=False, path=False,
                            cid=cid, blobs=blobs, ch=show_channel,
                            ch_online=False,
                            name=name,
                            start=1, end=0, channel=channel, invalid=False,
                            file=fp.name, fdate=False, sep=";",
                            server=server)
        fp.seek(0)
        content = fp.read()
    return content


def delete_claims(claims, what="media",
                  print_msg=True,
                  server="http://localhost:5279"):
    """Delete individual claims."""
    if print_msg:
        print("Delete claims")
        print(80 * "-")

    n_claims = len(claims)

    for num, claim in enumerate(claims, start=1):
        if not claim:
            continue

        name = claim["name"]
        print(f"Claim {num}/{n_claims}, '{name}'")
        lbryt.delete_single(cid=claim["claim_id"],
                            what=what,
                            server=server)
        if num < n_claims:
            print()


def clean_ch(channels, numbers, info,
             what="media",
             print_msg=True,
             server="http://localhost:5279"):
    """Delete claims from channels."""
    if print_msg:
        print("Delete claims from channels")
        print(80 * "-")

    n_channels = len(channels)

    for num, group in enumerate(zip(channels, numbers, info), start=1):
        channel = group[0]
        number = group[1]
        information = group[2]

        if "NOT_FOUND" in information or "not a valid url" in information:
            continue

        print(f"Channel {num}/{n_channels}, '{information}'")
        lbryt.ch_cleanup(channel=channel,
                         number=number,
                         what=what,
                         server=server)
        if num < n_channels:
            print()


def list_supports(show_ch_var=False,
                  show_claims_var=True,
                  show_cid_var=False,
                  combine_var=True,
                  print_msg=True,
                  server="http://localhost:5279"):
    """List supports."""
    if print_msg:
        print("List all supported claims")
        print(80 * "-")

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        lbryt.list_supports(claim_id=show_cid_var,
                            combine=combine_var,
                            claims=show_claims_var,
                            channels=show_ch_var,
                            file=fp.name, fdate=False, sep=";",
                            server=server)
        fp.seek(0)
        content = fp.read()
    return content


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
