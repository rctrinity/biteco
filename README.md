# Bitcoin Economics Live Terminal Dashboard 

 Inspired by Clark Moody's online dashboard at https://bitcoin.clarkmoody.com/dashboard/   
 This python written module should replace bitcoin-cli internal getinfo if you are running a node full-time.   
   
## **Requirements**:   

Rich library  https://github.com/Textualize/rich    
     python -m pip install rich       
     
 python-bitcoinlib by Peter Todd ( https://github.com/petertodd/python-bitcoinlib )    
     git clone https://github.com/petertodd/python-bitcoinlib.git    
         
 ## **Install**:    
     
 1. clone python-bitcoinlib   
 2. Install libsssl-dev -> sudo apt-get install libssl-dev on linux or brew install openssl on mac-os. Needed for bitcoinlib.   
 3. Copy the 3 scripts from here: biteco.py, gentables.py, and util.py into the main python-bitcoinlib directory   
 4. Install Rich library   
 5. To run -> python3 ~/main-folder-to-python-bitcoinlib/biteco.py   
 
 The bitcoinlib rpc module uses your bitcoin.conf file to authenticate with the node.   
 
 Below is a screenshot of the dashboard.   
 
 
![Image 3-5-23 at 4 47 PM](https://user-images.githubusercontent.com/103879453/223024407-91c74c99-6055-4720-a8c0-2e66c58c89a2.jpg)
