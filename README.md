# Bitcoin Economics Live Terminal Dashboard 

 Inspired by Clark Moody's online dashboard at https://bitcoin.clarkmoody.com/dashboard/   
 This python written module should replace bitcoin-cli internal getinfo if you are running a node full-time.   

 Version 1.0.0 stable release
 - Tested on Ubuntu & Mac M1
 - Added server uptime to the footer of the panel
 - The 'Percent RBF' is disabled by default. Line 37 in ./biteco/gentables.py, you can change to True. Beware, can run sluggish if activity is high.
 
 
## **Requirements**:   

Must be running your own Bitcoin node. :-)

Biteco uses Rich Library for the Dashboard, Panel, and Tables. Uses python-bitcoinlib to communicate with your node.
Below is more information on the two libraries. You do not need to install these individually, as the **Install** steps below manages this and
installs any missing libraries.

- Rich library  https://github.com/Textualize/rich               
- python-bitcoinlib by Peter Todd ( https://github.com/petertodd/python-bitcoinlib )        
         
 The below steps will install the required libraries above, as well as requests, if missing.
 
 ## **Install**:    
 1. From home folder, clone biteco -> git clone https://github.com/rctrinity/biteco
 2. python3 -m pip install -e biteco/  
 3. To run -> biteco  
 4. Optional only: Add rpcworkqueue=48 (default is 16) in your bitcoin.conf
 
 To stop biteco, touch ~/biteco/biteco/kill_biteco
 I created an alias on my machine to run the touch command. Biteco exists smoothly with this option, and is recommended approach.
 
 - 'touch' kill_biteco in folder ~/biteco/biteco/ sends a kill trigger to the app. 
 - biteco will remove kill_biteco before exiting.
 
 The bitcoinlib rpc module uses your bitcoin.conf file to authenticate with your server. 
 I have made setting up biteco a bit easier with the setup module.
 
 
 Below is a screenshot of the dashboard.   
 
![Screenshot 2023-04-09 at 10 20 01 PM](https://github.com/rctrinity/biteco/blob/main/Biteco.png)



