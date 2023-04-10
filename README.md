# Bitcoin Economics Live Terminal Dashboard 

 Inspired by Clark Moody's online dashboard at https://bitcoin.clarkmoody.com/dashboard/   
 This python written module should replace bitcoin-cli internal getinfo if you are running a node full-time.   

 Version 0.2.4 released
 - Added Blocks to Clear and Percent RBF to Mempool Info
 - Code Cleanup
 
 
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
 
![Screenshot 2023-04-09 at 10 20 01 PM](https://user-images.githubusercontent.com/103879453/230818929-328d8657-469c-45b9-9a04-dd85d6091d72.png)



