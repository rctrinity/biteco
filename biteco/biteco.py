'''
 biteco.py
 v0.2.0 Stable
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

This terminal dashboard was inspired by Clark Moody's Bitcoin dashboard: https://bitcoin.clark.moody/dashboard
'''

from rich.align import Align
from rich.live import Live as Live
from rich.console import Console as console
from biteco.gentables import dashboard
from biteco.util import clear
from rich import print
import sys
import os
import os.path

class KillBiteco(Exception):
    pass

          
def main():
 
    clear() 
    print("[bright_black]Initializing dashboard[white]...")
    Dashboard = dashboard()
    
    try:        
        with Live(Align.center(Dashboard.generateLayout(),vertical="middle"), screen=True, console=console()) as live_table:
            while True:
                try:
                    here = os.path.abspath(os.path.dirname(__file__))
                    file_exists = os.path.exists(os.path.join(here, 'kill_biteco'))
                    if file_exists:
                        os.remove(os.path.join(here, 'kill_biteco'))
                        raise KillBiteco
                    
                    live_table.update(Align.center(Dashboard.updateLayout(), vertical="middle"), refresh=True)
                except KeyboardInterrupt:
                    raise

    except (KeyboardInterrupt, SystemExit):
        print(f"{'Shutting down: Keyboard Interrupt.'}")
    
    except (KillBiteco, SystemExit):
        print('Shutting down: kill_biteco found.')
          

if __name__ == '__main__':
    main()    
