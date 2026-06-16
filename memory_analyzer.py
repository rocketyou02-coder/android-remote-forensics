#!/usr/bin/env python3
"""
Memory Analyzer Module
Extracts and analyzes device memory
"""

import subprocess
import logging
import os

logger = logging.getLogger(__name__)


class MemoryAnalyzer:
    """Extract and analyze device memory"""
    
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
    
    def dump_memory(self, output_file: str) -> bool:
        """Dump device memory (requires root)"""
        if not self.device:
            logger.error("No device connected")
            return False
        
        try:
            logger.info("Attempting memory dump (requires root)...")
            
            # Get memory info
            cmd = [self.adb_path, '-s', self.device, 'shell', 'cat', '/proc/meminfo']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            with open(output_file, 'w') as f:
                f.write("=== Memory Information ===\n")
                f.write(result.stdout)
                f.write("\n\n=== Process Memory Maps ===\n")
                
                # Get process memory maps
                cmd = [self.adb_path, '-s', self.device, 'shell', 'cat', '/proc/maps']
                result = subprocess.run(cmd, capture_output=True, text=True)
                f.write(result.stdout)
            
            logger.info(f"Memory dump saved to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Error during memory dump: {e}")
            return False
    
    def get_memory_stats(self) -> dict:
        """Get memory statistics"""
        if not self.device:
            logger.error("No device connected")
            return {}
        
        try:
            cmd = [self.adb_path, '-s', self.device, 'shell', 'dumpsys', 'meminfo']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            stats = {}
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines[:30]:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        stats[key.strip()] = value.strip()
            
            return stats
        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {}
