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
"""Methods to search claims with the interface."""
import tempfile

import lbrytools as lbryt


def list_trending(threads=32,
                  page=0,
                  release=False, claim_id=False, title=False,
                  claim_type=None,
                  video_stream=False, audio_stream=False,
                  doc_stream=False, img_stream=False,
                  bin_stream=False, model_stream=False,
                  sanitize=True,
                  server="http://localhost:5279"):
    """Print trending claims in the network with different options."""
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        claims_info = \
            lbryt.list_trending_claims(threads=threads,
                                       page=page,
                                       trending="trending_mixed",
                                       release=release,
                                       claim_id=claim_id,
                                       title=title,
                                       claim_type=claim_type,
                                       video_stream=video_stream,
                                       audio_stream=audio_stream,
                                       doc_stream=doc_stream,
                                       img_stream=img_stream,
                                       bin_stream=bin_stream,
                                       model_stream=model_stream,
                                       sanitize=sanitize,
                                       file=fp.name, fdate=False, sep=";",
                                       server=server)
        fp.seek(0)
        lines = fp.read()

    summary = claims_info["summary"]
    searched = claims_info["searched"]

    return {"summary": summary,
            "searched": searched,
            "lines": lines}


def list_search(threads=32,
                page=0,
                text="lbry",
                tags=None,
                release=False, claim_id=False, title=False,
                claim_type=None,
                video_stream=False, audio_stream=False,
                doc_stream=False, img_stream=False,
                bin_stream=False, model_stream=False,
                sanitize=True,
                server="http://localhost:5279"):
    """Print the result of the claim search in the network."""
    if tags:
        tags = tags.split(",")
        tags = [tag.strip() for tag in tags]
    else:
        tags = []

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        claims_info = \
            lbryt.list_search_claims(threads=threads,
                                     page=page,
                                     order="release_time",
                                     text=text,
                                     tags=tags,
                                     release=release,
                                     claim_id=claim_id,
                                     title=title,
                                     claim_type=claim_type,
                                     video_stream=video_stream,
                                     audio_stream=audio_stream,
                                     doc_stream=doc_stream,
                                     img_stream=img_stream,
                                     bin_stream=bin_stream,
                                     model_stream=model_stream,
                                     sanitize=sanitize,
                                     file=fp.name, fdate=False, sep=";",
                                     server=server)
        fp.seek(0)
        lines = fp.read()

    summary = claims_info["summary"]
    searched = claims_info["searched"]

    return {"summary": summary,
            "searched": searched,
            "lines": lines}
