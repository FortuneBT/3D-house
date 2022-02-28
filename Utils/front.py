import rasterio as rio
from rasterio.plot import show
from matplotlib import pyplot as plt
import plotly.graph_objects as go

class Front():

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