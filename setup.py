import setuptools
import biteco


setuptools.setup(
    name='biteco',
    version=biteco.__version__,
    description='A terminal dashboard with live updates, displaying bitcoin economic metrics. Inspired by Clark Moody Bitcoin Dashboard.',
    url='https://github.com/rctrinity/biteco',
    packages=['biteco'],
    install_requires=['rich ==13.3.2',
                        'python-bitcoinlib == 0.12.0',
                    ],
    entry_points={
        'console_scripts': ['biteco = biteco.biteco:main'],
    },
)
