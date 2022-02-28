from typing import List

class Box():

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

