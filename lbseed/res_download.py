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
import importlib
import requests
import tempfile

try:
    import lbrytools as lbryt
    external_lib = True
except ModuleNotFoundError:
    external_lib = False


def server_exists(server="http://localhost:5279"):
    """Return True if the server is up, and False if not."""
    try:
        requests.post(server)
    except requests.exceptions.ConnectionError:
        print(f"Cannot establish connection to 'lbrynet' on {server}")
        print("Start server with:")
        print("  lbrynet start")
        return False
    return True


def resolve_ch(channels, numbers, print_msg=True,
               server="http://localhost:5279"):
    """Resolve input channels to see if they in fact exist."""
    resolve_info = []
    out = []

    for num, group in enumerate(zip(channels, numbers), start=1):
        channel = group[0]
        number = group[1]

        msg = {"method": "resolve",
               "params": {"urls": channel}}
        output = requests.post(server, json=msg).json()

        if "error" in output:
            info = output["error"]
        else:
            item = output["result"][channel]

            if "error" in item:
                error = item["error"]
                if "name" in error:
                    info = "{} {}".format(error["name"], error["text"])
                else:
                    info = error
            else:
                info = item["canonical_url"]

        channel = f"'{channel}'"
        out += [f"{num:2d}: name={channel:35s} number={number}  {info}"]
        resolve_info.append(info)

    if print_msg:
        print("Resolve channels")
        print(80 * "-")
        print("\n".join(out))
    return resolve_info


def get_download_dir(server="http://localhost:5279"):
    msg = {"method": "settings_get"}
    out_set = requests.post(server, json=msg).json()
    ddir = out_set["result"]["download_dir"]
    return ddir


def download_ch(channels, numbers, info,
                ddir=None, own_dir=False, save_file=True,
                proceed=False,
                print_msg=True,
                server="http://localhost:5279"):
    """Download claims from channels."""
    if print_msg:
        print("Download claims")
        print(80 * "-")

    n_channels = len(channels)

    for num, group in enumerate(zip(channels, numbers, info), start=1):
        channel = group[0]
        number = group[1]
        information = group[2]

        if "NOT_FOUND" in information:
            continue
        if print_msg:
            print(f"Channel {num}/{n_channels}, '{information}'")
            if num < n_channels:
                print()
            msg = {"method": "getch",
                   "params": {"channel": channel,
                              "number": number,
                              "download_directory": ddir,
                              "save_file": True}}

            if proceed and not external_lib:
                print(f"lbrynet getch '{channel}' --number={number}")
                output = requests.post(server, json=msg).json()
            elif proceed and external_lib:
                output = lbryt.ch_download_latest(channel=channel,
                                                  number=number,
                                                  ddir=ddir, own_dir=own_dir,
                                                  save_file=save_file,
                                                  server=server)


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


def resolve_claims(text, print_msg=True,
                   server="http://localhost:5279"):
    """Resolve claims to see if they actually exist."""
    split_lines = text.splitlines()
    lines = []

    for line in split_lines:
        item = line.strip()
        if " " in item:
            item = item.replace(" ", "")
        if not item:
            continue
        lines.append(item)

    claims = []
    out = []

    for num, line in enumerate(lines, start=1):
        result = lbryt.search_item(line, print_error=False,
                                   server=server)

        info = ""
        if not result:
            result = lbryt.search_item(cid=line, print_error=False,
                                       server=server)

        if not result:
            info = "No claim found"

        line = f'"{line}"'
        out += [f'{num:2d}: item={line:42s}  {info}']
        claims.append(result)

    if print_msg:
        print("Resolve claims")
        print(80 * "-")
        print("\n".join(out))
    return claims

