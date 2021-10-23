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
"""Auxiliary methods to parse input information of the graphical interface."""


def validate_input(text, assume_channel=True, number_float=False,
                   print_msg=False):
    """Validate the text entered."""
    lines = text.splitlines()

    claims = []
    numbers = []

    out = []
    num = 0

    for claim in lines:
        edited = False

        parts = claim.split(",")
        parts = [i.strip() for i in parts]

        claim_name = parts[0]
        try:
            number = parts[1]
        except IndexError:
            number = 2
            edited = True

        if " " in claim_name:
            claim_name = claim_name.replace(" ", "")
            edited = True
        if '"' in claim_name:
            claim_name = claim_name.replace('"', '')
            edited = True
        if "'" in claim_name:
            claim_name = claim_name.replace("'", "")
            edited = True

        if not claim_name:
            continue

        if not number:
            number = 2
            edited = True
        try:
            if number_float:
                number = round(float(number), 8)
            else:
                number = int(float(number))
        except ValueError:
            number = 2
            edited = True

        if assume_channel and not claim_name.startswith("@"):
            claim_name = "@" + claim_name

        num += 1
        name = f"'{claim_name}'"
        if edited:
            out += [f"{num:2d}: name={name:58s} number={number}  <-- edited"]
        else:
            out += [f"{num:2d}: name={name:58s} number={number}"]

        claims.append(claim_name)
        numbers.append(number)

    if print_msg:
        print("Validate input")
        print(80 * "-")
        print("\n".join(out))
    return claims, numbers
