# Automated Stock Exchange System

## Overview
This Python program is a course project that simulates an automated stock exchange system. It allows users to create accounts, place buy/sell orders (bids and asks), and automatically matches compatible orders for execution. The system demonstrates core programming concepts including file I/O for data persistence, input validation, object-oriented design, and basic trading algorithms, while maintaining transaction logs and account records.

## Features

- **Account Management**:
  - Create user accounts with first name, last name, and email
  - Unique user IDs automatically assigned
  - Account data persisted to file

- **Stock Trading**:
  - Place bidding (buy) orders
  - Place asking (sell) orders
  - Automatic matching of compatible orders
  - Transaction execution when bid price ≥ ask price
  - Partial order fulfillment supported

- **Data Persistence**:
  - Accounts saved to `accounts4.txt`
  - Transaction executions logged to `execution_log4.txt`

## Input Validation
The system includes robust input validation for:
- Non-empty fields
- Valid email formats
- Positive numbers for prices and quantities
- Valid stock names (alphanumeric only)
- Existing user IDs for transactions

## How It Works

1. **Accounts**:
   - New accounts are assigned sequential IDs
   - Account data is appended to the accounts file
   - All accounts are loaded at program startup

2. **Order Matching**:
   - Bids are sorted by price (highest first)
   - Asks are sorted by price (lowest first)
   - Matches occur when bid price ≥ ask price for the same stock
   - Transactions execute at the ask price

3. **Execution**:
   - The maximum possible quantity is traded
   - Remaining quantities stay in the order book
   - Fully filled orders are removed
   - All executions are logged with details

## Files

- `Automatic Stock Exchange System.py`: Main program file
- `accounts4.txt`: Stores account data (created if doesn't exist)
- `execution_log4.txt`: Logs all executed transactions (created if doesn't exist)

## How to Run

1. Ensure you have Python installed
2. Run the program: `python Backbencher.py`
3. Follow the menu prompts to:
   - Create accounts
   - Place bids and asks
   - View execution results in the log file

## Notes

- All stock names are converted to lowercase
- The system prevents users from trading with themselves
- Data is preserved between program runs

## Example Usage

1. Create an account
2. Place a bid for a stock
3. Place an ask for the same stock at a lower price
4. The system will automatically match and execute the trade
5. Check `execution_log4.txt` for transaction details
