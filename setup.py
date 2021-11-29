import os
import sys
import setuptools

__name__ = "lbrydseed"
__version__ = "1.0.0"
# entry = {'console_scripts': ['lbrydseed=dseed:main']}
# entry = {'gui_scripts': ['lbrydseed=dseed:main']}

base = os.path.dirname(__file__)
with open(os.path.join(base, "README.md")) as fdescription:
    long_description = fdescription.read()

classifiers = ['Framework :: AsyncIO',
               'Intended Audience :: Developers',
               'Intended Audience :: System Administrators',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python :: 3',
               'Operating System :: OS Independent',
               'Topic :: Internet',
               'Topic :: Software Development :: Testing',
               'Topic :: Software Development :: Libraries :: Python Modules',
               'Topic :: System :: Distributed Computing',
               'Topic :: Utilities']

setuptools.setup(name=__name__,
                 version=__version__,
                 author="belikor",
                 author_email="hello@lbry.com",
                 url="https://lbry.com",
                 description="Program to download content from channels",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 keywords="lbry protocol media download",
                 license="MIT",
                 python_requires=">=3.7",
                 # packges=setuptools.find_packages(),
                 packages=["lbseed", "lbrytools"],
                 py_modules=["dseed"],
                 zip_safe=False,
                 # entry_points=entry,
                 install_requires=["requests"],
                 classifiers=classifiers)

