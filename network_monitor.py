#!/usr/bin/env python3
"""
Network Monitor Module
Captures and monitors network traffic
"""

import subprocess
import logging

logger = logging.getLogger(__name__)


class NetworkMonitor:
    """Monitor device network traffic"""
    
    def __init__(self, device: str = None, interface: str = 'wlan0'):
        self.device = device or self._get_default_device()
        self.interface = interface
        self.adb_path = 'adb'
    
    def _get_default_device(self) -> str:
        """Get first connected device"""
        try:
            result = subprocess.run(
                ['adb', 'devices'],
                capture_output=True,
                text=True
            )
            lines = result.stdout.strip().split('\n')[1:]
            for line in lines:
                if 'device' in line and not 'offline' in line:
                    return line.split()[0]
        except Exception as e:
            logger.error(f"Error getting device: {e}")
        return None
    
    def start_capture(self, output_file: str) -> bool:
        """Start network traffic capture"""
        if not self.device:
            logger.error("No device connected")
            return False
        
        try:
            logger.info(f"Starting network capture on {self.interface}...")
            
            # Use tcpdump if available on device
            cmd = [
                self.adb_path, '-s', self.device, 'shell',
                'tcpdump', '-i', self.interface, '-w', f'/data/local/tmp/capture.pcap'
            ]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(f"Capture PID: {process.pid}")
            
            return True
        except Exception as e:
            logger.error(f"Error starting capture: {e}")
            return False
    
    def get_network_stats(self) -> dict:
        """Get network statistics"""
        if not self.device:
            logger.error("No device connected")
            return {}
        
        try:
            cmd = [self.adb_path, '-s', self.device, 'shell', 'netstat', '-an']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            stats = {
                'connections': result.stdout.count('ESTABLISHED'),
                'raw_output': result.stdout
            }
            
            return stats
        except Exception as e:
            logger.error(f"Error getting network stats: {e}")
            return {}
