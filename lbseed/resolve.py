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
"""Methods to resolve claims and channels."""
import os
import requests

import lbrytools as lbryt


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


def get_download_dir(server="http://localhost:5279"):
    msg = {"method": "settings_get"}
    out_set = requests.post(server, json=msg).json()
    ddir = out_set["result"]["download_dir"]
    return ddir


def check_download_dir(ddir=None, server="http://localhost:5279"):
    old_ddir = str(ddir)
    if not os.path.exists(ddir):
        ddir = get_download_dir(server=server)
        print(f"Directory does not exist: {old_ddir}")
        print(f"Default directory: {ddir}")
    return ddir


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
        out += [f"{num:2d}: name={channel:58s} number={number}  {info}"]
        resolve_info.append(info)

    if print_msg:
        print("Resolve channels")
        print(80 * "-")
        print("\n".join(out))
    return resolve_info


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

        if not result:
            result = lbryt.search_item(cid=line, print_error=False,
                                       server=server)

        if not result:
            info = "<-- claim not found"
        else:
            info = result["canonical_url"]

        line = f'"{line}"'
        out += [f'{num:2d}: item={line:58s}  {info}']
        claims.append(result)

    if print_msg:
        print("Resolve claims")
        print(80 * "-")
        print("\n".join(out))
    return claims
