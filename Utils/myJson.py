import rasterio as rio
import json
from typing import List

class myJson():

    def create_coord_json():

        mylist = myJson.create_list_files()

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
                #mypath = f"zip+file:.///geo/DHMVIIDSMRAS1m_k{mynumber}.zip!/GeoTIFF/"
                mypath = f"zip+file:..///Regions-Brux-Fland/DHMVIIDSMRAS1m_k{mynumber}.zip!/GeoTIFF/"

            else:
                mynumber = str(x)
                #mypath = f"zip+file:.///geo/DHMVIIDSMRAS1m_k{mynumber}.zip!/GeoTIFF/"
                mypath = f"zip+file:..///Regions-Brux-Fland/DHMVIIDSMRAS1m_k{mynumber}.zip!/GeoTIFF/"
            my_files.append(f"{mypath}DHMVIIDSMRAS1m_k{mynumber}{extension}")

        return my_files
