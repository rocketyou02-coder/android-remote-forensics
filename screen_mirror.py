#!/usr/bin/env python3
"""
Screen Mirror Module
Captures and displays Android device screen in real-time
"""

import subprocess
import threading
import logging
from PIL import Image
from io import BytesIO
import time

logger = logging.getLogger(__name__)


class ScreenMirror:
    """Mirror Android device screen"""
    
    def __init__(self, device: str = None, fps: int = 30):
        self.device = device or self._get_default_device()
        self.fps = fps
        self.running = False
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
    
    def capture_frame(self) -> Image.Image:
        """Capture single frame from device"""
        try:
            cmd = [self.adb_path, '-s', self.device, 'shell', 'screencap', '-p']
            result = subprocess.run(cmd, capture_output=True, timeout=5)
            
            if result.returncode == 0:
                image = Image.open(BytesIO(result.stdout))
                return image
        except Exception as e:
            logger.error(f"Error capturing frame: {e}")
        return None
    
    def start(self):
        """Start screen mirroring"""
        if not self.device:
            logger.error("No device connected")
            return
        
        self.running = True
        logger.info(f"Starting screen mirror from {self.device}")
        
        try:
            import cv2
            cv2.namedWindow('Android Screen Mirror', cv2.WINDOW_AUTOSIZE)
            
            while self.running:
                frame = self.capture_frame()
                if frame:
                    frame_array = np.array(frame)
                    cv2.imshow('Android Screen Mirror', frame_array)
                    
                    if cv2.waitKey(int(1000/self.fps)) & 0xFF == ord('q'):
                        break
                else:
                    time.sleep(0.1)
            
            cv2.destroyAllWindows()
        except ImportError:
            logger.error("OpenCV not installed. Install with: pip install opencv-python")
        except KeyboardInterrupt:
            logger.info("Screen mirroring stopped")
        finally:
            self.running = False
    
    def capture_screenshot(self, output_path: str) -> bool:
        """Capture and save single screenshot"""
        try:
            frame = self.capture_frame()
            if frame:
                frame.save(output_path)
                logger.info(f"Screenshot saved to {output_path}")
                return True
        except Exception as e:
            logger.error(f"Error saving screenshot: {e}")
        return False
    
    def stop(self):
        """Stop screen mirroring"""
        self.running = False
        logger.info("Screen mirroring stopped")
