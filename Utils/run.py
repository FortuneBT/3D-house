import multiprocessing
import rasterio as rio
from typing import List
import pandas as pd
import geopandas as gpd
import numpy as np
from Utils.coord import Coord 
from Utils.myJson import myJson
from Utils.front import Front
from Utils.box import Box
import multiprocessing
import threading
from rasterio.crs import CRS
from rasterio.transform import from_origin
from rasterio.windows import Window
import time
import rioxarray as rxr
from typing import Tuple

class Run():
    
    def __init__(self):
        self.time_application = False
        self.begin = 0
        self.end = 0
        self.coord = []


    def start(self):

        self.begin = time.perf_counter()

        coord = Coord()

        sbox:Box = coord.process_input()

        self.coord.append(coord.lat)
        self.coord.append(coord.lon)


        """pathDTM is needed to create CHM"""
        pathDSM,pathDTM = Coord.inside_files(sbox)

        print(pathDSM)

        if pathDSM != 0:
            
            dsm = rio.open(pathDSM)

            mywin = Front.cropped_window(sbox,dsm)

            """Canopy Height Model (CHM)"""
            chm_read = self.chmed(dsm,pathDTM,mywin) 
            """crop_tif()"""

            """the 2D map version"""
            Front.show_2D(chm_read) # 

            Front.show_3D(chm_read)

            dsm.close()

            self.end = time.perf_counter()
        else:
            print("the address is not in those maps!")
            self.end = time.perf_counter()

        if self.time_application == True:
            whole_time = round(self.end - self.begin,2)
            print(f"the time of the execution of this application is : {whole_time} second(s)")



    def chmed(self, dsm, pathDTM, mywin):

        pathFILE = "../Regions-Brux-Fland/test.tif"

        dtm = rio.open(pathDTM)

        chm_read = dsm.read(1,window=mywin) - dtm.read(1,window=mywin)
        
        return chm_read



    def mytime(self):

        self.time_application = True
        

def crop_tif(data, tif_index, poly, shape_cut=True) -> Tuple[np.ndarray]:

    DSM = rxr.open_rasterio(data['DSM_list'][tif_index],masked=True)
    DTM = rxr.open_rasterio(data['DTM_list'][tif_index],masked=True)
    
    # First clipping with bounds optimizes the processing
    left, bottom, right, top = poly.bounds
    DSM_clip = DSM.rio.clip_box(left, bottom, right, top)
    DTM_clip = DTM.rio.clip_box(left, bottom, right, top)

    if shape_cut:
        DSM_clip = DSM_clip.rio.clip([poly.__geo_interface__])
        DSM_clip = np.nan_to_num(DSM_clip, nan=0)

        DTM_clip = DTM_clip.rio.clip([poly.__geo_interface__])
        DTM_clip = np.nan_to_num(DTM_clip, nan=0)
    
    # Close the .tif files to avoid memory leaks
    DSM.close()
    DTM.close()

    result = DSM_clip - DTM_clip
    
    return result