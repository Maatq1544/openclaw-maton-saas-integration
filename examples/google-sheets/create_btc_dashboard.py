#!/usr/bin/env python3
"""
Example: Create Google Spreadsheet and add data via Maton.ai

Usage:
    export MATON_API_KEY="your_key_here"
    python3 create_btc_dashboard.py
"""

import urllib.request
import json
import os
from datetime import datetime

MATON_API_KEY = os.environ.get('MATON_API_KEY')
if not MATON_API_KEY:
    print("Error: MATON_API_KEY environment variable not set")
    exit(1)

def maton_request(url, data=None, method='GET'):
    """Make request to Maton gateway"""
    req = urllib.request.Request(url, method=method)
    req.add_header('Authorization', f'Bearer {MATON_API_KEY}')
    req.add_header('Content-Type', 'application/json')
    
    if data:
        req.data = json.dumps(data).encode()
    
    try:
        response = urllib.request.urlopen(req)
        return json.load(response)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode()}")
        raise

# Step 1: Create spreadsheet
print("Creating BTC Analysis Dashboard...")
create_response = maton_request(
    'https://gateway.maton.ai/google-sheets/v4/spreadsheets',
    data={
        'properties': {
            'title': f'BTC Analysis Dashboard - {datetime.now().strftime("%Y-%m-%d")}'
        }
    },
    method='POST'
)

spreadsheet_id = create_response['spreadsheetId']
spreadsheet_url = create_response['spreadsheetUrl']

print(f"✓ Created spreadsheet: {spreadsheet_url}")

# Step 2: Add headers
headers = [['Timestamp', 'BTC Price (USD)', 'Volume (BTC)', 'Spread (%)', 'Signal', 'Notes']]

append_response = maton_request(
    f'https://gateway.maton.ai/google-sheets/v4/spreadsheets/{spreadsheet_id}/values/A1:append',
    data={
        'values': headers,
        'valueInputOption': 'RAW'
    },
    method='POST'
)

print(f"✓ Added headers")

# Step 3: Add sample data
sample_data = [
    [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "69305.49",
        "44254.75",
        "0.02",
        "HOLD",
        "Normal market conditions"
    ],
    [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "69500.00",
        "52000.00",
        "0.05",
        "🐋 WHALE WALL",
        "Large sell wall detected at $69,500"
    ]
]

append_response = maton_request(
    f'https://gateway.maton.ai/google-sheets/v4/spreadsheets/{spreadsheet_id}/values/A2:append',
    data={
        'values': sample_data,
        'valueInputOption': 'RAW'
    },
    method='POST'
)

print(f"✓ Added sample data")
print(f"\n🎉 Dashboard ready: {spreadsheet_url}")
print(f"Spreadsheet ID: {spreadsheet_id}")
print("\nYou can now automate data pushes to this sheet from your OpenClaw agent!")
