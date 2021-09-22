#!/usr/bin/env python3
"""
General purpose tooltip classes.

Based on
https://hg.python.org/cpython/file/63a00d019bb2/Lib/idlelib/ToolTip.py
"""
import tkinter as tk


class ToolTipBase:
    """
    Base for a tooltip for a given widget.
    """
    def __init__(self, widget):
        self.waittime = 500  # miliseconds
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self._id1 = self.widget.bind("<Enter>", self.enter)
        self._id2 = self.widget.bind("<Leave>", self.leave)
        self._id3 = self.widget.bind("<ButtonPress>", self.leave)

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

    def showtip(self):
        if self.tipwindow:
            return
        # The tip window must be completely outside the widget;
        # otherwise when the mouse enters the tip window we get
        # a leave event and it disappears, and then we get an enter
        # event and it reappears, and this repeats forever.
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 1

        # Create a toplevel window, remove the window,
        # and show the tooltip through a custom function.
        self.tipwindow = tk.Toplevel(self.widget)
        self.tipwindow.wm_overrideredirect(True)
        self.tipwindow.wm_geometry("+%d+%d" % (x, y))
        self.showcontents()

    def showcontents(self, text="Your text here"):
        """Show the actual contents. Can be overriden in a derived class."""
        label = tk.Label(self.tipwindow,
                         text=text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1)
        label.pack(ipadx=2, ipady=2)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


class ToolTip(ToolTipBase):
    """
    Tooltip class that can be used with any widget.
    """
    def __init__(self, widget, text):
        super().__init__(widget)
        self.text = text

    def showcontents(self):
        super().showcontents(self.text)


class ListboxToolTip(ToolTipBase):
    """
    Tooltip class that is used with a list of strings.
    """
    def __init__(self, widget, items):
        super().__init__(widget)
        self.items = items

    def showcontents(self):
        listbox = tk.Listbox(self.tipwindow, background="#ffffe0",
                             height=len(self.items))
        listbox.pack()
        m = 10
        for item in self.items:
            listbox.insert(tk.END, item)
            if len(item) > m:
                m = len(item)
                print(m)

        listbox["width"] = m - 5
