#!/usr/bin/env python3
"""
Example: Send Slack notification via Maton.ai

Usage:
    export MATON_API_KEY="your_key_here"
    python3 send_alert.py "C0123456789" "BTC Alert: Whale detected!"
"""

import urllib.request
import json
import os
import sys

if len(sys.argv) < 3:
    print("Usage: python3 send_alert.py CHANNEL_ID MESSAGE")
    exit(1)

MATON_API_KEY = os.environ.get('MATON_API_KEY')
if not MATON_API_KEY:
    print("Error: MATON_API_KEY environment variable not set")
    exit(1)

channel_id = sys.argv[1]
message = sys.argv[2]

# Send Slack message
data = json.dumps({
    'channel': channel_id,
    'text': message
}).encode()

req = urllib.request.Request(
    'https://gateway.maton.ai/slack/api/chat.postMessage',
    data=data,
    method='POST'
)
req.add_header('Authorization', f'Bearer {MATON_API_KEY}')
req.add_header('Content-Type', 'application/json')

try:
    response = urllib.request.urlopen(req)
    result = json.load(response)
    
    if result.get('ok'):
        print(f"✓ Message sent to Slack!")
        print(f"Channel: {channel_id}")
        print(f"Timestamp: {result.get('ts')}")
    else:
        print(f"✗ Error: {result.get('error')}")
        exit(1)
        
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode()}")
    exit(1)
