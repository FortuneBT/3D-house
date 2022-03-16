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
    
    def __init__(self) -> None:

        self.time_application:bool = False
        self.begin:float = 0
        self.end:float = 0
        self.latitude:float = 0
        self.longitude:float = 0
        self.pathDSM:str = None
        self.pathDTM:str = None
        self.dsm:rio = None
        self.dtm:rio = None
        self.address:str = ""
        self.sbox:Box = None
        self.bbox:Box = None
        self.mywin = None
        self.chm = None
        self.fig2 = None
        self.fig3 = None


    def start(self):

        self.begin = time.perf_counter()

        result = self.input()

        if result != 0:
            
            self.chm = self.create_chm()

            front = Front()

            front.show_2D(self.chm) 

            front.show_3D(self.chm)

            self.fig2 = front.fig_2D
            self.fig3 = front.fig_3D

            self.dsm.close()
            self.dtm.close()

            self.end = time.perf_counter()
        else:
            print("the address is not in those maps!")
            self.end = time.perf_counter()


        if self.time_application == True:
            whole_time = round(self.end - self.begin,2)
            print(f"the time of the execution of this application is : {whole_time} second(s)")



    def format_chm(self, mywin):

        self.dtm = rio.open(self.pathDTM)

        chm_read = self.dsm.read(1,window=mywin) - self.dtm.read(1,window=mywin)
        
        return chm_read



    def mytime(self):

        self.time_application = True



    def get_coordinate(self, coordinate):

            self.address = coordinate.address

            self.latitude = coordinate.lat

            self.longitude = coordinate.lon



    def input(self,address,size):

        coord = Coord()

        self.sbox:Box = coord.process_input(address,size)

        self.get_coordinate(coord)

        self.pathDSM,self.pathDTM = Coord.inside_files(self.sbox)

        return self.pathDSM


    
    def create_chm(self):

        self.dsm = rio.open(self.pathDSM)

        self.mywin = Front.cropped_window(self.sbox,self.dsm)

        """Canopy Height Model (CHM)"""
        chm_read = self.format_chm(self.mywin) 

        return chm_read
        
    def beginning(self,address,size):

        result = self.input(address,size)

        if result != 0:
            
            self.chm = self.create_chm()

            self.dsm.close()
            self.dtm.close()

        return self.chm


    def show2d(self):
        front = Front()
        fig = front.show_2D(self.chm)
        return fig

    def show3d(self):
        front = Front()
        fig = front.show_3D(self.chm)
        return fig

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