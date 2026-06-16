#!/bin/bash

# Android Remote Forensics Tool - Installation Script
# For Kali Linux and compatible distributions

echo "[*] Android Remote Forensics Tool Installer"
echo "[*] This tool requires root privileges"

if [[ $EUID -ne 0 ]]; then
   echo "[!] This script must be run as root"
   exit 1
fi

echo "[+] Checking Python version..."
python3 --version

echo "[+] Installing system dependencies..."
apt-get update
apt-get install -y python3-pip python3-dev android-tools-adb android-tools-fastboot libusb-1.0-0 libusb-1.0-0-dev

echo "[+] Installing Python dependencies..."
pip3 install -r requirements.txt

echo "[+] Setting up file permissions..."
chmod +x arft.py
chmod +x scripts/*.py
chmod +x scripts/*.sh

echo "[+] Creating symbolic link..."
ln -sf $(pwd)/arft.py /usr/local/bin/arft

echo "[+] Checking ADB installation..."
which adb

echo "[+] Installation complete!"
echo "[*] Run 'arft --help' to get started"
echo "[*] Connect your Android device and enable USB debugging"
