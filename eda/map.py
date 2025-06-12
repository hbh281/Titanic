import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px


def showEmbarkedMap(df):
    embarked_coords = {
        "C" : {"lat" : 49.633, "lon" : -1.616},
        "Q" : {"lat" : 51.849, "lon" : -8.294},
        "S" : {"lat": 50.904, "lon": -1.404}
    }
    df["lat"] =df["Embarked"].map(lambda x: embarked_coords[x]["lat"] if x in embarked_coords else None)
    df["lon"] =df["Embarked"].map(lambda x: embarked_coords[x]["lon"] if x in embarked_coords else None)

    fig_map = px.scatter_mapbox(
        df,
        lat = "lat",
        lon = "lon",
        hover_name = "Name",
        hover_data= ["Sex","Age","Fare","Survived"],
        color = "Embarked",
        zoom =3,
        height= 600
    )
    fig_map.update_layout(
        mapbox_style = "carto-positron",
        title = "🚢 승객 출발 위치 (Embarked Location Map)",
        margin = {"r":0,"t":30,"l":0,"b":0}
        
    )
    st.plotly_chart(fig_map,use_container_width= True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    embarked_counts = df.groupby(['Embarked','lat','lon']).size().reset_index(name = 'PassengerCount')
    fig_count = px.scatter_mapbox(
        embarked_counts,
        lat = "lat",
        lon = "lon",
        size = "PassengerCount",
        hover_name= "Embarked",
        hover_data=["PassengerCount"],
        zoom = 3,
        
    )
    fig_count.update_layout(
        mapbox_style = "carto-positron",
        title = "항구별 승객수",
        margin = {"r":0,"t":30,"l":0,"b":0}
    )
    st.plotly_chart(fig_count,use_container_width=True)