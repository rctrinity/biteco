from setuptools import setup, find_packages
import os
from biteco import __version__, __name__

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

setup(
    name=__name__,
    version=__version__,
    author='Farley',
    author_email='bfarley68@gmail.com',
    license='GNU Lesser General Public License v2.1',
    description='A terminal dashboard with live updates, displaying bitcoin economic metrics. Inspired by Clark Moody Bitcoin Dashboard.',
    long_description=README,
        long_description_content_type='text/markdown',
        classifers=[
            "Programming Language :: Python",
            "License :: OSI Approved :: GNU Lesser General Public License v2.1 or later (LGPLv2+)",
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

