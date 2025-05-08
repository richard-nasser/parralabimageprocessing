import pandas as pd
import xml.etree.ElementTree as et
import plotly.express as px
import tifffile as tifffile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


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



def create_marked_file_final(xml_file, input_file, output_file):
    import numpy as np
    import tifffile
    import xml.etree.ElementTree as ET

    original_image = tifffile.imread(input_file)
    layers, channels, height, width = original_image.shape
    print(original_image.shape)
    binary_image = np.zeros((layers, 1, height, width), dtype=np.uint8)
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for marker_type in root.findall('Marker_Data/Marker_Type'):
        type_id = int(marker_type.find('Type').text)

        for marker in marker_type.findall('Marker'):

            x = int(marker.find('MarkerX').text) -1
            y = int(marker.find('MarkerY').text) -1
            z_raw = ((int(marker.find('MarkerZ').text) + 2 ) // 3) -1

            if 0 < z_raw <= layers and 0 < y <= height and 0 < x <= width:
                binary_image[z_raw, 0, y, x] = 255

            else:
                print(f"Skipped out-of-bounds marker: raw z={z_raw}, scaled z={z_raw}, y={y}, x={x}")

    if output_file:
        tifffile.imwrite(output_file, binary_image)
        print(f"Saved marked image to {output_file}")

    return binary_image


create_marked_file_final('FF15A/CellCounter_FF151L2L.xml', 'FF15/FF151L2L.lsm', 'FF15/FF151L2L_marked7.tif')

