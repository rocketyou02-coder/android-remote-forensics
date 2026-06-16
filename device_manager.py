#!/usr/bin/env python3
"""
Device Manager Module
Handles connection and communication with Android devices
"""

import subprocess
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class DeviceManager:
    """Manage connections to Android devices via ADB"""
    
    def __init__(self):
        self.connected_device = None
        self.adb_path = self._find_adb()
    
    def _find_adb(self) -> str:
        """Find ADB executable path"""
        try:
            result = subprocess.run(['which', 'adb'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as e:
            logger.error(f"Error finding ADB: {e}")
        return 'adb'
    
    def list_devices(self) -> List[str]:
        """List all connected Android devices"""
        try:
            result = subprocess.run(
                [self.adb_path, 'devices'],
                capture_output=True,
                text=True
            )
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            devices = [line.split()[0] for line in lines if line.strip() and 'device' in line]
            return devices
        except Exception as e:
            logger.error(f"Error listing devices: {e}")
            return []
    
    def connect(self, device_address: str) -> bool:
        """Connect to a remote Android device via TCP/IP"""
        try:
            result = subprocess.run(
                [self.adb_path, 'connect', device_address],
                capture_output=True,
                text=True,
                timeout=10
            )
            if 'connected' in result.stdout.lower():
                self.connected_device = device_address
                logger.info(f"Connected to {device_address}")
                return True
            logger.error(f"Connection failed: {result.stdout}")
            return False
        except Exception as e:
            logger.error(f"Error connecting to device: {e}")
            return False
    
    def execute_command(self, command: str) -> Optional[str]:
        """Execute command on connected device"""
        if not self.connected_device:
            logger.warning("No device connected")
            return None
        
        try:
            result = subprocess.run(
                [self.adb_path, '-s', self.connected_device, 'shell', command],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return None
    
    def pull_file(self, device_path: str, local_path: str) -> bool:
        """Pull file from device"""
        if not self.connected_device:
            logger.warning("No device connected")
            return False
        
        try:
            result = subprocess.run(
                [self.adb_path, '-s', self.connected_device, 'pull', device_path, local_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Error pulling file: {e}")
            return False
    
    def push_file(self, local_path: str, device_path: str) -> bool:
        """Push file to device"""
        if not self.connected_device:
            logger.warning("No device connected")
            return False
        
        try:
            result = subprocess.run(
                [self.adb_path, '-s', self.connected_device, 'push', local_path, device_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Error pushing file: {e}")
            return False
    
    def get_device_info(self) -> dict:
        """Get device information"""
        info = {}
        properties = [
            'ro.build.version.release',
            'ro.build.version.sdk',
            'ro.product.model',
            'ro.product.manufacturer',
            'ro.serialno'
        ]
        
        for prop in properties:
            output = self.execute_command(f'getprop {prop}')
            if output:
                info[prop] = output.strip()
        
        return info
