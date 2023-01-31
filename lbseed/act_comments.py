#!/usr/bin/env python3
# --------------------------------------------------------------------------- #
# The MIT License (MIT)                                                       #
#                                                                             #
# Copyright (c) 2022 Eliud Cabrera Castillo <e.cabrera-castillo@tum.de>       #
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
"""Methods to list claims with the interface."""
import tempfile
import time

import lbrytools as lbryt
import lbrytools.funcs as funcs


def get_r_list(comments, cmnt_info=None, indent=0, sanitize=False):
    """Put all comments in a flat list so we can get the comments quickly."""
    if not cmnt_info:
        cmnt_info = []

    n_base = len(comments)
    indentation = indent * " "

    for num, comment in enumerate(comments, start=1):
        ch = comment.get("channel_url", "lbry://_Unknown_#000")
        ch = ch.lstrip("lbry://").split("#")
        ch_name = ch[0] + "#" + ch[1][0:3]

        if sanitize:
            ch_name = lbryt.sanitize_text(ch_name)

        comm_id = comment["comment_id"]
        comm = comment["comment"]

        if sanitize:
            comm = lbryt.sanitize_text(comm)

        comm = comm.splitlines()
        if len(comm) > 0:
            comm = comm[0]
        else:
            comm = ""

        if len(comm) > 80:
            cmmnt = f'"{comm:.80s}..."'
        else:
            cmmnt = f'"{comm}"'

        line = (f"{indentation}"
                f"{num:2d}/{n_base:2d}; {ch_name:30s}; {cmmnt}; "
                f"{comm_id}")
        cmnt_info.append({"line": line,
                          "data": comment})

        if ("replies" in comment and "sub_replies" in comment
                and comment["sub_replies"]):
            get_r_list(comment["sub_replies"], indent=indent+2,
                       sanitize=sanitize, cmnt_info=cmnt_info)

    return cmnt_info


def list_comments(claim=None,
                  comm_server="https://comments.odysee.com/api/v2",
                  server="http://localhost:5279"):
    """Get all comments from a specific claim."""
    cid = claim["claim_id"]

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        output = lbryt.list_comments(uri=None, cid=cid, name=None,
                                     sub_replies=True,
                                     hidden=False, visible=False,
                                     full=False,
                                     file=fp.name, fdate=False,
                                     page=1, page_size=999,
                                     sanitize=True,
                                     comm_server=comm_server,
                                     server=server)
        fp.seek(0)
        content = fp.read()

    lines = []
    comments = []

    if output:
        cmnt_info = []
        cmnt_info = get_r_list(output["root_comments"],
                               cmnt_info=cmnt_info, indent=0, sanitize=True)

        lines = [info["line"] for info in cmnt_info]
        comments = [info["data"] for info in cmnt_info]
    else:
        output["root_comments"] = []
        output["replies"] = []

    text = ("Total comments: " + str(len(comments)) + "; "
            "root comments: " + str(len(output["root_comments"])) + "; "
            "replies: " + str(len(output["replies"])))

    return {"claim": claim,
            "lines": lines,
            "comments": comments,
            "content": content,
            "text": text}


