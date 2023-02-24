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
import requests

import lbrytools as lbryt


def i_resolve_ch(validated_chs,
                 print_msg=True,
                 server="http://localhost:5279"):
    """Resolve input channels to see if they in fact exist."""
    resolved_chs = []
    out = []

    for num, validated_ch in enumerate(validated_chs, start=1):
        channel = validated_ch["claim"]
        number = validated_ch["number"]

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

        chan = f"'{channel}'"

        if number is None:
            out += [f"{num:2d}: name={chan:58s}  {info}"]
        else:
            out += [f"{num:2d}: name={chan:58s} number={number}  {info}"]

        resolved_chs.append({"claim": channel,
                             "number": number,
                             "info": info})

    if print_msg:
        print("Resolve channels")
        print(80 * "-")
        print("\n".join(out))

    return resolved_chs


def i_resolve_claims(text,
                     repost=True,
                     print_msg=True,
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

    resolved_claims = []
    out = []

    for num, line in enumerate(lines, start=1):
        result = lbryt.search_item(uri=line, repost=repost,
                                   print_error=False,
                                   server=server)

        if not result:
            result = lbryt.search_item(cid=line, repost=repost,
                                       print_error=False,
                                       server=server)

        if not result:
            info = "<-- claim not found"
        else:
            info = result["canonical_url"]

        line = f'"{line}"'
        out += [f'{num:2d}: item={line:58s}  {info}']
        resolved_claims.append(result)

    if print_msg:
        print("Resolve claims")
        print(80 * "-")
        print("\n".join(out))

    return resolved_claims


def i_resolve_claims_supp(validated_claims,
                          show_support=False,
                          print_msg=True,
                          sep=";",
                          server="http://localhost:5279"):
    """Resolve claims to see if they actually exist and return a new vector."""
    resolved_claims = []
    out = []

    for num, validated_claim in enumerate(validated_claims, start=1):
        claim = validated_claim["claim"]
        number = validated_claim["number"]

        result = lbryt.search_item(claim, print_error=False,
                                   server=server)

        if not result:
            result = lbryt.search_item(cid=claim, print_error=False,
                                       server=server)

        if not result:
            info = "<-- claim not found"
        else:
            info = result["canonical_url"]

            resolved_claims.append({"claim": claim,
                                    "number": number,
                                    "resolved": result})

            if show_support:
                supp = lbryt.get_base_support(info)

                existing = supp["existing_support"]
                base = supp["base_support"]
                old = supp["old_support"]

                info += (f" {sep} "
                         f"curr: {existing:.8f}{sep} "
                         f"base: {base:.8f}{sep} "
                         f"old: {old:.8f}")

        claim = f'"{claim}"'

        out += [f'{num:2d}: item={claim:58s}  {info}']

    if print_msg:
        print("Resolve claims")
        print(80 * "-")
        print("\n".join(out))

    return resolved_claims
