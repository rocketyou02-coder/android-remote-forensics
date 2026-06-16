#!/usr/bin/env python3
"""
Android Remote Forensics Tool (ARFT)
A comprehensive tool for remote access, control, and forensic analysis of Android devices
Author: rocketyou02-coder
License: MIT
"""

import sys
import os
import click
import logging
from pathlib import Path
from modules.device_manager import DeviceManager
from modules.screen_mirror import ScreenMirror
from modules.file_extraction import FileExtraction
from modules.activity_monitor import ActivityMonitor
from modules.app_analyzer import AppAnalyzer
from modules.memory_analyzer import MemoryAnalyzer
from modules.network_monitor import NetworkMonitor
from modules.data_recovery import DataRecovery

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('arft.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ARFT:
    """Main Android Remote Forensics Tool class"""
    
    def __init__(self):
        self.device_manager = DeviceManager()
        self.screen_mirror = None
        self.file_extraction = None
        self.activity_monitor = None
        self.app_analyzer = None
        self.memory_analyzer = None
        self.network_monitor = None
        self.data_recovery = None
    
    def connect_device(self, device_address):
        """Connect to Android device"""
        logger.info(f"Attempting to connect to {device_address}")
        if self.device_manager.connect(device_address):
            logger.info("Successfully connected to device")
            return True
        logger.error("Failed to connect to device")
        return False
    
    def list_devices(self):
        """List connected devices"""
        devices = self.device_manager.list_devices()
        if devices:
            logger.info(f"Found {len(devices)} device(s)")
            for device in devices:
                logger.info(f"  - {device}")
            return devices
        logger.warning("No devices found")
        return []


@click.group()
def cli():
    """Android Remote Forensics Tool - Control and analyze Android devices"""
    pass


@cli.command()
@click.option('--ip', required=True, help='Device IP address')
@click.option('--port', default=5555, help='Device port (default: 5555)')
def connect(ip, port):
    """Connect to an Android device"""
    arft = ARFT()
    device_address = f"{ip}:{port}"
    if arft.connect_device(device_address):
        click.echo(click.style("[+] Connected successfully", fg='green'))
    else:
        click.echo(click.style("[!] Connection failed", fg='red'))


@cli.command()
def list_devices():
    """List all connected devices"""
    arft = ARFT()
    devices = arft.list_devices()
    if devices:
        click.echo("\nConnected Devices:")
        for i, device in enumerate(devices, 1):
            click.echo(f"  {i}. {device}")
    else:
        click.echo(click.style("No devices found. Enable USB debugging on your Android device.", fg='yellow'))


@cli.command()
@click.option('--device', default=None, help='Target device ID')
@click.option('--fps', default=30, help='Frames per second (default: 30)')
def screen_mirror(device, fps):
    """Mirror Android device screen in real-time"""
    click.echo(click.style("[*] Starting screen mirroring...", fg='cyan'))
    arft = ARFT()
    arft.screen_mirror = ScreenMirror(device, fps)
    try:
        arft.screen_mirror.start()
    except KeyboardInterrupt:
        click.echo(click.style("\n[*] Screen mirroring stopped", fg='yellow'))


@cli.command()
@click.option('--device', default=None, help='Target device ID')
@click.option('--path', required=True, help='Path to extract from device')
@click.option('--output', required=True, help='Output directory for extracted files')
def extract_files(device, path, output):
    """Extract files from Android device for forensic analysis"""
    click.echo(click.style(f"[*] Extracting files from {path}...", fg='cyan'))
    arft = ARFT()
    arft.file_extraction = FileExtraction(device)
    try:
        arft.file_extraction.extract(path, output)
        click.echo(click.style(f"[+] Files extracted to {output}", fg='green'))
    except Exception as e:
        click.echo(click.style(f"[!] Extraction failed: {str(e)}", fg='red'))


@cli.command()
@click.option('--device', default=None, help='Target device ID')
@click.option('--output', required=True, help='Output file for monitoring data')
def monitor_activities(device, output):
    """Monitor and log device activities"""
    click.echo(click.style("[*] Starting activity monitoring...", fg='cyan'))
    arft = ARFT()
    arft.activity_monitor = ActivityMonitor(device, output)
    try:
        arft.activity_monitor.start()
    except KeyboardInterrupt:
        click.echo(click.style("\n[*] Activity monitoring stopped", fg='yellow'))


@cli.command()
@click.option('--device', default=None, help='Target device ID')
@click.option('--output', required=True, help='Output file for analysis results')
def app_analysis(device, output):
    """Analyze installed applications and permissions"""
    click.echo(click.style("[*] Analyzing installed applications...", fg='cyan'))
    arft = ARFT()
    arft.app_analyzer = AppAnalyzer(device)
    try:
        arft.app_analyzer.analyze(output)
        click.echo(click.style(f"[+] Analysis complete. Results saved to {output}", fg='green'))
    except Exception as e:
        click.echo(click.style(f"[!] Analysis failed: {str(e)}", fg='red'))


@cli.command()
@click.option('--device', default=None, help='Target device ID')
@click.option('--output', required=True, help='Output file for memory dump')
def memory_dump(device, output):
    """Extract device memory for analysis"""
    click.echo(click.style("[*] Extracting device memory...", fg='cyan'))
    arft = ARFT()
    arft.memory_analyzer = MemoryAnalyzer(device)
    try:
        arft.memory_analyzer.dump_memory(output)
        click.echo(click.style(f"[+] Memory dump saved to {output}", fg='green'))
    except Exception as e:
        click.echo(click.style(f"[!] Memory dump failed: {str(e)}", fg='red'))


@cli.command()
@click.option('--device', default=None, help='Target device ID')
@click.option('--interface', default='wlan0', help='Network interface to monitor')
@click.option('--output', required=True, help='Output file for pcap data')
def network_monitor_cmd(device, interface, output):
    """Capture and monitor network traffic"""
    click.echo(click.style("[*] Starting network monitoring...", fg='cyan'))
    arft = ARFT()
    arft.network_monitor = NetworkMonitor(device, interface)
    try:
        arft.network_monitor.start_capture(output)
    except KeyboardInterrupt:
        click.echo(click.style("\n[*] Network monitoring stopped", fg='yellow'))


@cli.command()
@click.option('--device', default=None, help='Target device ID')
@click.option('--output', required=True, help='Output directory for recovered data')
def data_recovery_cmd(device, output):
    """Recover deleted files and data"""
    click.echo(click.style("[*] Starting data recovery...", fg='cyan'))
    arft = ARFT()
    arft.data_recovery = DataRecovery(device)
    try:
        arft.data_recovery.recover(output)
        click.echo(click.style(f"[+] Recovery complete. Results saved to {output}", fg='green'))
    except Exception as e:
        click.echo(click.style(f"[!] Recovery failed: {str(e)}", fg='red'))


@cli.command()
def about():
    """Display tool information"""
    click.echo("""
╔════════════════════════════════════════════════════════════╗
║     Android Remote Forensics Tool (ARFT) v1.0              ║
║     Remote Access, Control & Forensic Analysis for Android ║
║                                                            ║
║  Author: rocketyou02-coder                                ║
║  License: MIT                                              ║
║  Purpose: Security Testing & Forensic Analysis             ║
║                                                            ║
║  ⚠️  LEGAL NOTICE:                                         ║
║  Unauthorized device access is illegal.                   ║
║  Only use this tool with proper authorization.             ║
╚════════════════════════════════════════════════════════════╝
    """)


if __name__ == '__main__':
    if os.geteuid() != 0:
        print("[!] This tool must be run with sudo/root privileges")
        sys.exit(1)
    cli()