def show_comment(cmnt_data, sanitize=True):
    """Get the output of a single comment."""
    index = cmnt_data["index"] + 1

    claim_uri = cmnt_data["claim"]["canonical_url"]

    if "release_time" in cmnt_data["claim"]["value"]:
        claim_time = int(cmnt_data["claim"]["value"]["release_time"])
    else:
        claim_time = cmnt_data["claim"]["meta"]["creation_timestamp"]

    claim_time = time.strftime(funcs.TFMT, time.gmtime(claim_time))

    claim_title = cmnt_data["claim"]["value"].get("title", "(None)")

    cmt_time = cmnt_data["timestamp"]
    cmt_time = time.strftime(funcs.TFMT, time.gmtime(cmt_time))

    sig_ts = int(cmnt_data["signing_ts"])
    sig_ts = time.strftime(funcs.TFMT, time.gmtime(sig_ts))

    cmnt_author = cmnt_data["channel_name"]

    comment = cmnt_data["comment"]

    if sanitize:
        claim_uri = lbryt.sanitize_text(claim_uri)
        claim_title = lbryt.sanitize_text(claim_title)
        cmnt_author = lbryt.sanitize_text(cmnt_author)
        comment = lbryt.sanitize_text(comment)

    out = ["canonical_url: " + claim_uri,
           "claim_id: " + cmnt_data["claim"]["claim_id"],
           "release_time: " + claim_time,
           "title: " + claim_title,
           80 * "-",
           f"{index}",
           "timestamp:  " + cmt_time,
           "signing_ts: " + sig_ts,
           "comment author: " + cmnt_author,
           "comment author ID: " + cmnt_data["channel_id"],
           "comment_id: " + cmnt_data["comment_id"],
           "parent_id:  " + cmnt_data.get("parent_id", "(None)"),
           "currency: " + cmnt_data.get("currency", "(None)"),
           "support_amount: " + str(cmnt_data.get("support_amount", 0)),
           "is_fiat: " + str(cmnt_data.get("is_fiat", "")),
           "is_hidden: " + str(cmnt_data.get("is_hidden", "")),
           "is_pinned: " + str(cmnt_data.get("is_pinned", "")),
           "abandoned: " + str(cmnt_data.get("abandoned", "")),
           80 * "-",
           comment]

    content = "\n".join(out)

    return content


def show_no_comment(claim, sanitize=True):
    """Get basic output when the claim has no comments."""
    claim_uri = claim["canonical_url"]

    if "release_time" in claim["value"]:
        claim_time = int(claim["value"]["release_time"])
    else:
        claim_time = claim["meta"]["creation_timestamp"]

    claim_time = time.strftime(funcs.TFMT, time.gmtime(claim_time))

    claim_title = claim["value"].get("title", "(None)")

    if sanitize:
        claim_uri = lbryt.sanitize_text(claim_uri)
        claim_title = lbryt.sanitize_text(claim_title)

    out = ["canonical_url: " + claim_uri,
           "claim_id: " + claim["claim_id"],
           "release_time: " + claim_time,
           "title: " + claim_title,
           80 * "-",
           "No comments"]

    content = "\n".join(out)

    return content


def act_comment(cmnt_in,
                action="create",
                cmnt_reply="reply",
                wallet_id="default_wallet",
                comm_server="https://comments.odysee.com/api/v2",
                server="http://localhost:5279"):
    """Perform an action on the comment."""
    cid = cmnt_in["claim"]["claim_id"]

    new_comment = cmnt_in["new_comment"]
    author_uri = cmnt_in["author"]

    comment_id = cmnt_in["comment_id"]

    if cmnt_reply in ("reply"):
        parent_id = comment_id
    elif cmnt_reply in ("standalone"):
        parent_id = None

    if action in ("create"):
        result = lbryt.create_comment(comment=new_comment,
                                      cid=cid,
                                      parent_id=parent_id,
                                      author_uri=author_uri,
                                      wallet_id=wallet_id,
                                      comm_server=comm_server,
                                      server=server)
        operation = "created comment"
    elif action in ("edit"):
        result = lbryt.update_comment(comment=new_comment,
                                      comment_id=comment_id,
                                      wallet_id=wallet_id,
                                      comm_server=comm_server,
                                      server=server)
        operation = "edited comment"
    elif action in ("abandon"):
        result = lbryt.abandon_comment(comment_id=comment_id,
                                       wallet_id=wallet_id,
                                       comm_server=comm_server,
                                       server=server)
        operation = "abandoned comment"

    if not result:
        if action in ("edit", "abandon"):
            text = (f"Status: failure ({action}); "
                    "can only edit or abandon our own comments; "
                    "also, check connection")
        elif action in ("create"):
            text = (f"Status: failure ({action}); "
                    "check connection")
    else:
        text = f"Status: success; {operation}"

    output = {"result": result,
              "status": text}

    return output
