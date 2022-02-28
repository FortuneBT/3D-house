import rasterio as rio
from typing import List
import pandas as pd
import geopandas as gpd
import numpy as np
from Utils.coord import Coord
from Utils.myJson import myJson
from Utils.front import Front
from Utils.box import Box



myaddress:str = input("Wich address do you want to see ? : ")

sbox:Box = Coord.process_input(myaddress)

path:Coord = Coord.inside_files(sbox)

if path != 0:
    source:rio = rio.open(path)
    mywin = Front.cropped_window(sbox,source)
    #Front.show_2D(source,mywin)
    Front.show_3D(source,mywin)
    print("DONE !!!!!!!!!")
else:
    print("the address is not in those maps!")
open