import http.server
import socketserver
import json
from datetime import datetime

# Server settings
HOST = '127.0.0.1'
PORT = 5001

# Hash table for accounts: {account_number: {'password': password, 'balance': balance}}
accounts = {}

# Create log file with current date and time
log_filename = f"server_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
print(f"Logging to {log_filename}")

# Function to log an action
def log_action(account_number, command, action):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - Account {account_number}: Command '{command}' - {action}"
    with open(log_filename, 'a') as log_file:
        log_file.write(log_entry + '\n')

class ATMRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)
        
        # Initial connection (account number only)
        if 'account_number' in data and 'password' not in data and 'message' not in data:
            account_number = data['account_number']
            log_action(account_number, "CONNECT", f"Client connected from {self.client_address}")
            
            if account_number in accounts:
                response = {"status": "exists", "message": "Please send password"}
            else:
                response = {"status": "new", "message": "Please create password"}
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
            return

        # Authentication (account number and password)
        if 'account_number' in data and 'password' in data and 'message' not in data:
            account_number = data['account_number']
            password = data['password']
            
            if account_number in accounts:
                if accounts[account_number]['password'] == password:
                    response = {"status": "authenticated", "message": "Login successful"}
                    log_action(account_number, "LOGIN", "Login successful")
                else:
                    response = {"status": "error", "message": "Invalid password"}
                    log_action(account_number, "LOGIN", "Invalid password")
            else:
                accounts[account_number] = {'password': password, 'balance': 0}
                response = {"status": "authenticated", "message": "Account created"}
                log_action(account_number, "CREATE", "Account created")
            
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
            return

        # Command processing (account number and message)
        if 'account_number' in data and 'message' in data:
            account_number = data['account_number']
            message = data['message']
            print(f"Received from client: {message}")
            
            parts = message.split()
            command = parts[0].upper() if parts else "Unknown"
            amount = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
            
            # Ensure account exists before processing commands
            if account_number not in accounts:
                self._set_headers(403)
                self.wfile.write(json.dumps({"error": "Account not authenticated"}).encode())
                return
            
            response = {"command": command}
            
            if command == 'W':  # Withdraw
                if amount > 0 and accounts[account_number]['balance'] >= amount:
                    accounts[account_number]['balance'] -= amount
                    response["message"] = f"Withdrew {amount}"
                    log_action(account_number, message, f"Withdrew {amount}, new balance: {accounts[account_number]['balance']}")
                else:
                    response["message"] = "Insufficient funds or invalid amount"
                    log_action(account_number, message, "Failed: Insufficient funds or invalid amount")
            elif command == 'D':  # Deposit
                if amount > 0:
                    accounts[account_number]['balance'] += amount
                    response["message"] = f"Deposited {amount}"
                    log_action(account_number, message, f"Deposited {amount}, new balance: {accounts[account_number]['balance']}")
                else:
                    response["message"] = "Invalid deposit amount"
                    log_action(account_number, message, "Failed: Invalid deposit amount")
            elif command == 'G':  # Get balance
                response["balance"] = accounts[account_number]['balance']
                log_action(account_number, message, f"Balance checked: {accounts[account_number]['balance']}")
            elif command == 'Q':  # Quit
                log_action(account_number, message, "Client requested disconnect")
            else:
                response["message"] = "Unknown command"
                log_action(account_number, message, "Failed: Unknown command")
            
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Invalid request
        self._set_headers(400)
        self.wfile.write(json.dumps({"error": "Invalid request"}).encode())

# Set up and run the server
with socketserver.TCPServer((HOST, PORT), ATMRequestHandler) as server:
    print(f"Server listening on {HOST}:{PORT}")
    server.serve_forever()