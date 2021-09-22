#!/usr/bin/env python3
"""Small application to download claims from channels."""
import sys
import tkinter as tk
import tkinter.scrolledtext as scrtext


def validate_input(text):
    channels = text.splitlines()

    chan_parsed = []
    num_parsed = []

    out = []
    num = 0

    for ch in channels:
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
        _ch_name = f"'{ch_name}'"
        if edited:
            out += [f"{num:2d}: name={_ch_name:35s} number={number}  <-- edited"]
        else:
            out += [f"{num:2d}: name={_ch_name:35s} number={number}"]

        chan_parsed.append(ch_name)
        num_parsed.append(number)

    print("\n".join(out))
    return chan_parsed, num_parsed


class Application(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_widgets(parent)

    def setup_widgets(self, parent):
        self.setup_buttons(parent)
        self.setup_textbox(parent)

    def setup_buttons(self, parent):
        b_validate = tk.Button(parent, text="Validate",
                               width=20,
                               command=self.validate)
        b_validate.pack()
        b_validate.focus()

        button = tk.Button(parent, text="Download claims",
                           width=20,
                           command=self.start_download)
        button.pack()

        _text = ("Add a channel, a comma, "
                 "and the number of items to download\n"
                 "from this channel")
        label = tk.Label(parent, text=_text, justify=tk.LEFT)
        label.pack()

    def setup_textbox(self, parent):
        self.textbox = scrtext.ScrolledText(parent,
                                            font="monospace",
                                            width=62, height=12,
                                            wrap=tk.NONE)
        self.textbox.bind("<Tab>", self.focus_next_widget)

        channels = ["@my-favorite-channel, 5",
                    "@OdyseeHelp#b, 10",
                    "@lbry:3f, 11"]
        channels = "\n".join(channels)

        self.textbox.insert("1.0", channels)
        self.textbox.pack(side="top", fill="both", expand=True)

        hsrl = tk.Scrollbar(parent,
                            orient="horizontal",
                            command=self.textbox.xview)
        hsrl.pack(side="bottom", fill=tk.X)
        self.textbox.config(xscrollcommand=hsrl.set)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def validate(self):
        text = self.textbox.get("1.0", tk.END)
        chans, nums = validate_input(text)
        return chans, nums

    def start_download(self):
        print("Download claims")
        print(80 * "-")
        chans, nums = self.validate()
        print()


def main(argv=None):
    root = tk.Tk()
    myapp = Application(root)
    myapp.master.title("lbrydseed")
    myapp.mainloop()


if __name__ == "__main__":
    sys.exit(main())

