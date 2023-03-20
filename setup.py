import setuptools
import biteco


setuptools.setup(
    name='biteco',
    version=biteco.__version__,
    description='A terminal dashboard with live updates, displaying bitcoin economic metrics. Inspired by Clark Moody Bitcoin Dashboard.',
    url='https://github.com/rctrinity/biteco',
    packages=['biteco'],
    entry_points={
        'console_scripts': ['biteco = biteco.biteco:main'],
    },
)