from setuptools import setup, find_packages
import os
from biteco import __version__

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

setup(
    name='biteco',
    version=__version__,
    description='A terminal dashboard with live updates, displaying bitcoin economic metrics. Inspired by Clark Moody Bitcoin Dashboard.',
    long_description=README,
        long_description_conten_type='text/markdown',
        classifers=[
            "Programming Language :: Python",
            "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        ],
    url='https://github.com/rctrinity/biteco',
    packages=find_packages(),
    install_requires=['rich ==13.3.2',
                        'python-bitcoinlib == 0.12.0',
                    ],
    entry_points={
        'console_scripts': ['biteco = biteco.biteco:main'],
    },
)
