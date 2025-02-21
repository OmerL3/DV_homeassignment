import requests
import json

# Server URL
URL = 'http://127.0.0.1:5001'

# Send request to server
def send_request(data):
    response = requests.post(URL, json=data)
    return response.json()

# Get account number
account_number = input("Enter your account number: ")
response = send_request({"account_number": account_number})
print(f"Server says: {response['message']}")

# Send password
password = input("Enter password: ")
response = send_request({"account_number": account_number, "password": password})
print(f"Server says: {response['message']}")

if response['status'] != "authenticated":
    print("Connection closed due to authentication failure")
    exit()

# Main loop
while True:
    user_input = input("Enter command (W <amt>:Withdraw, D <amt>:Deposit, G:Get balance, Q:Quit): ")
    response = send_request({"account_number": account_number, "message": user_input})
    
    print(f"Received command: {response['command']}")
    if 'message' in response:
        print(f"Server says: {response['message']}")
    if 'balance' in response:
        print(f"Current balance: {response['balance']}")
    
    if user_input.upper().startswith('Q'):
        break

print("Connection closed")