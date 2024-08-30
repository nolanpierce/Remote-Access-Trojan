import os
from pathlib import Path
import pyminizip
import glob
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileManager:
    
    def __init__(self) -> None:
        self.home = str(Path.home())
        self.downloads = str(Path.home() / 'Downloads')
        self.desktop = str(Path.home() / 'Desktop')

    def get_home_path(self) -> str:
        return self.home
    
    def get_desktop_path(self) -> str:
        return self.desktop
    
    def get_downloads_path(self) -> str:
        return self.downloads

    @staticmethod
    def remove_file(file_path: str) -> bool:
        if not file_path:
            logging.error("File path is None or empty.")
            return False

        try: 
            os.remove(file_path)
            logging.info(f"File removed: {file_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to remove file: {file_path}. Error: {e}")
            return False

    @staticmethod
    def move_file(src_path: str, dest_path: str) -> bool:
        if not src_path or not dest_path:
            logging.error("Source or destination path is None or empty.")
            return False

        try:
            os.rename(src_path, dest_path)
            logging.info(f"File moved from {src_path} to {dest_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to move file from {src_path} to {dest_path}. Error: {e}")
            return False

    def list_files(self, directory: str) -> list:
        if not directory:
            logging.error("Directory path is None or empty.")
            return []

        try:
            files = glob.glob(f'{directory}/*')
            logging.info(f"Listed files in directory: {directory}")
            return files
        except Exception as e:
            logging.error(f"Failed to list files in directory: {directory}. Error: {e}")
            return []

    def lock_files(self, files: list, output_zip: str, password: str) -> bool:
        """
        Creates a password-protected zip file for all files in the list.

        Parameters:
            files (list): A list of file paths to be compressed and encrypted.
            output_zip (str): The path where the output encrypted file should be saved.
            password (str): The encryption password.

        Returns:
            bool: True if the files were successfully locked, False otherwise.
        """
        try:
            # Compress and password-protect multiple files into a single zip
            pyminizip.compress_multiple(files, [], output_zip, password, 5)
            logging.info(f"Files zipped and password protected: {output_zip}")
            return True
        except Exception as e:
            logging.error(f"Failed to lock files. Error: {e}")
            return False

