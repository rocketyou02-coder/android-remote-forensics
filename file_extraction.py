#!/usr/bin/env python3
"""
File Extraction Module
Extracts files from Android devices for forensic analysis
"""

import subprocess
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class FileExtraction:
    """Extract files from Android devices"""
    
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
    
    def extract(self, device_path: str, output_dir: str) -> bool:
        """Extract files from device path"""
        if not self.device:
            logger.error("No device connected")
            return False
        
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            logger.info(f"Extracting {device_path} to {output_dir}")
            
            # Use adb pull to extract
            cmd = [self.adb_path, '-s', self.device, 'pull', device_path, output_dir]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info(f"Successfully extracted files")
                return True
            else:
                logger.error(f"Extraction failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            return False
    
    def extract_app_data(self, package_name: str, output_dir: str) -> bool:
        """Extract specific application data"""
        if not self.device:
            logger.error("No device connected")
            return False
        
        try:
            device_app_path = f"/data/data/{package_name}"
            return self.extract(device_app_path, output_dir)
        except Exception as e:
            logger.error(f"Error extracting app data: {e}")
            return False
    
    def extract_system_partition(self, output_dir: str) -> bool:
        """Extract system partition (requires root)"""
        if not self.device:
            logger.error("No device connected")
            return False
        
        try:
            logger.info("Attempting to extract system partition...")
            return self.extract("/system", output_dir)
        except Exception as e:
            logger.error(f"Error extracting system partition: {e}")
            return False
    
    def list_files(self, device_path: str) -> list:
        """List files in device directory"""
        if not self.device:
            logger.error("No device connected")
            return []
        
        try:
            cmd = [self.adb_path, '-s', self.device, 'shell', 'ls', '-la', device_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                files = result.stdout.strip().split('\n')
                return files
            return []
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []
