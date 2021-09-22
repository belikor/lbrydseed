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


def validate_input(text, print_msg=False):
    """Validate the text entered."""
    lines = text.splitlines()
 
    channels = []
    numbers = []
 
    out = []
    num = 0
 
    for ch in lines:
        edited = False
 
        parts = ch.split(",")
        parts = [i.strip() for i in parts]
 
        ch_name = parts[0]
        try:
            number= parts[1]
        except IndexError:
            number = 2
            edited = True
 
        if " " in ch_name:
            ch_name = ch_name.replace(" ", "")
            edited = True
        if '"' in ch_name:
            ch_name = ch_name.replace('"', '')
            edited = True
        if "'" in ch_name:
            ch_name = ch_name.replace("'", "")
            edited = True
 
        if not ch_name:
            continue
 
        if not number:
            number = 2
            edited = True
        try:
            number = int(float(number))
        except ValueError:
            number = 2
            edited = True 
 
        if not ch_name.startswith("@"):
            ch_name = "@" + ch_name
 
        num += 1
        channel = f"'{ch_name}'"
        if edited:
            out += [f"{num:2d}: name={channel:35s} number={number}  <-- edited"]
        else:
            out += [f"{num:2d}: name={channel:35s} number={number}"]
 
        channels.append(ch_name)
        numbers.append(number)
 
    if print_msg:
        print("Validate input")
        print(80 * "-")
        print("\n".join(out))
    return channels, numbers

