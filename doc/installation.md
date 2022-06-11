# Installation

Go back to the [_README_](../README.md).

## Content

- [Basic installation](#basic-installation)
- [Requisites](#requisites)
- [LBRY daemon](#lbry-daemon)
- [Python](#python)
- [lbrytools](#lbrytools)
- [Updating](#updating)
- [System wide installation](#system-wide-installation)
- [Optional](#optional)
- [AppImage](#appimage)

## Basic installation

Use Git to clone this repository with `--recurse-submodules`
to include `lbrytools` with the rest of the code:
```sh
git clone --recurse-submodules https://github.com/belikor/lbrydseed
```

After cloning you should have the following structure:
```
lbrydseed/
    dseed.py
    lbrytools/
    lbseed/
```

[Go back to _Content_](#content)

## Requisites

The basic requisites to run the program are:

- `lbrynet`, the LBRY daemon
- Python 3, and the packages
    - `tkinter`
    - `requests`
    - `emoji`
    - `lbrytools`
    - `matplotlib` (optional)

[Go back to _Content_](#content)

## LBRY daemon

You must have the LBRY Desktop application or the `lbrynet` client.
Get them from [lbry.com/get](https://lbry.com/get).

[Go back to _Content_](#content)

## Python

Most Linux distributions come with Python ready to use;
for Windows you may need to get the [official package](https://www.python.org/),
or a full featured distribution such as [Anaconda](https://www.anaconda.com/).
In Windows, make sure the Python executable is added to the `PATH`
so that it can be launched from anywhere in your system.

The program uses the `tkinter` module which makes the Tk graphical libraries
available in Python.
These libraries are normally distributed together with Python
although you may have to verify that they are actually installed:
```sh
sudo apt install python-tk
sudo apt install python3-tk  # for Ubuntu
sudo pacman -S tk  # for Arch
```

The `requests` library is necessary to communicate with the LBRY daemon;
the `emoji` module is used to clean up emojis from the output:
```sh
python -m pip install --user requests emoji
python3 -m pip install --user requests emoji  # for Ubuntu
```

To install Python packages the `pip` package manager is used.
If this is not installed it can be installed:
```sh
sudo apt install python-pip
sudo apt install python3-pip  # for Ubuntu
sudo pacman -S python-pip  # for Arch
```

On Windows, most prerequisites can be installed using `pip`,
although a big distribution like Anaconda may be easier to use,
as it contains many packages already.

[Go back to _Content_](#content)

## lbrytools

You must have the [lbrytools](https://github.com/belikor/lbrytools)
library.

You can download it manually or clone this repository
with `--recurse-submodules` in order to achieve the following structure:
```
lbrydseed/
    dseed.py
    lbrytools/
    lbseed/
```

[Go back to _Content_](#content)

## Updating

To update the program's code, make sure you are in the `lbrydseed/` directory:
```sh
cd lbrydseed/
git pull
```

The [lbrytools](https://github.com/belikor/lbrytools) library
is hosted in its own repository, and is used in this program as a submodule.
To update this component:
```sh
git submodule update --remote --rebase lbrytools/
```

If this causes merging errors you may have to update the submodule manually:
```sh
cd lbrydseed/lbrytools/
git fetch
git reset --hard FETCH_HEAD
```

[Go back to _Content_](#content)

## System wide installation

This is optional, and only required if you want to have the libraries
available in your entire system.

Copy the `lbrytools` directory (the one with an `__init__.py`)
and the `lbseed` directory (also with an `__init__.py`),
and place them inside a `site-packages` directory that is searched by Python.

This could be a local directory speciffic to the user:
```
/home/user/.local/lib/python3.8/site-packages/lbrytools
/home/user/.local/lib/python3.8/site-packages/lbseed
```

Or a system-wide directory:
```
/usr/local/lib/python3.8/dist-packages/lbrytools
/usr/local/lib/python3.8/dist-packages/lbseed
/usr/lib/python3/dist-packages/lbrytools
/usr/lib/python3/dist-packages/lbseed
```

Then place `dseed.py` wherever you want, and run it from there.

[Go back to _Content_](#content)

### Environmental variables

This is optional. Instead of moving the `lbrytools` and `lbseed` libraries,
simply add them to the `PYTHONPATH` environmental variable.
We must add the parent directory containing these libraries.
For example, if
```
/top1/
    lbseed/
/top2/pkg/
    lbrytools/
```

the variable would be
```sh
PYTHONPATH="/top1:/top2/pkg:$PYTHONPATH"
```

[Go back to _Content_](#content)

## Optional

The `matplotlib` library is optional, and only needed
to plot the histograms in the `"Seeding ratio"` page.
```sh
python -m pip install --user matplotlib
python3 -m pip install --user matplotlib  # for Ubuntu
```

[Go back to _Content_](#content)

## Setuptools

We can use `setuptools` with its standard options to generate
a directory (`build/lib/`) or archive (`dist/`) with the necessary files:
```sh
python setup.py build
python setup.py sdist
python setup.py clean
python setup.py clean --all
```

[Go back to _Content_](#content)

## AppImage

We can create an AppImage by running a single script:
```sh
bash create_appimage.sh
```

It will download some auxiliary tools and plugins, then it will create
an `AppDir` directory to be used with the downloaded `appimagetool`
to produce the final AppImage.

[Go back to _Content_](#content)
