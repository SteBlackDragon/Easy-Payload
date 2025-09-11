import pandas as pd

def exec(csv_path, txt_path, bin_type):
    
    # Lista contenente gli oggetti del csv
    dati = []
    
    # Lista contenente gli oggetti per la visualizzazione 3D
    items_3d = []
    
    # Lista contentenente il contenitore
    container_3d = []
    
    # Estrae i nomi delle colonne del csv dal file di txt di configurazione
    try:
        with open(txt_path, 'r') as file:
            lines = file.readlines()
            nome = lines[0].strip()
            depth = lines[1].strip()
            lenght = lines[2].strip()
            weight = lines[3].strip()
            height = lines[4].strip() 
    except FileNotFoundError:
        print("Error: TXT file not found")
    except IndexError:
        print("Error: TXT file does not contain enough lines")
        #exit()

    # Creazione della classe per gli oggetti pallet
    class DimensioniPallet:
        def __init__(self, id=None, lungh=None, largh=None, peso=None, altezza=None):
            self.lungh = lungh
            self.largh = largh
            self.id = id
            self.area = 0.0
            self.peso= peso
            self.altezza= altezza
            
    # Pulizia dei dati da caratteri indesiderati e conversione dei valori estratti da str a float convertiti in metri
    def convert_to_meters(value_str):
        try:
            cleaned_value = value_str.split(";")[0]
            cleaned_value = cleaned_value.replace(".", "")
            cleaned_value = cleaned_value.replace(",", ".")
            return float(cleaned_value) / 1000
        except (ValueError, AttributeError):
            print(f"Error converting value: {value_str}")
        return 0.0

    # Pulizia dei dati da caratteri indesiderati e conversione dei valori estratti da str a float
    def convert_to_float(value_str):
        try:
            cleaned_value = value_str.split(";")[0]
            cleaned_value = cleaned_value.replace(".", "")
            cleaned_value = cleaned_value.replace(",", ".")
            return float(cleaned_value)
        except (ValueError, AttributeError):
            print(f"Error converting value: {value_str}")
        return 0.0
    
    file_path = csv_path

    # Lettura del file CSV
    try:
        myCSVfile = pd.read_csv(
            file_path,
            sep=";",
            decimal=",",
            dtype={depth: str, lenght: str, nome: str, weight : str, height : str},
            thousands=".",
            encoding="utf-8"
        )
    except FileNotFoundError:
        print("Error: CSV file not found")
        exit()
    except KeyError:
        print("Error: One or more columns not found in the CSV")
        exit()
    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty")
        exit()

    # Estrazione dei valori degli oggetti dal file csv
    for _, row in myCSVfile.iterrows():
    
        id = row[nome]
        lungh_str = row[depth]
        largh_str = row[lenght]
        peso_str = row[weight]
        altezza_str = row[height]

        lungh = convert_to_meters(lungh_str)
        largh = convert_to_meters(largh_str)
        peso= convert_to_float(peso_str)
        altezza= convert_to_meters(altezza_str)

        pallet = DimensioniPallet(id, lungh, largh,peso,altezza)
        pallet.area = pallet.lungh * pallet.largh
        pallet.id=pallet.id[-8:]
        dati.append(pallet)
        
    #preparazione dei dati per la visualizzazione 3D
    for item in dati:
        item.name=item.id
        item.width=item.largh
        item.height=item.altezza
        item.depth=item.lungh
        item.weight=item.peso
        
        items_3d.append(item)
    
    # Creazione della classe per generare l'oggetto contenitore
    class Bin3d:
        def __init__(self, name =None, width = None, height = None, depth = None, max_weight = None):
            self.name = name
            self.width = width
            self.height = height
            self.depth = depth
            self.max_weight = max_weight
    
    # Creazione del oggetto contenitore
    container = Bin3d("Container", 2.30, 2.36, 12.03, 30480)
    camion_motrice = Bin3d("Camion Motrice", 2.40, 2.36, 8.00, 10000)
    camion_bilico = Bin3d("Camion Bilico", 2.40, 2.36, 13.60,24000)
    
    # Scelta del contenitore e aggiunta alla lista
    if bin_type == "Container":
        container_3d.append(container)
    elif bin_type == "Camion Motrice":
        container_3d.append(camion_motrice)
    elif bin_type == "Camion Bilico":
        container_3d.append(camion_bilico)
    else:
        container_3d.append(container)
        
    # Debug
    """
    for pallet in dati:
        print("id:",pallet.id,"","Lunghezza:",pallet.lungh,"","Larghezza:",pallet.largh,"","Altezza:",pallet.altezza, "","Peso:",pallet.peso)
    
    #"""

    return container_3d, items_3d

#exec(csv_path = "C:\\Users\\stage.convett\\Documents\\T_20250320_143411.csv") #debug