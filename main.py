import pandas as pd
import xml.etree.ElementTree as et
import plotly.express as px
import tifffile as tifffile
import numpy as np

def pull_marker_data(xml_file):
    file = et.parse(xml_file)
    root = file.getroot()
    marker_data = []

    MDElement = root.find('Marker_Data')
    for Marker_Type in MDElement.findall('Marker_Type'):
        type_id = int(Marker_Type.find('Type').text)

        for Marker in Marker_Type.findall('Marker'):
            xloc = int(Marker.find('MarkerX').text) if Marker.find('MarkerX') is not None else None
            yloc = int(Marker.find('MarkerY').text) if Marker.find('MarkerY') is not None else None
            zloc = int(Marker.find('MarkerZ').text) if Marker.find('MarkerZ') is not None else None

            zlayer = (2 + zloc) / 3


            marker_data.append({
                'z': zlayer,
                'type_id': type_id,
                'y': yloc,
                'x': xloc,
            })

    dataframe = pd.DataFrame(marker_data, columns=['z', 'type_id', 'y', 'x'])
    return dataframe

def visualize_marker_data(dataframe):
    fig = px.scatter_3d(dataframe, z='z',color='type_id', y='y',x='x')
    fig.show()


def create_marked_file_2(xml_file, input_file, output_file):
    original_image = tifffile.imread(input_file)
    layers, channels, height, width = original_image.shape
    dataframe = pull_marker_data(xml_file)
    marked_image = np.copy(original_image)
    id_layers = dataframe['z'].unique()
    for z in id_layers:
        z = int(z)
        if z > 0 and z >= layers:
            continue

        z_layer_markers = dataframe[dataframe['z'] == z]

        for _, marker in z_layer_markers.iterrows():
            y, x = int(marker['y']), int(marker['x'])
            if 0 < y <= height and 0 < x <= width:
                marked_image[z, 1, y, x] = 255
            else:
                marked_image[z, 1, y, x] = 0

    return tifffile.imwrite(output_file, marked_image)

create_marked_file_2('FF15A/CellCounter_FF151L2l.xml', 'FF15/FF151L2L.lsm', 'FF15/FF151L2L_marked.lsm')

def display_image(image_path):
    return tifffile.imshow(tifffile.imread(image_path))


display_image('FF15/FF151L2L_marked.lsm')

