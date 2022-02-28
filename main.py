import rasterio as rio
from typing import List
from rasterio.plot import show
from matplotlib import pyplot as plt
import pandas as pd
import geopandas as gpd
import pyproj
from geopy.geocoders import Nominatim
import numpy as np
import json
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode,plot,iplot
import cufflinks as cf


#cf.go_offline()


def conv_coord_system_location(latitude:float,longitude:float,address_system:int,belgian_system:int)->List[float]:

    coord_address:List = []

    belgian_coord:pyproj = pyproj.Transformer.from_crs(address_system, belgian_system)

    #lat_address,lon_address = belgian_coord.transform(location.latitude,location.longitude)

    lat_address,lon_address = belgian_coord.transform(latitude,longitude)

    coord_address.append(lat_address)
    coord_address.append(lon_address)

    return coord_address



def create_coord(my_address:str)-> List[float]:

    address = my_address

    geolocator = Nominatim(user_agent="myhome")

    location = geolocator.geocode(address)

    address_system:int = 4326
    
    #belgian_system:int = int(str(map.meta["crs"]).split(":")[1])

    belgian_system:int = 31370

    #location.address

    #print(location.raw)

    #local_boundingbox = location.raw["boundingbox"]

    coord = conv_coord_system_location(location.latitude,location.longitude,address_system,belgian_system)

    return coord



def create_b_box(source)->List[float]:

    box:List = []

    big_left:float = source.bounds.left
    big_top:float = source.bounds.top
    big_bottom:float= source.bounds.bottom
    big_right:float = source.bounds.right

    box.append(big_left)
    box.append(big_bottom)
    box.append(big_right)
    box.append(big_top)

    #source.bounds

    return box



def create_s_box(myLatitude:float,myLongitude:float,lat_size:int,lon_size:int)->List[float]:

    box:List = []

    lat_address = myLatitude
    lon_address = myLongitude

    small_left:float = lat_address - lat_size
    small_bottom:float = lon_address - lon_size
    small_right:float = lat_address + lat_size
    small_top:float = lon_address + lon_size
    
    box.append(small_left)
    box.append(small_bottom)
    box.append(small_right)
    box.append(small_top)

    return box


def test_box(big_box,small_box):

    result:bool = False

    small_left:float = small_box[0]
    small_bottom:float = small_box[1]
    small_right:float = small_box[2]
    small_top:float = small_box[3]

    big_left:float = big_box[0]
    big_bottom:float = big_box[1]
    big_right:float = big_box[2]
    big_top:float = big_box[3]
    
    if small_left > big_left:
        if small_bottom > big_bottom:
            if small_right < big_right:
                if small_top < big_top:
                    result = True
    
    return result


def cropped_window(small_box,source):

    small_left = small_box[0]
    small_bottom = small_box[1]
    small_right = small_box[2]
    small_top = small_box[3]

    mywin = source.window(left=small_left,bottom=small_bottom,right=small_right,top=small_top)

    return mywin


def show_2D(map,my_window):

    source = map

    mywin = my_window
    
    plt.imshow(source.read(1,window=mywin))
    plt.show()


def show_3D(map,my_window)-> None:

    source = map

    mywin = my_window

    myz = source.read(1,window=mywin)

    fig = go.Figure(data=[go.Surface(z=myz)]) 
    fig.show()


def process_input(my_address)-> List:

    lat,lon = create_coord(my_address)

    sbox = create_s_box(lat,lon,30,30)

    return sbox


def create_list_files():
    """
    Create a variable that contains the liste of files that i have to read
    """

    my_files:List= []
    mynumber:str = ""
    extension = ".tif"

    for x in range(1,44):
        if x < 10:
            mynumber = "0"+str(x)
            mypath = f"zip+file:.///geo/DHMVIIDSMRAS1m_k{mynumber}.zip!/GeoTIFF/"
        else:
            mynumber = str(x)
            mypath = f"zip+file:.///geo/DHMVIIDSMRAS1m_k{mynumber}.zip!/GeoTIFF/"

        my_files.append(f"{mypath}DHMVIIDSMRAS1m_k{mynumber}{extension}")

    return my_files



def create_coord_json():

    mylist = create_list_files()

    data = dict()
    data["parameters"] = []

    for elem in mylist:

        myfile = rio.open(elem)

        path = myfile.name

        file = path.split("/")[8]
        file = file.split(".")[0]

        big_left:float = myfile.bounds.left
        big_top:float = myfile.bounds.top
        big_bottom:float= myfile.bounds.bottom
        big_right:float = myfile.bounds.right

        data["parameters"].append({
            "Left" : big_left,
            "Bottom" : big_bottom,
            "Right" : big_right,
            "Top" : big_top,
            "Name" : file,
            "Path" : path
        })

    with open("mycoord.json", "w") as mydata:
        json.dump(data,mydata)
    

def read_json():
    with open("mycoord.json") as file:
        data = json.load(file)
    
    return data["parameters"]



def inside_files(small_box):

    data = read_json()

    result = 0

    for e in data:
        
        big_box = []

        if result == 0:
            bleft = e["Left"]
            bbottom = e["Bottom"]
            bright = e["Right"]
            btop = e["Top"]

            big_box.append(bleft)
            big_box.append(bbottom)
            big_box.append(bright)
            big_box.append(btop)
            
            result = test_box(big_box,small_box)

            if result == 0:
                path = 0
            else:
                path = e["Path"]
                print("The file is : ",e["Name"])
                break


    print("SMALL BOX",small_box)
    print("BIG BOX",big_box)

    return path



myaddress = input("Wich address do you want to see ? : ")

sbox = process_input(myaddress)

path = inside_files(sbox)

if path != 0:
    source = rio.open(path)
    mywin = cropped_window(sbox,source)
    #show(source)
    #show_2D(source,mywin)
    show_3D(source,mywin)
    print("DONE !!!!!!!!!")
else:
    print("the address is not in those maps!")
open