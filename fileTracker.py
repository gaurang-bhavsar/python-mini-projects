#!/usr/bin/env python3
"""
File Tracker - A utility to monitor and track file changes in a directory
"""

import os
import time
import logging
import argparse
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Set, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("file_tracker.log"),
        logging.StreamHandler()
    ]
)

class FileTracker:
    """
    A class to track file changes in a directory
    """
    
    def __init__(self, directory: str, recursive: bool = False, ignore_patterns: list = None):
        """
        Initialize the FileTracker
        
        Args:
            directory: The directory to monitor
            recursive: Whether to monitor subdirectories
            ignore_patterns: List of patterns to ignore
        """
        self.directory = os.path.abspath(directory)
        self.recursive = recursive
        self.ignore_patterns = ignore_patterns or []
        self.file_states: Dict[str, Dict] = {}
        self.running = False
        
        if not os.path.exists(self.directory):
            raise ValueError(f"Directory '{self.directory}' does not exist")
        
        logging.info(f"Initializing file tracker for {self.directory}")
        logging.info(f"Recursive mode: {self.recursive}")
        if self.ignore_patterns:
            logging.info(f"Ignoring patterns: {', '.join(self.ignore_patterns)}")
    
    def _get_file_hash(self, file_path: str) -> str:
        """
        Calculate MD5 hash of a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            MD5 hash of the file
        """
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logging.error(f"Error calculating hash for {file_path}: {e}")
            return ""
    
    def _get_file_info(self, file_path: str) -> Dict:
        """
        Get file information
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        stat = os.stat(file_path)
        return {
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "hash": self._get_file_hash(file_path),
            "last_checked": time.time()
        }
    
    def _should_ignore(self, path: str) -> bool:
        """
        Check if a path should be ignored
        
        Args:
            path: Path to check
            
        Returns:
            True if the path should be ignored, False otherwise
        """
        for pattern in self.ignore_patterns:
            if pattern in path:
                return True
        return False
    
    def scan_directory(self) -> Dict[str, Dict]:
        """
        Scan the directory and get the current state of all files
        
        Returns:
            Dictionary with file paths as keys and file information as values
        """
        current_files = {}
        
        for root, dirs, files in os.walk(self.directory):
            # Skip directories if not recursive
            if not self.recursive and root != self.directory:
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.directory)
                
                # Skip ignored files
                if self._should_ignore(rel_path):
                    continue
                
                try:
                    current_files[rel_path] = self._get_file_info(file_path)
                except Exception as e:
                    logging.error(f"Error processing {file_path}: {e}")
        
        return current_files
    
    def detect_changes(self) -> Tuple[Set[str], Set[str], Set[str]]:
        """
        Detect changes between the current state and the previous state
        
        Returns:
            Tuple of (created, modified, deleted) file sets
        """
        current_files = self.scan_directory()
        
        # Find created and modified files
        created = set()
        modified = set()
        
        for file_path, info in current_files.items():
            if file_path not in self.file_states:
                created.add(file_path)
            elif (info["size"] != self.file_states[file_path]["size"] or 
                  info["modified"] != self.file_states[file_path]["modified"] or
                  info["hash"] != self.file_states[file_path]["hash"]):
                modified.add(file_path)
        
        # Find deleted files
        deleted = set(self.file_states.keys()) - set(current_files.keys())
        
        # Update file states
        self.file_states = current_files
        
        return created, modified, deleted
    
    def start_tracking(self, interval: int = 5):
        """
        Start tracking file changes
        
        Args:
            interval: Interval in seconds between checks
        """
        self.running = True
        self.file_states = self.scan_directory()
        logging.info(f"Initial scan complete. Found {len(self.file_states)} files.")
        
        try:
            while self.running:
                time.sleep(interval)
                created, modified, deleted = self.detect_changes()
                
                # Log changes
                for file_path in created:
                    logging.info(f"Created: {file_path}")
                
                for file_path in modified:
                    logging.info(f"Modified: {file_path}")
                
                for file_path in deleted:
                    logging.info(f"Deleted: {file_path}")
                
                if created or modified or deleted:
                    logging.info(f"Summary: {len(created)} created, {len(modified)} modified, {len(deleted)} deleted")
                
        except KeyboardInterrupt:
            logging.info("Tracking stopped by user")
            self.running = False
    
    def stop_tracking(self):
        """Stop tracking file changes"""
        self.running = False
        logging.info("Tracking stopped")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Track file changes in a directory")
    parser.add_argument("directory", help="Directory to monitor")
    parser.add_argument("-r", "--recursive", action="store_true", help="Monitor subdirectories")
    parser.add_argument("-i", "--interval", type=int, default=5, help="Check interval in seconds")
    parser.add_argument("--ignore", nargs="+", default=[], help="Patterns to ignore")
    
    args = parser.parse_args()
    
    try:
        tracker = FileTracker(args.directory, args.recursive, args.ignore)
        print(f"Starting file tracker for {args.directory}")
        print(f"Press Ctrl+C to stop tracking")
        tracker.start_tracking(args.interval)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
