'''
 biteco.py
 v0.01 BETA
 Capture Market, Network, Gold, Metrics, and upcoming Events (difficulty and halving)  
 Copyright (c) 2023 Farley
 ___             _       _  _ 
| __| __ _  _ _ | | ___ | || |
| _| / _` || '_|| |/ -_) \_. |
|_|  \__/_||_|  |_|\___| |__/

Requires: 
   Rich library ( https://github.com/Textualize/rich )
     python -m pip install rich
   
   python-bitcoinlib by Peter Todd ( https://github.com/petertodd/python-bitcoinlib )
     git clone https://github.com/petertodd/python-bitcoinlib.git
         This uses a modified copy of rpc.py from bitcoin.core, which is included in custom folder

This terminal dashboard was inspired by Clark Moody's Bitcoin dashboard: https://bitcoin.clark.moody/dashboard
'''

import sys
from time import sleep
from rich.align import Align
from rich.live import Live as Live
from rich.console import Console as console
from rich import print, pretty
from gentables import generateLayout
from util import clear

          
def main():
    clear() 
    print("[bright_black]Initializing dashboard[white]...")
    
    try:        
        with Live(Align.center(generateLayout(),vertical="middle"), screen=True, console=console()) as live_table:
            while True:
                sleep(60*0.05)  # 5 Minutes has been solid. If adjusted lower, the getnetowrkinfo RPC call tends to give connection problems.
                live_table.update(Align.center(generateLayout(), vertical="middle"), refresh=True)

    except KeyboardInterrupt:
        print(f"{'Shutting down: Keyboard Interrupt.'}")
        sys.exit()  

if __name__ == '__main__':
    main()    
