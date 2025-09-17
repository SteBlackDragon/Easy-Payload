import plotly.graph_objects as go
import numpy as np

def exec(container_3d, items_3d):
    # Item color list
    color_list=["red", "blue", "green", "yellow", "orange", "purple",
        "pink", "brown", "gray", "cyan", "magenta", "lime", "black"]
    
    num_colors = len(color_list)

    # Calculation and definition of the container vertices
    def vertici_cont():
        cont_x = np.array([0, cont_lunghezza, cont_lunghezza, 0, 0, cont_lunghezza, cont_lunghezza, 0])
        cont_y = np.array([0, 0, cont_larghezza, cont_larghezza, 0, 0, cont_larghezza, cont_larghezza])
        cont_z = np.array([0, 0, 0, 0, cont_altezza, cont_altezza, cont_altezza, cont_altezza])
        return cont_x, cont_y, cont_z

    # Calculation of container faces using triangles (2xside)
    def facce_cont():
        cont_i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 5]
        cont_j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 7, 3]
        cont_k = [0, 7, 2, 3, 6, 7, 1, 0, 5, 5, 2, 6]
        return cont_i, cont_j, cont_k

    # Creating container figures
    def creazione_figure_contenitore(cont_x, cont_y, cont_z, cont_i, cont_j, cont_k):
        cont=go.Figure(data=[go.Mesh3d(x=cont_x,y=cont_y,z=cont_z,
                                i=cont_i, j=cont_j, k=cont_k,
                                color="lightskyblue",
                                opacity=0.8,
                                name="Bin/Container")])
        return cont

    # Insertion and adaptation of the container into the layout
    def inserimento_layout_contenitore(cont):
        cont.update_layout(scene=dict(
            xaxis_title="Length",
            yaxis_title="Width",
            zaxis_title="Height",
            aspectratio=dict(x=cont_lunghezza, y=cont_larghezza, z=cont_altezza),
            ),
            title="Truck/container load",
    )
        return cont

    # Adding items to the 3D container
    def aggiungi_item_al_container(cont, items_3d):
        # Variables used to map the current location
        current_x = 0
        current_y = 0
        max_row_height = 0  # Maximum height of the current row

        color_index=0

        global unfitted_items
        unfitted_items = []

        # Lists for locations and labels
        text_x_coords = []
        text_y_coords = []
        text_z_coords = []
        text_labels = []

        # Offset to apply the text above
        text_z_offset = 0.05

        for item in items_3d:
            # Color settings
            item_color=color_list[color_index % num_colors]
            color_index+=1
            # Verify that the item does not go outside the limits of the container
            if (current_x + item.width > cont_lunghezza):
                # Passa alla riga successiva
                current_x = 0
                current_y += max_row_height
                max_row_height = 0

            if (current_y + item.depth > cont_larghezza):
                #print(f"Error: the item {item.name} exceed the limits of the container!")
                unfitted_items.append(item)
                continue

            # Place item
            item.position = [current_x, current_y, 0]  # Z is always 0 to occupy the surface

            # Calculation of the coordinates of the item vertices
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

            # Calculation of item faces
            item_i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 5]
            item_j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 7, 3]
            item_k = [0, 7, 2, 3, 6, 7, 1, 0, 5, 5, 2, 6]

            # Adding the item to the container figure
            cont.add_trace(go.Mesh3d(
                x=item_x, y=item_y, z=item_z,
                i=item_i, j=item_j, k=item_k,
                color=item_color,
                opacity=0.99,
                name=f"Item {item.name}"
            ))

            label_x = item.position[0] + item.width / 2
            label_y = item.position[1] + item.depth / 2
            label_z = item.position[2] + item.height + text_z_offset # Place above the item

            # Add coordinates and label to lists
            text_x_coords.append(label_x)
            text_y_coords.append(label_y)
            text_z_coords.append(label_z)
            text_labels.append(f"<b>{item.name}</b>")

            # Update the current position and maximum row height
            current_x += item.width
            max_row_height = max(max_row_height, item.depth)

        # Add the Scatter3d trace for labels after processing all items
        cont.add_trace(go.Scatter3d(
            x=text_x_coords,
            y=text_y_coords,
            z=text_z_coords,
            mode='text', # Show text only
            text=text_labels,
            textfont=dict(
                size=10, # Font size
                color='black' # Text color
            ),
            textposition='middle center', # Position of the text with respect to the point (x,y,z)
        ))

        # Update the current position and maximum row height
        current_x += item.width
        max_row_height = max(max_row_height, item.depth)

        return cont

    # Extracts container size
    for bin in container_3d:
        cont_lunghezza = bin.width  # container width
        cont_larghezza = bin.depth  # container depth
        cont_altezza = bin.height   # container height

    # Function initialization
    cont_x, cont_y, cont_z = vertici_cont()
    cont_i, cont_j, cont_k = facce_cont()
    cont = creazione_figure_contenitore(cont_x, cont_y, cont_z, cont_i, cont_j, cont_k)
    cont = inserimento_layout_contenitore(cont)

    # Adding items to the container
    cont = aggiungi_item_al_container(cont, items_3d)

    def visualizza_contenitore(cont):
        cont.show()
    # Displaying the container with items
    visualizza_contenitore(cont)


    return container_3d, items_3d
    
