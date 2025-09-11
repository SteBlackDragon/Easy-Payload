import plotly.graph_objects as go
import numpy as np

def exec(container_3d, items_3d):
    # Lista colori item
    color_list=["red", "blue", "green", "yellow", "orange", "purple",
        "pink", "brown", "gray", "cyan", "magenta", "lime", "black"]
    
    num_colors = len(color_list)

    # Calcolo e definizione dei vertici  del contenitore
    def vertici_cont():
        cont_x = np.array([0, cont_lunghezza, cont_lunghezza, 0, 0, cont_lunghezza, cont_lunghezza, 0])
        cont_y = np.array([0, 0, cont_larghezza, cont_larghezza, 0, 0, cont_larghezza, cont_larghezza])
        cont_z = np.array([0, 0, 0, 0, cont_altezza, cont_altezza, cont_altezza, cont_altezza])
        return cont_x, cont_y, cont_z

    # calcolo delle faccie del contenitore tramite triangoli (2xfaccia)
    def facce_cont():
        cont_i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 5]
        cont_j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 7, 3]
        cont_k = [0, 7, 2, 3, 6, 7, 1, 0, 5, 5, 2, 6]
        return cont_i, cont_j, cont_k

    # Creazione delle figure del contenitore
    def creazione_figure_contenitore(cont_x, cont_y, cont_z, cont_i, cont_j, cont_k):
        cont=go.Figure(data=[go.Mesh3d(x=cont_x,y=cont_y,z=cont_z,
                                i=cont_i, j=cont_j, k=cont_k,
                                color="lightskyblue",
                                opacity=0.8,
                                name="Contenitore")])
        return cont

    # Inserimento ed adattamento del contenitore nel layout
    def inserimento_layout_contenitore(cont):
        cont.update_layout(scene=dict(
            xaxis_title="Lunghezza",
            yaxis_title="Larghezza",
            zaxis_title="Altezza",
            aspectratio=dict(x=cont_lunghezza, y=cont_larghezza, z=cont_altezza),
            ),
            title="Carico del Camion/Container",
    )
        return cont

    # Aggiunta degli item al container 3D
    def aggiungi_item_al_container(cont, items_3d):
        # Variabili per tracciare la posizione corrente
        current_x = 0
        current_y = 0
        max_row_height = 0  # Altezza massima della riga corrente

        color_index=0

        global unfitted_items
        unfitted_items = []

        # Liste per posizioni ed etichette
        text_x_coords = []
        text_y_coords = []
        text_z_coords = []
        text_labels = []

        # Offset per applicare il testo sopra
        text_z_offset = 0.05

        for item in items_3d:
            # Impostazione colore
            item_color=color_list[color_index % num_colors]
            color_index+=1
            # Verifica che l'item non esca dai limiti del container
            if (current_x + item.width > cont_lunghezza):
                # Passa alla riga successiva
                current_x = 0
                current_y += max_row_height
                max_row_height = 0

            if (current_y + item.depth > cont_larghezza):
                #print(f"Errore: L'item {item.name} supera i limiti del container!")
                unfitted_items.append(item)
                continue

            # Posiziona l'item
            item.position = [current_x, current_y, 0]  # Z è sempre 0 per occupare la superficie

            # Calcolo delle coordinate dei vertici dell'item
            item_x = np.array([
                item.position[0], item.position[0] + item.width, item.position[0] + item.width, item.position[0],
                item.position[0], item.position[0] + item.width, item.position[0] + item.width, item.position[0]
            ])
            item_y = np.array([
                item.position[1], item.position[1], item.position[1] + item.depth, item.position[1] + item.depth,
                item.position[1], item.position[1], item.position[1] + item.depth, item.position[1] + item.depth
            ])
            item_z = np.array([
                item.position[2], item.position[2], item.position[2], item.position[2],
                item.position[2] + item.height, item.position[2] + item.height, item.position[2] + item.height, item.position[2] + item.height
            ])

            # Calcolo delle facce dell'item
            item_i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 5]
            item_j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 7, 3]
            item_k = [0, 7, 2, 3, 6, 7, 1, 0, 5, 5, 2, 6]

            # Aggiunta dell'item alla figura del container
            cont.add_trace(go.Mesh3d(
                x=item_x, y=item_y, z=item_z,
                i=item_i, j=item_j, k=item_k,
                color=item_color,
                opacity=0.99,
                name=f"Item {item.name}"
            ))

            label_x = item.position[0] + item.width / 2
            label_y = item.position[1] + item.depth / 2
            label_z = item.position[2] + item.height + text_z_offset # Posiziona sopra l'item

            # Aggiungi le coordinate e l'etichetta alle liste
            text_x_coords.append(label_x)
            text_y_coords.append(label_y)
            text_z_coords.append(label_z)
            text_labels.append(f"<b>{item.name}</b>")

            # Aggiorna la posizione corrente e l'altezza massima della riga
            current_x += item.width
            max_row_height = max(max_row_height, item.depth)

        # Aggiungi il trace Scatter3d per le etichette dopo aver processato tutti gli item
        cont.add_trace(go.Scatter3d(
            x=text_x_coords,
            y=text_y_coords,
            z=text_z_coords,
            mode='text', # Mostra solo il testo
            text=text_labels,
            textfont=dict(
                size=10, # Dimensione del font
                color='black' # Colore del testo
            ),
            textposition='middle center', # Posizione del testo rispetto al punto (x,y,z)
        ))

        # Aggiorna la posizione corrente e l'altezza massima della riga
        current_x += item.width
        max_row_height = max(max_row_height, item.depth)

        return cont

    # Estrae le dimensioni del container
    for bin in container_3d:
        cont_lunghezza = bin.width  # larghezza del container
        cont_larghezza = bin.depth  # profondità del container
        cont_altezza = bin.height   # altezza del container

    # Inizializzazione funzioni
    cont_x, cont_y, cont_z = vertici_cont()
    cont_i, cont_j, cont_k = facce_cont()
    cont = creazione_figure_contenitore(cont_x, cont_y, cont_z, cont_i, cont_j, cont_k)
    cont = inserimento_layout_contenitore(cont)

    # Aggiunta degli item al container
    cont = aggiungi_item_al_container(cont, items_3d)

    def visualizza_contenitore(cont):
        cont.show()
    # Visualizzazione del contenitore con gli item
    visualizza_contenitore(cont)

    return container_3d, items_3d