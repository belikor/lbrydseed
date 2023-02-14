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


def validate_input(text,
                   assume_channel=True, number_float=False,
                   print_msg=False,
                   sep=","):
    """Validate the text entered to get claims and numbers.

    The `text` has three parts, a claim input (name or claim ID), a separator,
    and then a number:
    ::
        @name, 12345
        some-claim, 333
        abcd0000efgh0000ijkl0000mopq0000rstu0000, 7.07
    """
    lines = text.splitlines()

    validated_claims = []

    out = []
    num = 0

    for line in lines:
        edited = False

        parts = line.split(sep)
        parts = [part.strip() for part in parts]

        claim_input = parts[0]

        try:
            number = parts[1]
        except IndexError:
            number = 2
            edited = True

        if " " in claim_input:
            claim_input = claim_input.replace(" ", "")
            edited = True

        if '"' in claim_input:
            claim_input = claim_input.replace('"', '')
            edited = True

        if assume_channel:
            if "'" in claim_input:
                claim_input = claim_input.replace("'", "")
                edited = True

        if not claim_input:
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

        if assume_channel and not claim_input.startswith("@"):
            claim_input = "@" + claim_input

        num += 1
        c_input = f'"{claim_input}"'

        if edited:
            out += [f"{num:2d}: input={c_input:58s} number={number}  "
                    "<-- edited"]
        else:
            out += [f"{num:2d}: input={c_input:58s} number={number}"]

        validated_claims.append({"claim_input": claim_input,
                                 "number": number})

    if print_msg:
        print("Validate input")
        print(80 * "-")
        print("\n".join(out))

    return validated_claims
