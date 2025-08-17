For this app to run, you need to first run the command\
`pip install -r requirements.txt`\
The server runs on http://127.0.0.1:8000\

This app uses cryptography from one of the python frameworks, Hashing and encryption

Currently less protection but soon to be iron clad security, CRUD operations are run on the  back-end

Create function has an auto-create -[this creates a password for the user], users can also add an existing pwd
Read function serves to return valid user request (http get) requests
Update allows users to edit existing user data without having to delete it first
Delete fucntion allows for the safe deletion of existing user data with pre-coded SQL commands so as to avoid SQL injection


