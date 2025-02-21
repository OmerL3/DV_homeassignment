# ATM Server-Client System  

## Overview  
This project implements a simple ATM server-client system deployed on [Render](https://render.com). The server handles account operations such as deposits, withdrawals, and balance inquiries.  

**Note:** The server might be **offline** but can be deployed upon request.  

## Server  
- **Type:** HTTPS server  
- **Data Structure:** Uses a dictionary to store account information:  
  ```python
  {account_number: {"password": password, "balance": balance}}
  ```
- **Available Commands:**  
  - `W <amount>` – Withdraw `<amount>` from the account  
  - `D <amount>` – Deposit `<amount>` into the account  
  - `G` – Get account balance  

## Client  
The client interacts with the server by sending requests to execute ATM operations.  

### Running the Client  
1. Ensure Python is installed on your system.  
2. Install dependencies:  
   ```sh
   pip install -r requirements.txt
   ```
3. Run the client script:  
   ```sh
   python client.py
   ```
4. Follow the on-screen prompts:  
   - Enter your **account number**.  
   - Enter your **password**.  
   - Use the following commands:  
     - `W <amount>` – Withdraw money  
     - `D <amount>` – Deposit money  
     - `G` – Get balance  
     - `Q` – Quit session  

### Example Interaction  
```
Enter your account number: 12345
Server says: Please send password
Enter password: mypassword
Server says: Authentication successful

Enter command (W <amt>:Withdraw, D <amt>:Deposit, G:Get balance, Q:Quit): D 500
Received command: D 500
Server says: Deposit successful
Current balance: 500

Enter command: G
Received command: G
Current balance: 500

Enter command: Q
Connection closed
```

## Deployment  
The server is hosted on Render. If inactive, it can be redeployed upon request.  
