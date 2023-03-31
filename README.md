JSONSchema - JSON Validation
This lab exercise is for understanding input validation on JSON schema.

Instructions
Vulnerable Variant
Step 1: Change to directory
cd /root/node-json-schema
Step 2: Build Container
docker build -t node-jsonschema .
Step 3: Run Docker Container
docker run -d -p 5000:5000 node-jsonschema

Step 4: Attempt Multiple payloads
http POST http://localhost:5000/signup firstName="<script>alert(1)</script>" lastName=somethingElse
Attempt multiple payloads of different types of vulnerabilities

Teardown
Step 1: Stop the app
clean-docker
Secure Variant
Step 1:
On the IDE, go to node-jsonschema folder
Open Dockerfile
Replace line number 7 with COPY solution-index.js /app/
Replace line number 9 with CMD ["node", "solution-index.js"]
Save the changes
It Should look like this

```docker
FROM node:10

RUN mkdir -p /app
WORKDIR /app
COPY package*.json /app/
RUN npm install
COPY solution-index.js /app/
EXPOSE 5000
CMD ["node", "solution-index.js"]
```
Copy
Step 2: Rebuild the application
docker build -t node-jsonschema .
Step 3: Run the app
docker run -d -p 5000:5000 node-jsonschema
Step 4: Stop the application
http POST http://localhost:5000/signup firstName="<script>alert(1)</script>" lastName=somethingElse email=something@email.com
Teardown
Step 1: Stop the app
clean-docker
