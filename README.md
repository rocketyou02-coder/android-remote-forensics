# Android Remote Forensics Tool (ARFT)

A comprehensive Kali Linux tool for remote access, control, and forensic analysis of Android devices. Designed for security professionals and forensic analysts.

## Features

- **Remote Device Control**: Execute commands on Android devices
- **Screen Mirroring**: Real-time screen capture and display
- **File Extraction**: Forensic-grade file system analysis and extraction
- **Activity Monitoring**: Track application activities and system logs
- **Memory Analysis**: Extract and analyze device memory
- **Network Monitoring**: Capture and analyze network traffic
- **App Analysis**: Inspect installed applications and permissions
- **Data Recovery**: Recover deleted files and data

## Prerequisites

- Kali Linux (or any Linux distribution)
- Python 3.8+
- ADB (Android Debug Bridge)
- USB drivers for Android devices
- Root/sudo access

## Installation

```bash
git clone https://github.com/rocketyou02-coder/android-remote-forensics.git
cd android-remote-forensics
chmod +x install.sh
sudo ./install.sh