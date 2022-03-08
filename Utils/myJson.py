import rasterio as rio
import json
from typing import List

class myJson():

    def create_coord_json():

        mylist = myJson.create_list_files()

        dsm = mylist[0]
        dtm = mylist[1]

        data = dict()
        data["parameters"] = []

        for x,elem in enumerate(dsm):

            myfileDSM = rio.open(elem)
            myfileDTM = rio.open(dtm[x])

            pathDSM = myfileDSM.name
            pathDTM = myfileDTM.name

            fileDSM = pathDSM.split("/")[8]
            fileDSM = fileDSM.split(".")[0]
            fileDTM = pathDTM.split("/")[8]
            fileDTM = fileDTM.split(".")[0]

            big_left:float = myfileDSM.bounds.left
            big_top:float = myfileDSM.bounds.top
            big_bottom:float= myfileDSM.bounds.bottom
            big_right:float = myfileDSM.bounds.right

            data["parameters"].append({
                "Left" : big_left,
                "Bottom" : big_bottom,
                "Right" : big_right,
                "Top" : big_top,
                "DSM" : fileDSM,
                "DTM" : fileDTM,
                "DSM Path" : pathDSM,
                "DTM Path" : pathDTM
            })

        with open("mycoord.json", "w") as mydata:
            json.dump(data,mydata)
    

    def read_json():
        with open("mycoord.json") as file:
            data = json.load(file)
        
        return data["parameters"]



    def create_list_files():
        """
        Create a variable that contains the liste of files that i have to read
        """

        dsm:List= []
        dtm:List= []
        
        my_files:List= []

        mynumber:str = ""
        extension = ".tif"

        for x in range(1,44):
            if x < 10:
                mynumber = "0"+str(x)
                mypathDSM = f"zip+file:..///Regions-Brux-Fland/DHMVIIDSMRAS1m_k{mynumber}.zip!/GeoTIFF/"
                mypathDTM = f"zip+file:..///Regions-Brux-Fland/DHMVIIDTMRAS1m_k{mynumber}.zip!/GeoTIFF/"
            else:
                mynumber = str(x)
                mypathDSM = f"zip+file:..///Regions-Brux-Fland/DHMVIIDSMRAS1m_k{mynumber}.zip!/GeoTIFF/"
                mypathDTM = f"zip+file:..///Regions-Brux-Fland/DHMVIIDTMRAS1m_k{mynumber}.zip!/GeoTIFF/"

            dsm.append(f"{mypathDSM}DHMVIIDSMRAS1m_k{mynumber}{extension}")
            dtm.append(f"{mypathDTM}DHMVIIDTMRAS1m_k{mynumber}{extension}")
        
        my_files = dsm,dtm

        return my_files
