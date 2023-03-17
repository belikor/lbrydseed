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
"""Mixin classes that add comment pages to the main graphical interface.

These classes should not be instantiatied directly. They are just used
in a multiple inheritance, or mixin pattern, to provide the necessary
building command to build the specific page in the main interface.

::
    class CommentsPage:
        def setup_page_cmnt(self, parent):
            ...

    class Application(ttk.Frame, CommentsPage):
        def __init__(self, root):
            page_comment = ttk.Frame(root)
            self.setup_page_cmnt(page_comment)
"""
import tkinter as tk
import tkinter.ttk as ttk

import lbseed.blocks as blocks


class CommentsReplyPage:
    """Mixin class to provide the reply to comments page."""
    def setup_reply(self):
        self.top_reply = tk.Toplevel()
        self.top_reply.withdraw()
        self.top_reply.title("Comment reply")
        self.top_reply.protocol("WM_DELETE_WINDOW", self.remove_reply)

        self.setup_replay_intf(self.top_reply)
        return self.top_reply

    def remove_reply(self):
        self.top_reply.withdraw()
        return self.top_reply

    def setup_replay_intf(self, parent):
        frame1 = ttk.Frame(parent)
        frame1.pack(padx=4, pady=4, fill="both", expand=False)
        frame2 = ttk.Frame(parent)
        frame2.pack(padx=4, pady=4, fill="x")
        frame3 = ttk.Frame(parent)
        frame3.pack(padx=4, pady=4, fill="x")
        frame4 = ttk.Frame(parent)
        frame4.pack(padx=4, pady=4, fill="both", expand=True)
        frame5 = ttk.Frame(parent)
        frame5.pack(padx=4, pady=4, fill="x")
        self.setup_cmnt_claim(frame1)
        self.setup_rep_cmnt(frame2)
        self.setup_rep_chck(frame3)
        self.setup_textbox_rep_cmnt(frame4)
        self.setup_reply_status(frame5)

    def setup_cmnt_claim(self, parent):
        self.textbox_cmnt2 = blocks.setup_textbox(parent,
                                                  height=10,
                                                  font=self.txt_font)
        self.textbox_cmnt2["wrap"] = "word"

        content = "(no claim loaded)"
        self.textbox_cmnt2.replace("1.0", tk.END, content)
        self.textbox_cmnt2["state"] = "disabled"

    def setup_rep_cmnt(self, parent):
        lb = ttk.Label(parent, text="Comment as")
        lb.pack(side="left")

        self.cmb_author_cmnt = ttk.Combobox(parent,
                                            textvariable=self.cmb_rep_author,
                                            width=self.b_width - 1)
        self.cmb_author_cmnt.pack(side="left", padx=2)

        self.cmb_author_cmnt.state(["readonly"])
        self.cmb_author_cmnt["values"] = ["(None)"]
        self.cmb_author_cmnt.set("(None)")
        self.cmb_author_cmnt.bind("<<ComboboxSelected>>",
                                  self.cmb_cmnt_deselect)

        self.btn_cmnt = ttk.Button(parent,
                                   text="Reply",
                                   width=self.b_width,
                                   command=self.act_comment)
        self.btn_cmnt.pack(side="left", padx=4)

    def setup_rep_chck(self, parent):
        rad_cmt1 = ttk.Radiobutton(parent,
                                   text="Create comment",
                                   variable=self.rad_rep_opt,
                                   value="create",
                                   command=self.activate_rep)
        rad_cmt1.grid(row=0, column=0, sticky=tk.W)

        rad_cmt2 = ttk.Radiobutton(parent,
                                   text="Edit comment",
                                   variable=self.rad_rep_opt,
                                   value="edit",
                                   command=self.activate_edit)
        rad_cmt2.grid(row=1, column=0, sticky=tk.W)

        rad_cmt3 = ttk.Radiobutton(parent,
                                   text="Abandon comment",
                                   variable=self.rad_rep_opt,
                                   value="abandon",
                                   command=self.activate_abandon)
        rad_cmt3.grid(row=2, column=0, sticky=tk.W)

        self.rad_reply = ttk.Radiobutton(parent,
                                         text="Reply to active comment",
                                         variable=self.rad_rep_curr,
                                         value="reply")
        self.rad_reply.grid(row=0, column=1, columnspan=1, sticky=tk.W)

        self.rad_rep_alone = ttk.Radiobutton(parent,
                                             text="Create standalone comment",
                                             variable=self.rad_rep_curr,
                                             value="standalone")
        self.rad_rep_alone.grid(row=0, column=2, columnspan=1, sticky=tk.W)

    def _state_textbox_reply(self, state="normal"):
        self.textbox_cmnt_rep["state"] = state

        if state in ("normal"):
            self.textbox_cmnt_rep["background"] = "#ffffff"
        elif state in ("disabled"):
            self.textbox_cmnt_rep["background"] = "#939393"

    def _state_rad_reply(self, state="enabled"):
        self.rad_reply["state"] = state
        self.rad_rep_alone["state"] = state

    def activate_rep(self, show=True):
        self._state_rad_reply(state="enabled")
        self._state_textbox_reply(state="normal")
        self.cmb_author_cmnt["state"] = "enabled"
        self.btn_cmnt["text"] = "Reply"

        if show:
            self.show_comment()

    def activate_edit(self, show=True):
        self._state_rad_reply(state="disabled")
        self._state_textbox_reply(state="normal")
        self.cmb_author_cmnt["state"] = "disabled"
        self.btn_cmnt["text"] = "Edit"

        if show:
            self.show_comment()

    def activate_abandon(self, show=True):
        self._state_rad_reply(state="disabled")
        self._state_textbox_reply(state="normal")
        self.cmb_author_cmnt["state"] = "disabled"
        self.btn_cmnt["text"] = "Abandon"

        if show:
            self.show_comment()

        self._state_textbox_reply(state="disabled")

    def setup_textbox_rep_cmnt(self, parent):
        self.textbox_cmnt_rep = blocks.setup_textbox(parent,
                                                     font=self.txt_font)
        self.textbox_cmnt_rep["wrap"] = "word"

        content = ("(New comment)\n"
                   "\n"
                   "_Created with "
                   "[lbrydseed](https://github.com/belikor/lbrydseed)_")
        self.textbox_cmnt_rep.replace("1.0", tk.END, content)

    def setup_reply_status(self, parent):
        lab = ttk.Label(parent,
                        text="Status: no claim lodaded",
                        textvariable=self.lab_rep_status)
        lab.pack(side="left")


