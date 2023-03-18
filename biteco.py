'''
 biteco.py
 v0.1.1 Stable
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

from time import sleep
from rich.align import Align
from rich.live import Live as Live
from rich.console import Console as console
from gentables import dashboard, generateDataForTables
import util
from util import clear, q
from rich import print, pretty


def liveUpdate():
    global q
    q.put(generateDataForTables())

          
def main():
    
    clear() 
    print("[bright_black]Initializing dashboard[white]...")
    Dashboard = dashboard()
    
    # Pre-fill our Queue
    for i in range(3):
        liveUpdate()
        sleep(1)
    
    try:        
        with Live(Align.center(Dashboard.generateLayout(),vertical="middle"), screen=True, console=console()) as live_table:
            while True:
                try:
                    liveUpdate()
                    sleep(60*0.02) 
                    live_table.update(Align.center(Dashboard.updateLayout(), vertical="middle"), refresh=True)
                except KeyboardInterrupt:
                    raise

    except (KeyboardInterrupt, SystemExit):
        print(f"{'Shutting down: Keyboard Interrupt.'}")
          

if __name__ == '__main__':
    main()    
