import os
import shutil
import zipfile
import logging
from datetime import datetime

class BackupManager:
    @staticmethod
    def create_backup(base_dir="data", backup_dir="backups"):
        """Create a backup of all movie data and cache"""
        try:
            # Create backups directory if it doesn't exist
            os.makedirs(backup_dir, exist_ok=True)
            
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"movie_tracker_backup_{timestamp}.zip")
            
            # Create zip file
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add movies.json
                if os.path.exists(os.path.join(base_dir, "movies.json")):
                    zipf.write(os.path.join(base_dir, "movies.json"), "movies.json")
                
                # Add posters directory
                posters_dir = os.path.join(base_dir, "posters")
                if os.path.exists(posters_dir):
                    for root, _, files in os.walk(posters_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, base_dir)
                            zipf.write(file_path, arcname)
                
                # Add cache directory
                cache_dir = os.path.join(base_dir, "cache")
                if os.path.exists(cache_dir):
                    for root, _, files in os.walk(cache_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, base_dir)
                            zipf.write(file_path, arcname)
            
            logging.info(f"Backup created successfully: {backup_file}")
            return backup_file
            
        except Exception as e:
            logging.error(f"Failed to create backup: {e}")
            raise

    @staticmethod
    def restore_backup(backup_file, data_dir="data"):
        """Restore from a backup file"""
        try:
            # First, ensure the data directory exists
            os.makedirs(data_dir, exist_ok=True)
            
            # Create temporary extraction directory inside data dir
            temp_dir = os.path.join(data_dir, "temp_restore")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Extract backup
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Remove existing data files but keep the directory
            for item in os.listdir(data_dir):
                item_path = os.path.join(data_dir, item)
                if item != "temp_restore":  # Don't delete the temp directory
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
            
            # Move restored data to proper location
            for item in os.listdir(temp_dir):
                src_path = os.path.join(temp_dir, item)
                dst_path = os.path.join(data_dir, item)
                if os.path.exists(dst_path):
                    if os.path.isdir(dst_path):
                        shutil.rmtree(dst_path)
                    else:
                        os.remove(dst_path)
                shutil.move(src_path, dst_path)
            
            # Clean up temp directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
            logging.info(f"Backup restored successfully from: {backup_file}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to restore backup: {e}")
            raise
