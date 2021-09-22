#!/usr/bin/env python3
"""
Create a tooltip for a given widget.
"""
import tkinter as tk


class ToolTip:
    """
    Create a tooltip for a given widget.
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500  # miliseconds
        self.wraplength = 400  # pixels
        self.widget = widget
        self.tw = None
        self.id = None
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        iid = self.id
        self.id = None
        if iid:
            self.widget.after_cancel(iid)

    def showtip(self, event=None):
        if self.tw:
            return

        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + self.widget.winfo_height() + 1

        # Create a toplevel window, remove the window,
        # and leave only a floating label
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))

        label = tk.Label(self.tw,
                         text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()

