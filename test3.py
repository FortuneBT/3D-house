import streamlit as st


header = st.container()
dataset = st.container()
features = st.container()
figure = st.container()

with header:
    st.title("Project of Data Science : 3D home")
    st.text("In this project, I will collect data coming from Lidar technologie and use it to show a 3D house")

with dataset:
    st.header("Dataset are the DSM and the DTM to create a CHM")
    st.text("The dataset i'm using is coming from ** this website ** and containe only data from the flanderen and Bruxelles region")


with features:
    st.header("2D and 3D model of a given place")


with figure:
    st.header("My address")



