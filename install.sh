#!/bin/bash

echo "🔧 Installing Python dependencies..."
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install bip-utils

echo "🔑 Making wallet generator executable..."
chmod +x wallet_generator.py

echo "✅ Done! Run it with: ./wallet_generator.py"
