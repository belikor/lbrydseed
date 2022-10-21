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
"""Methods to delete claims with the interface."""
import tempfile

import lbrytools as lbryt


def list_supports(show_ch=False,
                  show_claims=True,
                  show_cid=False,
                  show_combined=True,
                  show_invalid=False,
                  sanitize=True,
                  threads=32,
                  print_msg=True,
                  server="http://localhost:5279"):
    """List supports."""
    if print_msg:
        print("List all supported claims")
        print(80 * "-")

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        lbryt.list_supports(claim_id=show_cid,
                            invalid=show_invalid,
                            combine=show_combined,
                            claims=show_claims,
                            channels=show_ch,
                            sanitize=sanitize,
                            threads=threads,
                            file=fp.name, fdate=False, sep=";",
                            server=server)
        fp.seek(0)
        content = fp.read()
    return content


def add_supports(resolved_claims, support_style="create",
                 invalid=False,
                 threads=32,
                 print_msg=True,
                 server="http://localhost:5279"):
    """Add supports to the claims."""
    if print_msg:
        print("Add supports")
        print(80 * "-")

    n_claims = len(resolved_claims)

    if invalid:
        all_supports = lbryt.get_all_supports(threads=threads,
                                              server=server)
        invalids = all_supports['invalid_supports']

    for num, resolved_claim in enumerate(resolved_claims, start=1):
        number = resolved_claim["number"]

        if invalid:
            name = resolved_claim["claim"]
        else:
            claim = resolved_claim["resolved"]
            name = claim["name"]

        print(f"Claim {num}/{n_claims}, {name}")
        if support_style in ("create"):
            lbryt.create_support(cid=claim["claim_id"],
                                 amount=number,
                                 server=server)
        elif support_style in ("abandon_change"):
            if invalid:
                result = lbryt.abandon_support_inv(invalids=invalids,
                                                   cid=name,
                                                   keep=number,
                                                   threads=threads,
                                                   server=server)
                if not result:
                    lbryt.abandon_support_inv(invalids=invalids,
                                              name=name,
                                              keep=number,
                                              threads=threads,
                                              server=server)
            else:
                lbryt.abandon_support(cid=claim["claim_id"],
                                      keep=number,
                                      server=server)
        elif support_style in ("target"):
            lbryt.target_support(cid=claim["claim_id"],
                                 target=number,
                                 server=server)
        else:
            print(f"Wrong option: {support_style}")

        if num < n_claims:
            print()

    return support_style
