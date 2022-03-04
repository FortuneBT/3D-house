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


class Run():
    
    def __init__(self):
        self.time_application = False
        self.begin = 0
        self.end = 0


    def start(self):

        self.begin = time.perf_counter()

        myaddress:str = input("Wich address do you want to see ? : ")

        sbox:Box = Coord.process_input(myaddress)

        pathDSM,pathDTM = Coord.inside_files(sbox)

        pathTEST = "../Regions-Brux-Fland/test.tif"

        print(pathDSM)

        if pathDSM != 0:
            
            dsm = rio.open(pathDSM)

            """Canopy Height Model"""
            #dsm = self.chmed(dsm,pathDTM,pathTEST) 

            mywin = Front.cropped_window(sbox,dsm)

            """the 2D map version"""
            #Front.show_2D(source,mywin) # 

            Front.show_3D(dsm,mywin)
            dsm.close()
            print("DONE !!!!!!!!!")
            self.end = time.perf_counter()
        else:
            print("the address is not in those maps!")
            self.end = time.perf_counter()

        if self.time_application == True:
            whole_time = round(self.end - self.begin,2)
            print(f"the time of the execution of this application is : {whole_time} second(s)")



    def chmed(self, dsm, pathDTM, pathFILE):

        dtm = rio.open(pathDTM)

        chm = dsm.read() - dtm.read()

        kwargs = dtm.meta

        file = rio.open(pathFILE, 'w', **kwargs) 
        
        file.write(chm)

        dsm.close()

        dsm = rio.open(pathFILE)

        return dsm



    def mytime(self):

        self.time_application = True
        