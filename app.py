import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

# HEADER

def show_header(text_title: str):
    col1, col2 = st.columns([1, 6])

    with col1:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/3/32/Universidad_Panamericana_Logo_Dorado.jpg",
            width=120
        )

    with col2:
        st.title(text_title)
        st.caption("Pamela Yadira Vega Agraz")
        st.caption("Patricio Cárdenas Torres")
        st.caption("Universidad Panamericana")


show_header("Dashboard Videojuegos Steam")

# DATA

url = "https://github.com/pamelayva-8/Proyecto-BI-Videojuegos-Steam/blob/865ad3597646dfa80e52ce948f09acd4f4b22b79/steam_limpio.csv"

df = pd.read_csv(url)

# CONTENT

st.markdown("##  Videojuegos steam")

col1, col2 = st.columns(2)

with col1:
    st.metric("Videojuegos totales", len(df))

with col2:
    st.metric("Publisher", round(df['Publisher'].mean(), 2))

st.dataframe(df[['name', 'lat', 'lon', 'capacity']].head(10))
# MAP

centroide_lat = df['lat'].mean()
centroide_lon = df['lon'].mean()

mapa = folium.Map(
    location=[centroide_lat, centroide_lon],
    zoom_start=12
)

for i in range(len(df)):
    folium.Marker(
        location=[df['lat'][i], df['lon'][i]],
        popup=df['name'][i]
    ).add_to(mapa)

st_folium(mapa, width=700, height=500)
