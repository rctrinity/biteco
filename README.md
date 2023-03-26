# Bitcoin Economics Live Terminal Dashboard 

 Inspired by Clark Moody's online dashboard at https://bitcoin.clarkmoody.com/dashboard/   
 This python written module should replace bitcoin-cli internal getinfo if you are running a node full-time.   
   
## **Requirements**:   

Must be running your own Bitcoin node. :-)

Rich library  https://github.com/Textualize/rich    
     python -m pip install rich       
     
 python-bitcoinlib by Peter Todd ( https://github.com/petertodd/python-bitcoinlib )    
     git clone https://github.com/petertodd/python-bitcoinlib.git    
         
 The below install will install all the required libraries above.
 
 ## **Install**:    
 1. From home folder, clone biteco -> git clone https://github.com/rctrinity/biteco
 2. python3 -m pip install -e biteco/  
 3. To run -> biteco  
 4. Optional only: Add rpcworkqueue=48 (default is 16) in your bitcoin.conf
 
 To stop biteco, touch ~/biteco/biteco/kill_biteco
 
 kill_biteco in same folder as biteco.py sends a kill trigger to the app. biteco will remove kill_biteco before exiting.
 
 The bitcoinlib rpc module uses your bitcoin.conf file to authenticate with the node. 
 I have made setting up biteco a bit easier with the setup module.
 
 
 Below is a screenshot of the dashboard.   
 
 
![Screenshot from 2023-03-26 08-31-42](https://user-images.githubusercontent.com/103879453/227779204-e0d26af7-1921-4f4a-bced-28a04c81de25.png)

