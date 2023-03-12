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
 
 
![Screenshot 2023-03-12 at 7 45 24 AM](https://user-images.githubusercontent.com/103879453/224545585-00ba4d94-196e-4966-8efc-7a417d304ea8.png)
