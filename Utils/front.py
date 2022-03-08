import rasterio as rio
from rasterio.plot import show
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import numpy as np

class Front():

    def cropped_window(small_box,source):
        """
        This function will cropped a smaller windows. It will take a small part of the map
        of the tiff file and define the size we want to plot.
        small_box = the box representing the bounds around the location
        source = the object assign after opening the tiff file
        """

        small_left = small_box[0]
        small_bottom = small_box[1]
        small_right = small_box[2]
        small_top = small_box[3]

        mywin = source.window(left=small_left,bottom=small_bottom,right=small_right,top=small_top)

        return mywin


    def show_2D(chm_read):
        
        plt.imshow(chm_read)
        plt.show()


    def show_3D(myz)-> None:

        """myz = map.read(1,window=mywin)"""

        # Retrieves the NxM array from the BxNxM xarray object
        arr = myz.squeeze().data

        X = np.arange(0, myz.shape[0]*1, 1)
        Y = np.arange(0, myz.shape[1]*-1, -1)
        X, Y = np.meshgrid(X,Y)
    
        # Pads the array for better rendering
        arr = np.pad(arr, [(5, ), (5, )], mode='constant')
        
        arr = arr.T
        
        # Take the length to have proper ratio in the rendering
        N = len(arr[:,0])
        M = len(arr[0,:])
        
        fig = go.Figure(data=[go.Surface(x=X,y=Y,z=myz)]) 

        fig.update_layout(scene = {"aspectratio": {"x": (N/N), "y":(N/M), "z": np.max(arr)/M}})

        fig.show()