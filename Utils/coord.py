from typing import List
import pyproj
from geopy.geocoders import Nominatim
from Utils.box import Box
from Utils.myJson import myJson

class Coord():

    def __init__(self):
        
        self.lat = 0
        self.lon = 0
        self.address = None

    def conv_coord_system_location(latitude:float,longitude:float,address_system:int,belgian_system:int)->List[float]:

        coord_address:List = []

        belgian_coord:pyproj = pyproj.Transformer.from_crs(address_system, belgian_system)

        lat_address,lon_address = belgian_coord.transform(latitude,longitude)

        coord_address.append(lat_address)
        coord_address.append(lon_address)

        return coord_address



    def create_coord(self,address)-> List[float]:

        location = None

        while location == None:

            """if address == None:
                address:str = input("Wich address do you want to see ? : ")"""

            geolocator = Nominatim(user_agent="myhome")

            location = geolocator.geocode(address)

            if location == None:
                print("This address is not found !!!")
        
        self.address = location

        address_system:int = 4326

        belgian_system:int = 31370

        coord = Coord.conv_coord_system_location(location.latitude,location.longitude,address_system,belgian_system)
        
        return coord


    def process_input(self,address,size)-> List:

        lat,lon = self.create_coord(address)

        sbox = Box.create_s_box(lat,lon,size,size)

        self.lat = lat
        self.lon = lon

        return sbox


    def inside_files(small_box):

        data = myJson.read_json()

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
                
                result = Box.test_box(big_box,small_box)

                if result == 0:
                    path = 0
                else:
                    path = e["DSM Path"],e["DTM Path"]
                    print("The file is : ",e["DSM"])
                    break


        print("SMALL BOX",small_box)
        print("BIG BOX",big_box)

        return path