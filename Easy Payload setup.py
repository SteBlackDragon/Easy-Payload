import sys
import os
import shutil
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication, QMessageBox
from PyQt6.QtCore import Qt

# Nome della cartella contenente i file dell'applicazione nel bundle PyInstaller
SOURCE_FOLDER_NAME = "Easy Payload"
# Nome della cartella di destinazione nella home dell'utente
DESTINATION_FOLDER_NAME = "Easy Payload"
# Nome del file di collegamento sul Desktop
SHORTCUT_NAME = "Easy Payload.lnk"
# Nome del file di collegamento sorgente (dentro SOURCE_FOLDER_NAME)
SOURCE_SHORTCUT_FILENAME = "Easy Payload.lnk" 
# Icona dell'applicazione
APP_ICON = "icon.ico"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Configurazione Finestra ---
        self.setWindowTitle("Easy Payload Setup")
        self.setFixedSize(300, 270)
        self.setStyleSheet("QMainWindow { background-color: #cccccc; }")
        try:
            # Determina il percorso base (per PyInstaller o script diretto)
            if getattr(sys, 'frozen', False):
                # Se eseguito come bundle PyInstaller
                self.base_path = sys._MEIPASS
            else:
                # Se eseguito come script .py
                self.base_path = os.path.dirname(os.path.abspath(__file__))

            icon_path = os.path.join(self.base_path, APP_ICON)
            if os.path.exists(icon_path):
                 self.setWindowIcon(QtGui.QIcon(icon_path))
            else:
                 print(f"Attenzione: Icona non trovata in {icon_path}")

        except Exception as e:
            print(f"Errore durante l'impostazione dell'icona: {e}")

        # --- Percorsi Calcolati ---
        # Percorso completo della cartella sorgente (nel bundle o locale)
        self.source_path = os.path.join(self.base_path, SOURCE_FOLDER_NAME)
        # Percorso completo della cartella di destinazione
        self.destination_path = os.path.join(os.path.expanduser("~"), DESTINATION_FOLDER_NAME)
        # Percorso completo del file di collegamento sorgente
        self.source_link_path = os.path.join(self.source_path, SOURCE_SHORTCUT_FILENAME)
        # Percorso completo del file di collegamento sul Desktop
        self.destination_link_path = os.path.join(os.path.expanduser("~"), "Desktop", SHORTCUT_NAME)

        # --- Widget GUI ---
        self.title_label = QLabel("Setup Applicazione", self)
        self.title_label.setStyleSheet("font-size: 20px; color: #000000; font-weight: bold; font-family: 'Arial';")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setGeometry(0, 10, 300, 40)

        self.text_label = QLabel("Per installare Easy Payload premi 'Installa'.\nPer disinstallare premi 'Disinstalla'.", self)
        self.text_label.setStyleSheet("font-size: 12px; color: #000000; font-family: 'Arial';")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        self.text_label.setGeometry(10, 50, 280, 60)

        self.install_button = QPushButton("Installa", self)
        self.install_button.setStyleSheet("QPushButton { font-size: 12px; font-weight: bold; color: #FFFFFF; font-family: 'Arial'; background-color: lightgreen; border: 0px solid lightgreen; border-radius: 3px; } QPushButton:hover { background-color: #90EE90; } QPushButton:pressed { background-color: #32CD32; }")
        self.install_button.setGeometry(85, 125, 130, 30)
        # Connessione corretta usando lambda
        self.install_button.clicked.connect(self.install_program)

        self.uninstall_button = QPushButton("Disinstalla", self)
        self.uninstall_button.setStyleSheet("QPushButton { font-size: 12px; font-weight: bold; color: #FFFFFF; font-family: 'Arial'; background-color: #D2042D; border: 0px solid #D2042D; border-radius: 3px; } QPushButton:hover { background-color: #DC143C; } QPushButton:pressed { background-color: #FF0000; }")
        self.uninstall_button.setGeometry(85, 165, 130, 30)
        self.uninstall_button.clicked.connect(self.uninstall_program)

        self.status_label = QLabel("", self) # Etichetta per messaggi di stato
        self.status_label.setStyleSheet("font-size: 10px; color: grey; font-family: 'Arial';")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setGeometry(10, 210, 280, 40)

    def show_message(self, title, text, icon=QMessageBox.Icon.Information):
        """Mostra un popup di messaggio."""
        msgBox = QMessageBox(self) # Associa al genitore
        msgBox.setIcon(icon)
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()

    def install_program(self):
        """Installa l'applicazione."""
        self.status_label.setText("Installazione in corso...")
        QApplication.processEvents() # Aggiorna la GUI

        try:
            # Controlla se la cartella sorgente esiste
            if not os.path.exists(self.source_path):
                self.show_message("Errore Installazione",
                                  f"Cartella sorgente non trovata:\n{self.source_path}\nL'installer potrebbe essere corrotto.",
                                  QMessageBox.Icon.Critical)
                self.status_label.setText("Installazione fallita.")
                return

            # Controlla se la cartella di destinazione esiste già
            if os.path.exists(self.destination_path):
                reply = QMessageBox.question(self, "Destinazione Esistente",
                                             f"La cartella '{self.destination_path}' esiste già.\nVuoi sovrascriverla? (ATTENZIONE: il contenuto verrà eliminato)",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    print(f"Rimozione cartella esistente: {self.destination_path}")
                    try:
                        shutil.rmtree(self.destination_path)
                    except Exception as e:
                        self.show_message("Errore Installazione",
                                          f"Impossibile rimuovere la cartella esistente:\n{e}",
                                          QMessageBox.Icon.Warning)
                        self.status_label.setText("Installazione fallita.")
                        return # Interrompe l'installazione se non si può rimuovere
                else:
                    self.status_label.setText("Installazione annullata dall'utente.")
                    return # Interrompe l'installazione

            # 1. Copia la cartella principale dell'applicazione
            print(f"Copia da '{self.source_path}' a '{self.destination_path}'")
            shutil.copytree(self.source_path, self.destination_path)
            print("Copia cartella completata.")

            # 2. Copia il collegamento sul Desktop (se esiste il sorgente)
            if os.path.exists(self.source_link_path):
                 # Rimuove eventuale link esistente sul desktop
                 if os.path.exists(self.destination_link_path):
                     try:
                         os.remove(self.destination_link_path)
                     except Exception as e:
                         print(f"Attenzione: impossibile rimuovere link esistente '{self.destination_link_path}': {e}")

                 print(f"Copia link da '{self.source_link_path}' a '{self.destination_link_path}'")
                 shutil.copy2(self.source_link_path, self.destination_link_path) # copy2 preserva i metadati
                 print("Copia link completata.")
            else:
                 print(f"Attenzione: File di collegamento sorgente non trovato: {self.source_link_path}. Link non creato.")
                 self.show_message("Avviso Installazione",
                                   "Collegamento sul Desktop non creato (file sorgente non trovato).",
                                   QMessageBox.Icon.Warning)


            self.status_label.setText("Installazione completata con successo!")
            self.show_message("Installazione Completata",
                              f"Easy Payload è stato installato con successo in:\n{self.destination_path}",
                              QMessageBox.Icon.Information)

        except Exception as e:
            self.status_label.setText("Errore durante l'installazione.")
            self.show_message("Errore Installazione",
                              f"Si è verificato un errore:\n{e}",
                              QMessageBox.Icon.Critical)
            # Prova a pulire in caso di errore parziale (opzionale)
            if os.path.exists(self.destination_path):
                try:
                    shutil.rmtree(self.destination_path)
                except: pass # Ignora errori durante la pulizia

    def uninstall_program(self):
        """Disinstalla l'applicazione."""
        self.status_label.setText("Disinstallazione in corso...")
        QApplication.processEvents() # Aggiorna la GUI

        removed_folder = False
        removed_link = False
        errors = []

        # Rimuove la cartella dell'applicazione
        if os.path.exists(self.destination_path):
            try:
                shutil.rmtree(self.destination_path)
                print(f"Cartella rimossa: {self.destination_path}")
                removed_folder = True
            except Exception as e:
                errors.append(f"Errore durante la rimozione della cartella '{self.destination_path}':\n{e}")
                print(errors[-1])
        else:
            print(f"La cartella da rimuovere non esiste: {self.destination_path}")

        # Rimuove il collegamento sul Desktop
        if os.path.exists(self.destination_link_path):
            try:
                os.remove(self.destination_link_path)
                print(f"Collegamento rimosso: {self.destination_link_path}")
                removed_link = True
            except Exception as e:
                errors.append(f"Errore durante la rimozione del collegamento '{self.destination_link_path}':\n{e}")
                print(errors[-1])
        else:
            print(f"Il collegamento da rimuovere non esiste: {self.destination_link_path}")


        if not errors:
             self.status_label.setText("Disinstallazione completata.")
             self.show_message("Disinstallazione Completata",
                               "Easy Payload è stato disinstallato.",
                               QMessageBox.Icon.Information)
        else:
             self.status_label.setText("Errore durante la disinstallazione.")
             error_message = "Si sono verificati uno o più errori:\n\n" + "\n\n".join(errors)
             self.show_message("Errore Disinstallazione", error_message, QMessageBox.Icon.Warning)


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
# Comando Pyinstaller
#pyinstaller --onefile --windowed --icon="icon.ico" --hidden-import=PyQt6 --add-data "Easy Payload;Easy Payload" --add-data "icon.ico;." --exclude PyQt5 "Easy Payload setup.py"