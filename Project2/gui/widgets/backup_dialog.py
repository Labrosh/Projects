import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from utils.backup_manager import BackupManager

class BackupDialog(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("Backup and Restore")
        self.geometry("500x450")  # Increased height from 400 to 450
        self.minsize(500, 450)    # Also increased minimum height
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        style = ttk.Style()
        style.configure("Header.TLabel", font=('Helvetica', 12, 'bold'))
        style.configure("Info.TLabel", font=('Helvetica', 10))

        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Backup section
        backup_frame = ttk.LabelFrame(main_frame, text="Backup", padding="15")
        backup_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(backup_frame, 
                 text="Create a backup of your movie collection",
                 style="Header.TLabel").pack(pady=(0, 5))
        
        ttk.Label(backup_frame, 
                 text="This will save your movie list, posters, and all cached data\n"
                      "to a single file that you can restore later.",
                 style="Info.TLabel",
                 justify="left").pack(pady=(0, 10))
        
        ttk.Button(backup_frame, 
                  text="Create Backup", 
                  command=self.create_backup,
                  width=20).pack()

        # Restore section
        restore_frame = ttk.LabelFrame(main_frame, text="Restore", padding="15")
        restore_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        ttk.Label(restore_frame, 
                 text="Restore from a backup file",
                 style="Header.TLabel").pack(pady=(0, 5))
        
        ttk.Label(restore_frame, 
                 text="Select a previous backup file to restore your movie collection.\n"
                      "This will replace your current data with the backup's contents.\n"
                      "Your current data will be lost.",
                 style="Info.TLabel",
                 justify="left").pack(pady=(0, 10))
        
        ttk.Button(restore_frame, 
                  text="Restore from Backup",
                  command=self.restore_backup,
                  width=20).pack()

        # Close button at bottom
        ttk.Button(main_frame, 
                  text="Close",
                  command=self.destroy,
                  width=20).pack(pady=(0, 5))

        self.center_window()

    def create_backup(self):
        try:
            backup_file = BackupManager.create_backup()
            messagebox.showinfo("Success", 
                              f"Backup created successfully!\n\n"
                              f"Location: {backup_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}")

    def restore_backup(self):
        try:
            backup_file = filedialog.askopenfilename(
                title="Select Backup File",
                filetypes=[("ZIP files", "*.zip")],
                initialdir="backups"
            )
            if backup_file:
                if messagebox.askyesno("Confirm Restore", 
                                     "This will replace your current data with the backup.\n"
                                     "Your current data will be lost.\n\n"
                                     "Are you sure you want to continue?"):
                    BackupManager.restore_backup(backup_file)
                    # Reload the MovieManager data
                    self.app.movie_manager.load_data()
                    # Force refresh of the UI
                    self.app.load_movies()
                    messagebox.showinfo("Success", "Backup restored successfully!")
                    self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore backup: {str(e)}")

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
