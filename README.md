Request Filter Input Validation - NodeJS
Instructions
Vulnerable Variant
Step 1: Open terminal

Step 2: Access Directory with codebase

cd /root/node-input-validation

Step 3: Build the insecure app
docker build -t node-input-validation .

Step 4: Run the insecure app
docker run -d -p 8080:8080 node-input-validation

Step 5: Try and load some malicious payloads in the JSON input
http POST http://localhost:8080/create-user email="<script>alert(1)</script>" userType="OR '1'='1" address="something else" zip:=18975
Try a variation of different payloads. You should see that there's no input validation

Teardown
Step 1: Stop all the containers
curl -sSL https://raw.githubusercontent.com/we45/xml-files/master/clean-docker.sh | sh
Secure Variant
Now back in your IDE, examine the file secure_app.js and observe what's different about it

Step 1:

Now change the app.js to be like secure_app.js in the docker file
Either type in the code or copy-paste

Step 2: Access Directory with codebase

cd /root/node-input-validation
Step 3: Rebuild the container
docker build -t node-input-validation .

Step 4: Run the app
docker run -d -p 8080:8080 node-input-validation

Step 5: Try similar payloads
http POST http://localhost:8080/create-user email="<script>alert(1)</script>" userType="OR '1'='1" address="something else" zip:=18975

Teardown
Step 1: Stop all the containers
curl -sSL https://raw.githubusercontent.com/we45/xml-files/master/clean-docker.sh | sh

