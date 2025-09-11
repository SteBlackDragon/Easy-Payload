import sys
import os
import PyQt6.QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

csv_path = None
bin_type=None
recursive_packing=None

# Finestra di dialogo per arresto anomalo
class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(PyQt6.QtGui.QIcon(self.get_icon_path()))
        self.setWindowTitle("Arresto anomalo")
        self.setFixedSize(350, 130)
        layout = QVBoxLayout()
        error1_label = QLabel("Errore:")
        error1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(error1_label)
        error2_label = QLabel("Controlla che i campi csv inseriti siano corretti\n")
        error2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(error2_label)
        ok_button = QPushButton("Chiudi")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        self.setLayout(layout)
    
    # Funzione per ottenere il percorso dell'icona
    def get_icon_path(self):
        if hasattr(sys, '_MEIPASS'):
            # Se l'applicazione è eseguita come un bundle PyInstaller
            return os.path.join(sys._MEIPASS, "icon.ico")
        else:
            # Se l'applicazione è eseguita normalmente
            return "img/icon.ico"

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Inizializza la finestra principale
        self.setWindowTitle("Easy Payload")
        self.setFixedSize(520, 270)
        self.setWindowIcon(PyQt6.QtGui.QIcon(self.get_icon_path()))
        self.setStyleSheet("background-color: #F5F5F5;")
        self.settings_window = 0

        # Scritta di benvenuto
        self.welcome_label = QLabel("Benvenuto su Easy Payload", self)
        self.welcome_label.setStyleSheet("font-size: 20px; color: #000000; font-family: 'Arial'")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setGeometry(0, -10, 520, 100)
        self.autor_label = QLabel("By Turco Stefano", self)
        self.autor_label.setStyleSheet("font-size: 10px; color: #000000; font-family: 'Arial';")
        self.autor_label.setGeometry(220,55,90,20)
        
        # Selezione del file CSV 
        self.file_label= QLabel("File CSV:",self)
        self.file_label.setStyleSheet("font-size: 12px; color: #000000; margin-top: 15px; margin-left: 15px; font-family: 'Arial';")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.file_label.setGeometry(0, 85, 520, 100)

        self.file_LineEdit = QLineEdit(self)
        self.file_LineEdit.setPlaceholderText("Inserisci il percorso del file CSV")
        self.file_LineEdit.setStyleSheet("font-size: 12px; color: #000000; margin-top:12px; margin-left: 70px; font-family: 'Arial';")
        self.file_LineEdit.setGeometry(0, 85, 400, 30)
        self.file_LineEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.file_browse_button = QPushButton("Sfoglia", self)
        self.file_browse_button.setStyleSheet("QPushButton {font-size: 12px; color: #000000; font-family: 'Arial'; background-color: #84fa84;} QPushButton:checked {background-color: #64e986; color: #000000} QPushButton:pressed {background-color: #64e986; color: #000000}")
        self.file_browse_button.setGeometry(400,95, 100, 23)
        self.file_browse_button.clicked.connect(self.browse_file)

        # Menù per la selezione del tipo di trasporto
        self.transport_label= QLabel("seleziona il tipo di trasporto:",self)
        self.transport_label.setStyleSheet("font-size: 12px; color: #000000; margin-top: 15px; margin-left: 15px; font-family: 'Arial';")
        self.transport_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.transport_label.setGeometry(0, 130, 320, 100)

        self.trasport_select= QComboBox(self)
        self.trasport_select.setStyleSheet("font-size: 12px; color: #000000; margin-top:12px; font-family: 'Arial';")
        self.trasport_select.setGeometry(176, 131, 250, 30)
        self.trasport_select.setPlaceholderText("Seleziona qui")
        self.trasport_select.addItem("Container")
        self.trasport_select.addItem("Camion Motrice")
        self.trasport_select.addItem("Camion Bilico")
        self.trasport_select.currentIndexChanged.connect(self.select_bin)

        
        # Pulsante per accedere alla finestra di configurazione campi CSV
        self.settings_button_label= QLabel("Imposta i campi CSV:",self)
        self.settings_button_label.setStyleSheet("font-size: 12px; color: #000000; margin-top: 15px; margin-left: 15px; font-family: 'Arial';")
        self.settings_button_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settings_button_label.setGeometry(0, 175, 520, 100)

        self.settings_button= QPushButton("clicca qui", self)
        self.settings_button.setStyleSheet("font-size: 12px; color: #000000; background-color: lightgreen; border: 1px solid #adacb1; border-radius: 3px; margin-top:12px; margin-left:70px; font-family: 'Arial';")
        self.settings_button.setGeometry(70, 175, 150, 30)
        self.settings_button.setCheckable(True)
        self.settings_button.clicked.connect(self.get_settings_button)

        # Pulsante per avviare il programma
        self.start_button = QPushButton("Avvia", self)
        self.start_button.setStyleSheet("QPushButton { font-size: 12px; color: #000000; font-family: 'Arial'; background-color: #84fa84; border: 0px solid #adacb1; border-radius: 3px; } QPushButton:checked { background-color: #64e986;  color: #000000; border: 0px solid #DAA520; } QPushButton:pressed { background-color: #84fa84; }")
        self.start_button.setGeometry(80, 230, 360, 30)
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.get_run_button)
        
    # Funzione per ottenere il percorso dell'icona
    def get_icon_path(self):
        if hasattr(sys, '_MEIPASS'):
            # Se l'applicazione è eseguita come un bundle PyInstaller
            return os.path.join(sys._MEIPASS, "icon.ico")
        else:
            # Se l'applicazione è eseguita normalmente
            return "img/icon.ico"
        
    #Estrae il percorso del file CSV
    def browse_file(self):
        global csv_path
        file_path_tuple = QFileDialog.getOpenFileName(
            self,
            "Seleziona un file CSV",
            os.getcwd(),
            "CSV Files (*.csv);"
        )

        file_path = file_path_tuple[0]

        if file_path:
            self.file_LineEdit.setText(file_path)
            csv_path = file_path
            #print(csv_path)
        else:
            self.file_LineEdit.setText("Scegliere un file csv")
            self.file_LineEdit.setStyleSheet("font-size: 12px; color: black; margin-top:12px; margin-left:70px; font-family: 'Arial';")
        return csv_path
    
    #Estrae il tipo di trasporto
    def select_bin(self):
        global bin_type
        if self.trasport_select.currentText() == "Container":
            bin_type="Container"
        elif self.trasport_select.currentText() == "Camion Motrice":
            bin_type="Camion Motrice"
        elif self.trasport_select.currentText() == "Camion Bilico":
            bin_type="Camion Bilico"
        else:
            bin_type="Container"
        return bin_type
    
    # Raccoglie l'input per aprire òa finestra di configurazione campi CSV
    def get_settings_button(self):
        if self.settings_button.isChecked():
            self.settings_window = None
            if self.settings_window is None:
                self.settings_window = SettingsWindow()
            self.settings_window.show()
            
    
    # Avvia il programma ed estrae i valori dalla GUI
    def get_run_button(self, bin_type=select_bin):
            if self.start_button.isChecked():
                csv_path = self.file_LineEdit.text() #Percorso del file CSV
                bin_type = self.select_bin() #Tipo di trasporto
                self.start_button.setText("In Esecuzione...")
                from extract_data import exec as extract_data_exec
                from visualize_packing import exec as visualize_packing_exec
                
                #exist= os.path.isfile(txt_path)
                
                current_path=os.getcwd() 
                global txt_path
                txt_path=os.path.join(current_path, "csv_settings.txt") #recupera il percorso del file di testo di configurazione
                
                if os.path.isfile(txt_path) == False:
                    self.settings_button.setChecked(True)
                    self.get_settings_button()
                
                if csv_path and bin_type is not None:
                    if os.path.isfile(txt_path) == True:
                        try:
                            container3d, items3d=extract_data_exec(csv_path, txt_path, bin_type) #Avvia il programma di estrazione dati
                            visualize_packing_exec(container3d,items3d) #Avvia il programma di visualizzazione 3D
                        except Exception:
                            app = QApplication.instance()
                            if app is None:
                                app = QApplication(sys.argv)
                            dialog = MyDialog()
                            dialog.exec()
                            #if app is None:
                                #sys.exit()
                    
                    # Creazione piani di carico ricorsivi con gli item scartati
                        from visualize_packing import unfitted_items
                        if len(unfitted_items) > 0:
                            visualize_packing_exec(container3d,unfitted_items)

                            from visualize_packing import unfitted_items
                            if len(unfitted_items) > 0:
                                visualize_packing_exec(container3d,unfitted_items)

                                from visualize_packing import unfitted_items
                                if len(unfitted_items) > 0:
                                    visualize_packing_exec(container3d,unfitted_items)
                    else:
                        self.settings_button.setChecked(True)
                        self.get_settings_button()


                    # impostazione iniziale GUI 
                    self.file_LineEdit.setText("")
                    self.trasport_select.setPlaceholderText("Seleziona qui")
                    self.start_button.setChecked(False)
                    self.start_button.setText("Avvia")

                else:
                    self.start_button.setText("Errore: dati non validi")
                    self.start_button.setStyleSheet("QPushButton { font-size: 12px; color: #000000; font-family: 'Arial'; background-color: #84fa84; border: 0px solid #adacb1; border-radius: 3px; } QPushButton:checked { background-color: #84fa84;  color: red; font-weight: bold; border: 0px solid #DAA520; } QPushButton:pressed { background-color: #84fa84; }")

            elif self.start_button.isChecked() == False:
                self.start_button.setText("Avvia")

