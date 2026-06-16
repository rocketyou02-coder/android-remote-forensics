"""
ARFT Modules Package
Contains all forensic analysis and control modules
"""

from modules.device_manager import DeviceManager
from modules.screen_mirror import ScreenMirror
from modules.file_extraction import FileExtraction
from modules.activity_monitor import ActivityMonitor
from modules.app_analyzer import AppAnalyzer
from modules.memory_analyzer import MemoryAnalyzer
from modules.network_monitor import NetworkMonitor
from modules.data_recovery import DataRecovery

__all__ = [
    'DeviceManager',
    'ScreenMirror',
    'FileExtraction',
    'ActivityMonitor',
    'AppAnalyzer',
    'MemoryAnalyzer',
    'NetworkMonitor',
    'DataRecovery',
]

__version__ = '1.0.0'
__author__ = 'rocketyou02-coder'