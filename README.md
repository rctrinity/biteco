# Bitcoin Economics Live Terminal Dashboard 

 Inspired by Clark Moody's online dashboard at https://bitcoin.clarkmoody.com/dashboard/   
 This python written module should replace bitcoin-cli internal getinfo if you are running a node full-time.   

 Version 0.2.3 released
 
 
## **Requirements**:   

Must be running your own Bitcoin node. :-)

Rich library  https://github.com/Textualize/rich    
     python -m pip install rich       
     
 python-bitcoinlib by Peter Todd ( https://github.com/petertodd/python-bitcoinlib )    
     git clone https://github.com/petertodd/python-bitcoinlib.git    
         
 The below steps will install all the required libraries above.
 
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
 
 ![Screenshot from 2023-04-08 11-08-57](https://user-images.githubusercontent.com/103879453/230731538-07180c2c-dcbd-4764-90a6-2cf7c2546714.png)