class CommentsPage(CommentsReplyPage):
    """Mixin class to provide comments page."""
    def setup_page_cmnt(self, parent):
        self.setup_top_cmnt(parent)
        frame1 = ttk.Frame(parent)
        frame1.pack(padx=4, pady=4, fill="both", expand=False)
        frame2 = ttk.Frame(parent)
        frame2.pack(padx=4, pady=4, fill="x")
        frame3 = ttk.Frame(parent)
        frame3.pack(padx=4, pady=4, fill="both", expand=False)
        frame4 = ttk.Frame(parent)
        frame4.pack(padx=4, pady=4, fill="both", expand=True)
        frame5 = ttk.Frame(parent)
        frame5.pack(padx=4, pady=4, fill="x")

        note = ttk.Notebook(frame1)
        p1 = ttk.Frame(note)
        p2 = ttk.Frame(note)
        note.add(p1, text="Claims")
        note.add(p2, text="Resolve information")
        note.pack(fill="both", expand=True)
        self.setup_textbox_cmnt_claim(p1)
        self.setup_textbox_cmnt_claim_summ(p2)

        self.setup_rep_btn(frame2)
        self.setup_listbox_cmnt(frame3)
        self.setup_textbox_cmnt(frame4)
        self.setup_reply_status(frame5)
        self.setup_reply()

    def setup_top_cmnt(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(padx=4, pady=4)
        self.setup_grid_top_cmnt(frame, start=0)
        self.setup_grid_btn_cmnt(frame, start=1)
        self.setup_cmt_info(frame, start=3)

    def setup_grid_top_cmnt(self, parent, start=0):
        entry = ttk.Entry(parent,
                          textvariable=self.cmnt_server,
                          font=self.e_font)
        entry["width"] = self.b_width + 12
        entry.grid(row=start, column=0, sticky=tk.W)

        bt = ttk.Button(parent,
                        text="Default comment server",
                        width=self.b_width,
                        command=self.default_comm_server)
        bt.grid(row=start, column=1, sticky=tk.W, padx=4)

    def setup_grid_btn_cmnt(self, parent, start=0):
        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Resolve online",
                                b_command=self.resolve_claims,
                                l_text="Confirm that the claim exists",
                                start=start)

        blocks.setup_button_gen(parent,
                                width=self.b_width,
                                b_text="Display comments",
                                b_command=self.list_comments,
                                l_text=("Load a claim, and display comments "
                                        "under the claim"),
                                start=start+1)

    def setup_cmt_info(self, parent, start=0):
        lb = ttk.Label(parent,
                       text=("Add a claim; "
                             "this should be a claim name, "
                             "channel name, "
                             "or claim ID (40-character string).\n"
                             "Only the first item will be considered."))
        lb.grid(row=start, column=0, columnspan=2, sticky=tk.W)

    def setup_textbox_cmnt_claim(self, parent):
        self.textbox_cmnt_claim = blocks.setup_textbox(parent,
                                                       height=4,
                                                       font=self.txt_font)
        content = ("please-stop-using-windows...#f\n"
                   "debunking-the-candle-challenge:f\n"
                   "83a23b2e2f20bf9af0d46ad38132e745c35d9ff4\n"
                   "vim-alchemy-with-macros")
        self.textbox_cmnt_claim.replace("1.0", tk.END, content)

    def setup_textbox_cmnt_claim_summ(self, parent):
        self.textbox_cmnt_claim_summ = \
            blocks.setup_textbox(parent, font=self.txt_lst_font,
                                 height=6)
        self.textbox_cmnt_claim_summ.insert("1.0",
                                            "(information about the claims)")
        self.textbox_cmnt_claim_summ["state"] = "disabled"

    def setup_rep_btn(self, parent):
        btn = ttk.Button(parent,
                         text="Reply, edit, or delete comment",
                         width=self.b_width,
                         command=self.reply_actions)
        btn.grid(row=0, column=0, sticky=tk.W)

        sep = ";"
        summary = (f"Total comments: 0{sep} "
                   f"root comments: 0{sep} "
                   "replies: 0")

        self.lab_cmnt_num = ttk.Label(parent, text=summary)
        self.lab_cmnt_num.grid(row=1, column=0, sticky=tk.W)

    def setup_listbox_cmnt(self, parent):
        self.lstbox_cmnt = blocks.setup_listbox_gen(parent,
                                                    height=10,
                                                    font=self.txt_font,
                                                    list_var=self.cmnt_list)
        self.lstbox_cmnt["selectmode"] = "browse"
        self.lstbox_cmnt.configure(exportselection=False)

        self.lstbox_cmnt.bind("<<ListboxSelect>>",
                              lambda e: self.show_comment())
        self.lstbox_cmnt.bind("<Double-1>",
                              lambda e: self.reply_actions())
        self.lstbox_cmnt.bind("<<Activate>>",
                              lambda e: self.reply_actions())

    def setup_textbox_cmnt(self, parent):
        self.textbox_cmnt = blocks.setup_textbox(parent,
                                                 font=self.txt_font)
        self.textbox_cmnt["wrap"] = "word"

        content = "(no claim loaded)"
        self.textbox_cmnt.replace("1.0", tk.END, content)
        self.textbox_cmnt["state"] = "disabled"
