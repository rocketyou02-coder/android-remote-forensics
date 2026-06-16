#!/usr/bin/env python3
"""
Activity Monitor Module
Monitors and logs Android device activities
"""

import subprocess
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class ActivityMonitor:
    """Monitor device activities and log events"""
    
    def __init__(self, device: str = None, output_file: str = None):
        self.device = device or self._get_default_device()
        self.output_file = output_file or 'activities.log'
        self.adb_path = 'adb'
        self.running = False
    
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
    
    def monitor_logcat(self) -> None:
        """Monitor device logs via logcat"""
        if not self.device:
            logger.error("No device connected")
            return
        
        self.running = True
        try:
            logger.info("Starting logcat monitoring...")
            cmd = [self.adb_path, '-s', self.device, 'logcat']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            with open(self.output_file, 'a') as f:
                f.write(f"\n=== Logcat Monitoring Started: {datetime.now()} ===\n")
                
                while self.running:
                    line = process.stdout.readline()
                    if line:
                        f.write(line)
                        f.flush()
                        logger.info(line.strip())
        except KeyboardInterrupt:
            logger.info("Monitoring stopped")
        except Exception as e:
            logger.error(f"Error monitoring logcat: {e}")
        finally:
            self.running = False
            if 'process' in locals():
                process.terminate()
    
    def get_running_apps(self) -> list:
        """Get list of running applications"""
        if not self.device:
            logger.error("No device connected")
            return []
        
        try:
            cmd = [self.adb_path, '-s', self.device, 'shell', 'pm', 'list', 'packages']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                packages = result.stdout.strip().split('\n')
                return [pkg.replace('package:', '') for pkg in packages if pkg]
            return []
        except Exception as e:
            logger.error(f"Error getting running apps: {e}")
            return []
    
    def monitor_app_usage(self) -> None:
        """Monitor application usage"""
        if not self.device:
            logger.error("No device connected")
            return
        
        try:
            logger.info("Starting app usage monitoring...")
            with open(self.output_file, 'a') as f:
                f.write(f"\n=== App Usage Monitoring: {datetime.now()} ===\n")
                
                while self.running:
                    cmd = [self.adb_path, '-s', self.device, 'shell', 'dumpsys', 'usagestats']
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        f.write(f"\n[{datetime.now()}]\n")
                        f.write(result.stdout)
                        f.flush()
                    
                    time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("App usage monitoring stopped")
        except Exception as e:
            logger.error(f"Error monitoring app usage: {e}")
    
    def start(self) -> None:
        """Start activity monitoring"""
        self.running = True
        try:
            self.monitor_logcat()
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
    
    def stop(self) -> None:
        """Stop activity monitoring"""
        self.running = False
