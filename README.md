# P2P-CI
Running Instruction:
Python3.8 is required to run the code

# The setup I tested the functionalities of my code is following:
1. A server and a client are running on the vcl machine
   - By default, the firewall of the vcl environment block many of the port.
     So make sure to command the following in your CLI:
     sudo iptables -P INPUT ACCEPT
     sudo iptables -P FORWARD ACCEPT
     sudo iptables -P OUTPUT ACCEPT
     sudo iptables -F
     sudo iptables-save

2. A client is running on my local machine
   - You will have to change line10 server_name = '152.7.176.38' to the vcl machine ip address
  
3. Naming convention matters with the application. Currently, the txt file names as "title_rfcnumber.txt".
   So please make sure you follow this convention if you try to add more RFC other than the ones I provided.

# Steps to test:
1. run the server on the vcl machine by:
   python3 p2pserver_v3.py
2. run the client on the vcl machine by:
   python3 p2pclient_v3.py
3. Menu will be prompted as following:
********************************************************
Welcome to P2P-CI system

Please enter the option which you like to proceed

Option 1: ADD

Option 2: LOOKUP

Option 3: LIST

Option 4: Download RFC

Option 5: Leave

Enter your option

********************************************************
  
4. Enter the option you would like to verify; There will be input prompts
   to ask for your input

If you have any issues running the application, please do not hestitate to contact
us.
Contact info:
Zijun Lu: zlu5@ncsu.edu
Zhiyuan Ma: zma24@ncsu.edu