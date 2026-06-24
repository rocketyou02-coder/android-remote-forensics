#!/usr/bin/env python3
"""
Data Recovery Module
Recovers deleted files and data from Android devices
"""

import subprocess
import logging
import os

logger = logging.getLogger(__name__)


class DataRecovery:
    """Recover deleted data from Android devices"""
    
    def __init__(self, device: str = None):
        self.device = device or self._get_default_device()
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
    
    def recover(self, output_dir: str) -> bool:
        """Attempt to recover deleted data"""
        if not self.device:
            logger.error("No device connected")
            return False
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            logger.info(f"Starting data recovery to {output_dir}...")
            logger.warning("This requires root access on the device")
            
            # Extract cache and temp directories
            paths_to_recover = [
                '/cache',
                '/data/cache',
                '/data/tmp',
                '/data/local/tmp'
            ]
            
            for path in paths_to_recover:
                logger.info(f"Recovering from {path}...")
                local_path = os.path.join(output_dir, os.path.basename(path))
                
                cmd = [self.adb_path, '-s', self.device, 'pull', path, local_path]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"Successfully recovered {path}")
            
            logger.info("Data recovery complete")
            return True
        except Exception as e:
            logger.error(f"Error during data recovery: {e}")
            return False
