import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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

url = "https://github.com/pamelayva-8/Proyecto-BI-Videojuegos-Steam/raw/refs/heads/main/steam_limpio.csv"

df = pd.read_csv(url)
st.write(df.head())

# CONTENT

st.markdown("##  Videojuegos steam")

#Métricas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Videojuegos",
        len(df)
    )

with col2:
    st.metric(
        "Rating promedio",
        round(df['rating'].mean(), 2)
    )

with col3:
    st.metric(
        "Precio promedio",
        round(df['price'].mean(), 2)
    )

#Pregunta
st.markdown("""
### Pregunta de investigación

¿Qué características influyen en que un videojuego tenga una calificación positiva?
""")

#Estadísticas descriptivas
t.markdown("### Estadísticas descriptivas")

st.dataframe(
    df[
        [
            'rating',
            'price',
            'peak_ccu',
            'owners_numeric'
        ]
    ].describe()
)

#Gráfica 1
st.markdown("### Distribución del Rating")

fig, ax = plt.subplots(figsize=(8,5))

sns.histplot(
    df['rating'],
    bins=30,
    kde=True,
    ax=ax
)

ax.set_title("Distribución del Rating")

st.pyplot(fig)
