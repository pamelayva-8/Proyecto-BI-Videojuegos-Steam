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
        st.caption("📘 Developed for: Business Intelligence")
        st.caption("Universidad Panamericana")


show_header("Dashboard Ecobici CDMX")

# DATA

url = "https://gbfs.mex.lyftbikes.com/gbfs/gbfs.json"

pagina = requests.get(url).json()
ligas = pagina['data']['es']['feeds']

liga = [liga for liga in ligas if liga['name'] == 'station_information'][0]

df = pd.DataFrame(
    requests.get(liga['url']).json()['data']['stations']
)

# CONTENT

st.markdown("## 🚲 Ecobici Stations in Mexico City")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Stations", len(df))

with col2:
    st.metric("Average Capacity", round(df['capacity'].mean(), 2))

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