# Inizializzazione finestra di configurazione          
class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configurazione campi csv")
        self.setFixedSize(420, 240)
        self.setWindowIcon(PyQt6.QtGui.QIcon(self.get_icon_path()))
        self.setStyleSheet("background-color: #F5F5F5;")
        
        # Scritta informativa
        self.info_label = QLabel("Inseririsci il nome dei campi csv associati a questi dati:", self)
        self.info_label.setStyleSheet("font-size: 14px; color: #000000; font-family: 'Arial'")
        self.info_label.setGeometry(5, 5, 420, 30)
        
        # Input nome campo csv
        self.id_label = QLabel("Codice identificativo:", self)
        self.id_label.setStyleSheet("font-size: 12px; color: #000000; font-family: 'Arial;'")
        self.id_label.setGeometry(5, 55, 110, 20)
        
        self.id_lineEdit = QLineEdit(self)
        self.id_lineEdit.setStyleSheet("font-size: 12px; color: #000000; font-family: 'Arial'")
        self.id_lineEdit.setGeometry(120, 55, 250, 20)
        self.id_lineEdit.setPlaceholderText("Inserisci qui il nome del campo")
        
        # Input nome campo csv
        self.largh_label = QLabel("Larghezza oggetto:", self)
        self.largh_label .setStyleSheet("font-size: 12px; color: #000000; font-family: 'Arial'")
        self.largh_label .setGeometry(5, 85, 100, 20)
        
        self.largh_lineEdit = QLineEdit(self)
        self.largh_lineEdit.setStyleSheet("font-size: 12px; color: #000000; font-family: 'Arial'")
        self.largh_lineEdit.setGeometry(120, 85, 250, 20)
        self.largh_lineEdit.setPlaceholderText("Inserisci qui il nome del campo")
        
        # Input nome campo csv
        self.lungh_label = QLabel("Lunghezza oggetto:", self)
        self.lungh_label.setStyleSheet("font-size: 12px; color: #000000; font-family: 'Arial'")
        self.lungh_label.setGeometry(5, 115, 102, 20)
        
        self.lungh_lineEdit = QLineEdit(self)
        self.lungh_lineEdit.setStyleSheet("font-size: 12px; color: #000000; font-family: 'Arial'")
        self.lungh_lineEdit.setGeometry(120, 115, 250, 20)
        self.lungh_lineEdit.setPlaceholderText("Inserisci qui il nome del campo")
        
        # Input nome campo csv
        self.altezza_label = QLabel("Altezza oggetto:", self)
        self.altezza_label.setStyleSheet("font-size: 12px; color: #000000; font-family: 'Arial'")
        self.altezza_label.setGeometry(15, 145, 100, 20)
        
        self.altezza_lineEdit = QLineEdit(self)
        self.altezza_lineEdit.setStyleSheet("font-size: 12px; color: #000000; font-family: 'Arial'")
        self.altezza_lineEdit.setGeometry(120, 145, 250, 20)
        self.altezza_lineEdit.setPlaceholderText("Inserisci qui il nome del campo")
        
        # Input nome campo csv
        self.peso_label = QLabel("Peso oggetto:", self)
        self.peso_label.setStyleSheet("font-size: 12px; color: #000000; font-family: 'Arial'")
        self.peso_label.setGeometry(15, 175, 100, 20)
        
        self.peso_lineEdit = QLineEdit(self)
        self.peso_lineEdit.setStyleSheet("font-size: 12px; color: #000000; font-family: 'Arial'")
        self.peso_lineEdit.setGeometry(120, 175, 250, 20)
        self.peso_lineEdit.setPlaceholderText("Inserisci qui il nome del campo")
        
        # Pulsante per cancellare i campi
        self.delete_button= QPushButton("Cancella", self)
        self.delete_button.setStyleSheet("font-size: 12px; color: #000000; background-color: #84fa84; border: 1px solid #adacb1; border-radius: 3px; margin-top:12px; margin-left:70px; font-family: 'Arial';")
        self.delete_button.setCheckable(True)
        self.delete_button.setGeometry(250, 200, 150, 30)
        self.delete_button.clicked.connect(self.get_delete_button)
        
        # Pulsante per salvare i campi e chiudere la finestra
        self.exit_button= QPushButton("Salva", self)
        self.exit_button.setStyleSheet("font-size: 12px; color: #000000; background-color: #84fa84; border: 1px solid #adacb1; border-radius: 3px; margin-top:12px; margin-left:70px; font-family: 'Arial';")
        self.exit_button.setGeometry(165, 200, 150, 30)
        self.exit_button.setCheckable(True)
        self.exit_button.clicked.connect(self.get_exit_button)
        
    # Funzione per ottenere il percorso dell'icona
    def get_icon_path(self):
        if hasattr(sys, '_MEIPASS'):
            # Se l'applicazione è eseguita come un bundle PyInstaller
            return os.path.join(sys._MEIPASS, "icon.ico")
        else:
            # Se l'applicazione è eseguita normalmente
            return "img/icon.ico"

    # Funzione per cancellare i campi al click del pulsante cancella
    def get_delete_button(self):
        if self.delete_button.isChecked():
            self.id_lineEdit.setPlaceholderText("Inserisci qui il nome del campo")
            self.id_lineEdit.clear()
            self.largh_lineEdit.setPlaceholderText("Inserisci qui il nome del campo")
            self.largh_lineEdit.clear()
            self.lungh_lineEdit.setPlaceholderText("Inserisci qui il nome del campo")
            self.lungh_lineEdit.clear()
            self.altezza_lineEdit.setPlaceholderText("Inserisci qui il nome del campo")
            self.altezza_lineEdit.clear()
            self.peso_lineEdit.setPlaceholderText("Inserisci qui il nome del campo")
            self.peso_lineEdit.clear()
    
    # Funzione per salvare i campi e chiudere la finestra al click del pulsante salva
    def get_exit_button(self):
        if self.exit_button.isChecked():
            global nome, lenght, depth, height, weight
            nome=self.id_lineEdit.text()
            lenght=self.largh_lineEdit.text()
            depth=self.lungh_lineEdit.text()
            height=self.altezza_lineEdit.text()
            weight=self.peso_lineEdit.text()
            
            current_path=os.getcwd() 
            global txt_path
            txt_path=os.path.join(current_path, "csv_settings.txt") #recupera il percorso del file di testo di configurazione

                # Crea il file txt di configurazione
            with open(txt_path, "w") as file:
                file.write(f"{nome}\n")
                file.write(f"{depth}\n")
                file.write(f"{lenght}\n")
                file.write(f"{weight}\n")
                file.write(f"{height}")
            
            self.close()
        
if __name__== "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

#Comando pyinstaller
#pyinstaller --onedir --windowed --add-data icon.ico:. --icon=icon.ico --hidden-import pandas --hidden-import plotly --hidden-import numpy --hidden-import PyQt6 --name="Easy Payload" --exclude PyQt5 main.py