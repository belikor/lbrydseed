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
"""Methods to actually do something with the interface."""
import tempfile

import lbrytools as lbryt


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
        print(f"Claim {num}/{n_claims}, {name}")
        lbryt.download_single(cid=claim["claim_id"],
                              ddir=ddir, own_dir=own_dir,
                              save_file=save_file,
                              server=server)
        if num < n_claims:
            print()


def print_claims(blocks=False, cid=False, blobs=True, size=True,
                 show_channel=False,
                 show_out="name", channel=None,
                 invalid=False,
                 server="http://localhost:5279"):
    """Print all downloaded claims to a temporary file and read that file."""
    if show_out in ("name"):
        name = True
        title = False
        path = False
    elif show_out in ("title"):
        name = False
        title = True
        path = False
    elif show_out in ("path"):
        name = False
        title = False
        path = True

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        lbryt.print_summary(show="all",
                            blocks=blocks, cid=cid, blobs=blobs, size=size,
                            typ=False, ch=show_channel, ch_online=False,
                            name=name, title=title, path=path,
                            sanitize=True,
                            start=1, end=0, channel=channel, invalid=invalid,
                            file=fp.name, fdate=False, sep=";",
                            server=server)
        fp.seek(0)
        content = fp.read()
    return content


def print_ch_claims(channel,
                    number=0,
                    blocks=False, claim_id=False,
                    typ=False, ch_name=False,
                    title=False,
                    start=1, end=0,
                    reverse=False,
                    last_height=99_000_900,
                    server="http://localhost:5279"):
    """Print all or a certain number of claims for a specified channel."""
    if number:
        output = lbryt.ch_search_n_claims(channel,
                                          number=number,
                                          last_height=last_height,
                                          reverse=False,
                                          server=server)
    else:
        output = lbryt.ch_search_all_claims(channel,
                                            last_height=last_height,
                                            reverse=False,
                                            server=server)

    if not output:
        return False

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        content = lbryt.print_sch_claims(output["claims"],
                                         blocks=blocks, claim_id=claim_id,
                                         typ=typ, ch_name=ch_name,
                                         title=title, sanitize=True,
                                         start=start, end=end,
                                         reverse=reverse,
                                         file=fp.name, fdate=False, sep=";")
        fp.seek(0)
        content = fp.read()
    return content, len(output["claims"]), output["total_size"]


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
        print(f"Claim {num}/{n_claims}, {name}")
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


def show_claims_bids(show_controlling=False,
                     show_non_controlling=True,
                     skip_repost=False,
                     channels_only=False,
                     show_claim_id=False,
                     show_repost_status=True,
                     show_competing=True,
                     show_reposts=True,
                     compact=False,
                     server="http://localhost:5279"):
    """List the claims that we have and share a name with others.

    See if we have the controlling claim with the highest bid.
    """
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        lbryt.claims_bids(show_controlling=show_controlling,
                          show_non_controlling=show_non_controlling,
                          skip_repost=skip_repost,
                          channels_only=channels_only,
                          show_claim_id=show_claim_id,
                          show_repost_status=show_repost_status,
                          show_competing=show_competing,
                          show_reposts=show_reposts,
                          compact=compact,
                          file=fp.name, fdate=False, sep=";",
                          server=server)
        fp.seek(0)
        content = fp.read()

    return content


def add_supports(claims, supports, support_style="create",
                 print_msg=True,
                 server="http://localhost:5279"):
    """Add supports to the claims."""
    if print_msg:
        print("Add supports")
        print(80 * "-")

    n_claims = len(claims)

    for num, pair in enumerate(zip(claims, supports), start=1):
        claim = pair[0]
        number = pair[1]
        name = claim["name"]

        print(f"Claim {num}/{n_claims}, {name}")
        if support_style in ("create"):
            lbryt.create_support(cid=claim["claim_id"],
                                 amount=number,
                                 server=server)
        elif support_style in ("abandon_change"):
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


def print_trending(page=1,
                   claim_id=False,
                   claim_type=None,
                   video_stream=False,
                   audio_stream=False,
                   doc_stream=False,
                   img_stream=False,
                   bin_stream=False,
                   model_stream=False,
                   server="http://localhost:5279"):
    """Print trending claims in the network with different options."""
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        lbryt.print_trending_claims(page=page,
                                    trending="trending_mixed",
                                    claim_id=claim_id,
                                    claim_type=claim_type,
                                    video_stream=video_stream,
                                    audio_stream=audio_stream,
                                    doc_stream=doc_stream,
                                    img_stream=img_stream,
                                    bin_stream=bin_stream,
                                    model_stream=model_stream,
                                    sanitize=True,
                                    file=fp.name, fdate=False, sep=";",
                                    server=server)
        fp.seek(0)
        content = fp.read()

    return content


def return_search(page=1,
                  text="lbry",
                  tags=None,
                  claim_id=False,
                  claim_type=None,
                  video_stream=False, audio_stream=False,
                  doc_stream=False, img_stream=False,
                  bin_stream=False, model_stream=False,
                  server="http://localhost:5279"):
    """Print the result of the claim search in the network."""
    if tags:
        tags = tags.split(",")
        tags = [tag.strip() for tag in tags]
    else:
        tags = []

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        lbryt.print_search_claims(page=page,
                                  order="release_time",
                                  text=text,
                                  tags=tags,
                                  claim_id=claim_id,
                                  claim_type=claim_type,
                                  video_stream=video_stream,
                                  audio_stream=audio_stream,
                                  doc_stream=doc_stream,
                                  img_stream=img_stream,
                                  bin_stream=bin_stream,
                                  model_stream=model_stream,
                                  sanitize=True,
                                  file=fp.name, fdate=False, sep=";",
                                  server=server)
        fp.seek(0)
        content = fp.read()

    return content
