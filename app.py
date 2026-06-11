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

st.divider()

# DATA

url = "https://github.com/pamelayva-8/Proyecto-BI-Videojuegos-Steam/raw/refs/heads/main/steam_limpio.csv"

df = pd.read_csv(url)

#Sidebar
st.sidebar.header("Filtros")

rating_min = st.sidebar.slider(
    "Rating mínimo",
    0,
    100,
    0
)

df_filtrado = df[
    df['rating'] >= rating_min
]

st.divided()

#Sidebar índice
st.sidebar.markdown("## Navegación")

pagina = st.sidebar.radio(
    "Ir a:",
    [
        "Inicio",
        "Estadísticas",
        "Visualizaciones",
        "Machine Learning",
        "Conclusiones"
    ]
)

# CONTENT

st.markdown("##  Videojuegos steam")

st.divider()

#Métricas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Videojuegos",
        len(df_filtrado)
    )

with col2:
    st.metric(
        "Rating promedio",
        round(df_filtrado['rating'].mean(), 2)
    )

with col3:
    st.metric(
        "Precio promedio",
        round(df_filtrado['price'].mean(), 2)
    )
st.divider()

#Pregunta
st.markdown("""
### Pregunta de investigación

¿Qué características influyen en que un videojuego tenga una calificación positiva?
""")

st.markdown("""
Este proyecto analiza más de 56 mil videojuegos de Steam para identificar
qué características pueden influir en que un videojuego reciba una
calificación positiva por parte de los usuarios.
""")

st.divider()
#Estadísticas descriptivas
st.markdown("### Estadísticas descriptivas")

st.dataframe(
    df[
        [
            'rating',
            'price',
            'peak_ccu',
            'owners_numeric'
        ]
    ].describe().round(2)
)
st.divider()

#Videojuegos

st.markdown("### Top 10 videojuegos mejor calificados")

top10 = df.sort_values(
    by='rating',
    ascending=False
)[['name','rating','price']].head(10)

st.dataframe(top10)

st.divider()

juego = st.text_input(
    "Buscar videojuego"
)

if juego:
    resultado = df[
        df['name'].str.contains(
            juego,
            case=False,
            na=False
        )
    ]

    st.dataframe(resultado.head(20))

st.divider()
#Gráfica 1
st.markdown("### Distribución del Rating")

fig, ax = plt.subplots(figsize=(8,5))

sns.histplot(
    df_filtrado['rating'],
    bins=30,
    kde=True,
    ax=ax
)

ax.set_title("Distribución del Rating")

st.pyplot(fig)

st.info("""
Esta gráfica muestra cómo se distribuyen las calificaciones de los videojuegos. 
La mayoría de los videojuegos presentan ratings superiores al 70%.
""")
st.divider()

#Gráfica 2
st.markdown("### Rating vs Peak CCU")

fig, ax = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=df_filtrado,
    x='rating',
    y='peak_ccu',
    alpha=0.4,
    ax=ax
)

ax.set_yscale('log')

st.pyplot(fig)

st.divider()

#Gráfica 3
st.markdown("### Rating vs Precio")

fig, ax = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=df_filtrado,
    x='rating',
    y='price',
    alpha=0.4,
    ax=ax
)

st.pyplot(fig)

st.divider()

#ML

#Conclusiones
st.markdown("## Conclusiones")

