#!/usr/bin/env python3
"""
Application Analyzer Module
Analyzes installed applications and their permissions
"""

import subprocess
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class AppAnalyzer:
    """Analyze Android applications"""
    
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
    
    def get_installed_packages(self) -> list:
        """Get list of installed packages"""
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
            logger.error(f"Error getting packages: {e}")
            return []
    
    def get_app_permissions(self, package_name: str) -> dict:
        """Get permissions for specific app"""
        if not self.device:
            logger.error("No device connected")
            return {}
        
        try:
            cmd = [self.adb_path, '-s', self.device, 'shell', 'pm', 'dump', package_name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            permissions = {}
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'android.permission' in line:
                        permissions[line.strip()] = True
            
            return permissions
        except Exception as e:
            logger.error(f"Error getting permissions: {e}")
            return {}
    
    def get_app_info(self, package_name: str) -> dict:
        """Get detailed information about app"""
        if not self.device:
            logger.error("No device connected")
            return {}
        
        try:
            cmd = [self.adb_path, '-s', self.device, 'shell', 'dumpsys', 'package', package_name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            info = {}
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines[:20]:  # Get first 20 lines
                    if '=' in line or ':' in line:
                        info[line.strip()] = True
            
            return info
        except Exception as e:
            logger.error(f"Error getting app info: {e}")
            return {}
    
    def analyze(self, output_file: str) -> bool:
        """Perform comprehensive app analysis"""
        if not self.device:
            logger.error("No device connected")
            return False
        
        try:
            logger.info("Starting application analysis...")
            packages = self.get_installed_packages()
            
            analysis_results = {
                'timestamp': datetime.now().isoformat(),
                'device': self.device,
                'total_apps': len(packages),
                'applications': []
            }
            
            for i, package in enumerate(packages):
                logger.info(f"Analyzing {i+1}/{len(packages)}: {package}")
                
                app_data = {
                    'package_name': package,
                    'permissions': self.get_app_permissions(package),
                    'info': self.get_app_info(package)
                }
                
                analysis_results['applications'].append(app_data)
            
            # Save results
            with open(output_file, 'w') as f:
                json.dump(analysis_results, f, indent=2)
            
            logger.info(f"Analysis complete. Results saved to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            return False
