import sys
import os
import shutil
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication, QMessageBox
from PyQt6.QtCore import Qt

# Name of the folder containing the application files in the PyInstaller bundle
SOURCE_FOLDER_NAME = "Easy Payload"
# Name of the destination folder on the user's home page
DESTINATION_FOLDER_NAME = "Easy Payload"
# Name of the link file on the Desktop
SHORTCUT_NAME = "Easy Payload.lnk"
# Source link file name (dentro SOURCE_FOLDER_NAME)
SOURCE_SHORTCUT_FILENAME = "Easy Payload.lnk" 
# application icon
APP_ICON = "icon.ico"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Window settings ---
        self.setWindowTitle("Easy Payload Setup")
        self.setFixedSize(300, 270)
        self.setStyleSheet("QMainWindow { background-color: #cccccc; }")
        try:
            # Determines the base path (for PyInstaller or direct script)
            if getattr(sys, 'frozen', False):
                # When run as a PyInstaller bundle
                self.base_path = sys._MEIPASS
            else:
                # If run as a .py script
                self.base_path = os.path.dirname(os.path.abspath(__file__))

            icon_path = os.path.join(self.base_path, APP_ICON)
            if os.path.exists(icon_path):
                 self.setWindowIcon(QtGui.QIcon(icon_path))
            else:
                 print(f"Warning: icon not found in {icon_path}")

        except Exception as e:
            print(f"Error setting icon: {e}")

        # --- Calculated paths ---
        # Full path of the source folder (in bundle or local)
        self.source_path = os.path.join(self.base_path, SOURCE_FOLDER_NAME)
        # Full path of the destination folder
        self.destination_path = os.path.join(os.path.expanduser("~"), DESTINATION_FOLDER_NAME)
        # Full path to the source link file
        self.source_link_path = os.path.join(self.source_path, SOURCE_SHORTCUT_FILENAME)
        # Full path to the link file on the Desktop
        self.destination_link_path = os.path.join(os.path.expanduser("~"), "Desktop", SHORTCUT_NAME)

        # --- Widget GUI ---
        self.title_label = QLabel("Application Setup", self)
        self.title_label.setStyleSheet("font-size: 20px; color: #000000; font-weight: bold; font-family: 'Arial';")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setGeometry(0, 10, 300, 40)

        self.text_label = QLabel("To install Easy Payload press 'Install'.\nTo uninstall press 'Uninstall'.", self)
        self.text_label.setStyleSheet("font-size: 12px; color: #000000; font-family: 'Arial';")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        self.text_label.setGeometry(10, 50, 280, 60)

        self.install_button = QPushButton("Install", self)
        self.install_button.setStyleSheet("QPushButton { font-size: 12px; font-weight: bold; color: #FFFFFF; font-family: 'Arial'; background-color: lightgreen; border: 0px solid lightgreen; border-radius: 3px; } QPushButton:hover { background-color: #90EE90; } QPushButton:pressed { background-color: #32CD32; }")
        self.install_button.setGeometry(85, 125, 130, 30)
        # Correct connection using lambda
        self.install_button.clicked.connect(self.install_program)

        self.uninstall_button = QPushButton("Uninstall", self)
        self.uninstall_button.setStyleSheet("QPushButton { font-size: 12px; font-weight: bold; color: #FFFFFF; font-family: 'Arial'; background-color: #D2042D; border: 0px solid #D2042D; border-radius: 3px; } QPushButton:hover { background-color: #DC143C; } QPushButton:pressed { background-color: #FF0000; }")
        self.uninstall_button.setGeometry(85, 165, 130, 30)
        self.uninstall_button.clicked.connect(self.uninstall_program)

        self.status_label = QLabel("", self) # Status message label
        self.status_label.setStyleSheet("font-size: 10px; color: grey; font-family: 'Arial';")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setGeometry(10, 210, 280, 40)

    def show_message(self, title, text, icon=QMessageBox.Icon.Information):
        """Show message popup."""
        msgBox = QMessageBox(self) # Associate with parent
        msgBox.setIcon(icon)
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()

    def install_program(self):
        """Install the application."""
        self.status_label.setText("Installation in progress...")
        QApplication.processEvents() # Update the GUI

        try:
            # Check if the source folder exists
            if not os.path.exists(self.source_path):
                self.show_message("Error during installation",
                                  f"Source folder not found:\n{self.source_path}\nThe installer can be corrupted.",
                                  QMessageBox.Icon.Critical)
                self.status_label.setText("Installation failed.")
                return

            # Check if the destination folder already exists
            if os.path.exists(self.destination_path):
                reply = QMessageBox.question(self, "Exisisting destination",
                                             f"The folder '{self.destination_path}' already exists.\nWant to overwrite it? (WARNING: the content will be deleted)",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    print(f"Deleting existing folder: {self.destination_path}")
                    try:
                        shutil.rmtree(self.destination_path)
                    except Exception as e:
                        self.show_message("Installation Error",
                                          f"Unable to remove the existing folder:\n{e}",
                                          QMessageBox.Icon.Warning)
                        self.status_label.setText("Installation failed.")
                        return # Stop installation if it cannot be removed
                else:
                    self.status_label.setText("Installation aborted by user.")
                    return # Stop installation by user

            # 1. Copy the main application folder
            print(f"Copia da '{self.source_path}' a '{self.destination_path}'")
            shutil.copytree(self.source_path, self.destination_path)
            print("Copy completed folder.")

            # 2. Copy the link to the Desktop (if the source exists)
            if os.path.exists(self.source_link_path):
                 # Removes any existing links on the desktop
                 if os.path.exists(self.destination_link_path):
                     try:
                         os.remove(self.destination_link_path)
                     except Exception as e:
                         print(f"Warning: Unable to remove the existent link '{self.destination_link_path}': {e}")

                 print(f"Copy link from '{self.source_link_path}' to '{self.destination_link_path}'")
                 shutil.copy2(self.source_link_path, self.destination_link_path) # copy2 preserves metadata
                 print("Copy link completed")
            else:
                 print(f"Warning: Source link file not found: {self.source_link_path}. Link not created.")
                 self.show_message("Installation Notice",
                                   "Link on Desktop not created (source file not found).",
                                   QMessageBox.Icon.Warning)


            self.status_label.setText("Installation completed successfully!")
            self.show_message("Installation Completed",
                              f"Easy Payload has been successfully installed in:\n{self.destination_path}",
                              QMessageBox.Icon.Information)

        except Exception as e:
            self.status_label.setText("Error during installation.")
            self.show_message("Installation Error",
                              f"An error has occurred:\n{e}",
                              QMessageBox.Icon.Critical)
            # Try cleaning in case of partial error (optional)
            if os.path.exists(self.destination_path):
                try:
                    shutil.rmtree(self.destination_path)
                except: pass # Ignore errors during cleaning

    def uninstall_program(self):
        """Uninstall the application."""
        self.status_label.setText("Uninstalling...")
        QApplication.processEvents() # Update the GUI

        removed_folder = False
        removed_link = False
        errors = []

        # Removes the application folder
        if os.path.exists(self.destination_path):
            try:
                shutil.rmtree(self.destination_path)
                print(f"Removed folder: {self.destination_path}")
                removed_folder = True
            except Exception as e:
                errors.append(f"Error removing folder '{self.destination_path}':\n{e}")
                print(errors[-1])
        else:
            print(f"The folder to be removed does not exist: {self.destination_path}")

        # Removes the link on the Desktop
        if os.path.exists(self.destination_link_path):
            try:
                os.remove(self.destination_link_path)
                print(f"Removed link: {self.destination_link_path}")
                removed_link = True
            except Exception as e:
                errors.append(f"Error removing link '{self.destination_link_path}':\n{e}")
                print(errors[-1])
        else:
            print(f"The link to be removed does not exist: {self.destination_link_path}")


        if not errors:
             self.status_label.setText("Uninstallation completed.")
             self.show_message("Uninstallation completed.",
                               "Easy Payload has been uninstalled.",
                               QMessageBox.Icon.Information)
        else:
             self.status_label.setText("Error uninstalling.")
             error_message = "One or more errors occurred:\n\n" + "\n\n".join(errors)
             self.show_message("Uninstallation Error", error_message, QMessageBox.Icon.Warning)


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
# Pyinstaller Prompt
#pyinstaller --onefile --windowed --icon="icon.ico" --hidden-import=PyQt6 --add-data "Easy Payload;Easy Payload" --add-data "icon.ico;." --exclude PyQt5 "Easy Payload setup.py"
