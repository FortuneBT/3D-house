import streamlit as st
from Utils.mydata import Data
from Utils.run import Run


header = st.container()
dataset = st.container()
features = st.container()
figure = st.container()
mydata = Data()
app = Run()

with header:
    st.title("Project of Data Science : 3D home")
    st.markdown("In this project, I will collect data coming from Lidar technologie and use it to show a 3D house",)

with dataset:
    st.subheader("Dataset are the DSM and the DTM to create a CHM")
    st.markdown("The dataset i'm using is coming from **[DSM](http://www.geopunt.be/download?container=dhm-vlaanderen-ii-dsm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DSM,%20raster,%201m)** and [DTM](http://www.geopunt.be/download?container=dhm-vlaanderen-ii-dsm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DSM,%20raster,%201m) and contain only data from the flanders and Bruxelles region")
    st.markdown("I'm also using my previous work with the data scrapped from the website : ImmoWeb")
    st.write(mydata.price_mean_by_region())

with figure:

    st.header("My address")

    size = st.slider("What's the size of the window you want to crop ?", value=100,min_value=50,max_value=300,step=10)

    input = None

    input = st.text_input("What is your address ? ","la basilique de koekelberg")
    

    test = app.beginning(input,size)

 
    fig2 = app.show2d()
    fig3 = app.show3d()
    leftpart,righpart = st.columns([1,2])

    

    st.markdown(f"**{app.address}**")

    if input != "":
        st.plotly_chart(fig3, use_container_width=True)

    




