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

# DATA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

url = "https://github.com/pamelayva-8/Proyecto-BI-Videojuegos-Steam/raw/refs/heads/main/steam_limpio_2.csv"



df = pd.read_csv(url)

#Sidebar----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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


# CONTENT----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

st.markdown("##  Videojuegos steam")

st.divider()

#Métricas----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

#Pregunta----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
#Estadísticas descriptivas----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.markdown("### Estadísticas descriptivas")

st.dataframe(
    df_filtrado[
        [
            'rating',
            'price',
            'peak_ccu',
            'owners_numeric'
        ]
    ].describe().round(2)
)
st.divider()

#Videojuegos----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
#Gráfica 1------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

#Gráfica 2----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

st.info("""
Esta gráfica compara la calificación de los videojuegos con el máximo número de usuarios conectados simultáneamente (Peak CCU).
Cada punto representa un videojuego. Existen videojuegos con ratings altos y bajos independientemente de su popularidad.
Tener muchos usuarios simultáneos no garantiza una mejor calificación.
""")

st.divider()

#Gráfica 3----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

st.info("""
Esta gráfica muestra la relación entre el precio de un videojuego y su calificación.
No se observa una relación clara entre el precio y el rating.
Los videojuegos económicos pueden obtener calificaciones tan altas como los más costosos.
""")

st.divider()

#Gráfica 4: Heatmap ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

st.markdown("### Matriz de Correlación General")

st.info("""
La matriz de correlación permite identificar qué tan relacionadas están las variables numéricas entre sí.
Los valores cercanos a 1 indican una relación fuerte positiva.
""")

# Variables numéricas
corr = df_filtrado[
    [
        'rating',
        'price',
        'peak_ccu',
        'recommendations',
        'owners_numeric',
        'average_playtime_forever',
        'achievements',
        'dlc_count'
    ]
].corr()

# Crear figura
fig, ax = plt.subplots(figsize=(10,8))

sns.heatmap(
    corr,
    annot=True,
    cmap='coolwarm',
    fmt='.2f',
    ax=ax
)

ax.set_title('Matriz de Correlación')

st.pyplot(fig)

st.success("""
Las correlaciones con el rating son relativamente bajas, lo que indica que la satisfacción de los usuarios depende de múltiples factores y no de una sola variable.
""")

st.divider()

#Gráfica 5: Influencia del Publisher----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.markdown("### Influencia del Publisher")

st.info("""
Esta gráfica compara la distribución de ratings entre los principales publishers de Steam.
Cada caja representa cómo se distribuyen las calificaciones de los juegos publicados por una empresa.
""")

# Solo publishers válidos
df_publishers = df_filtrado[
    df_filtrado['primary_publisher'].notna()
].copy()

# Top 12 publishers
top_publishers = (
    df_publishers['primary_publisher']
    .value_counts()
    .head(12)
    .index
)

# Juegos de esos publishers
df_top_publishers = df_publishers[
    df_publishers['primary_publisher'].isin(top_publishers)
]

# Ordenar por mediana de rating
orden_mediana = (
    df_top_publishers
    .groupby('primary_publisher')['rating']
    .median()
    .sort_values(ascending=False)
    .index
)

fig, ax = plt.subplots(figsize=(12,8))

sns.boxplot(
    data=df_top_publishers,
    x='rating',
    y='primary_publisher',
    order=orden_mediana,
    ax=ax
)

st.pyplot(fig)

st.success("""
Algunos publishers presentan consistentemente ratings más altos que otros, lo que sugiere que la reputación del distribuidor podría influir en la percepción de calidad del videojuego.
""")

st.divider()

#Gráfica 6: Heatmap Publisher ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.markdown("### Reputación del Publisher")
st.info("""
Se analizó si la reputación histórica de un publisher está relacionada con el desempeño de sus videojuegos.
""")
# Crear reputación del publisher
publisher_stats = (
    df_filtrado
    .groupby('primary_publisher')['rating']
    .median()
    .rename('publisher_median_rating')
)

# Agregar columna al dataframe
df_pub = df_filtrado.merge(
    publisher_stats,
    on='primary_publisher',
    how='left'
)

# Variables para correlacionar
vars_interes = [
    'publisher_median_rating',
    'rating',
    'price',
    'peak_ccu',
    'owners_numeric',
    'average_playtime_forever',
    'dlc_count',
    'achievements'
]

# Matriz de correlación ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
matriz_corr = df_pub[vars_interes].corr()

# Heatmap
fig, ax = plt.subplots(figsize=(10,8))

sns.heatmap(
    matriz_corr,
    annot=True,
    cmap='coolwarm',
    fmt='.2f',
    linewidths=0.5,
    ax=ax
)

ax.set_title(
    'Correlación entre Reputación del Publisher y Otras Variables'
)

st.pyplot(fig)

st.success("""
La variable publisher_median_rating representa la reputación histórica del publisher.
Si presenta correlaciones positivas con el rating, podría indicar que algunos distribuidores tienden a publicar juegos mejor valorados por los usuarios.
""")

st.divider()

#Gráfica 7: Idioma ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


st.markdown("### Rating según Cantidad de Idiomas")

def contar_idiomas(x):

    if pd.isna(x):
        return 0

    return len(
        [
            idioma.strip()
            for idioma in str(x).split(',')
            if idioma.strip()
        ]
    )

df_idiomas = df_filtrado.copy()

df_idiomas['total_languages'] = (
    df_idiomas['supported_languages']
    .apply(contar_idiomas)
)

def grupo_idiomas(n):

    if n == 1:
        return "1 idioma"

    elif n <= 5:
        return "2-5 idiomas"

    elif n <= 10:
        return "6-10 idiomas"

    else:
        return "+10 idiomas"

df_idiomas['grupo_idiomas'] = (
    df_idiomas['total_languages']
    .apply(grupo_idiomas)
)

idiomas_rating = (
    df_idiomas
    .groupby('grupo_idiomas')['rating']
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(8,5))

sns.barplot(
    data=idiomas_rating,
    x='grupo_idiomas',
    y='rating',
    ax=ax
)

ax.set_ylabel("Rating Promedio")

st.pyplot(fig)

st.info("""
Esta gráfica analiza si ofrecer soporte para más idiomas está relacionado con una mejor calificación.
Los videojuegos con mayor localización pueden alcanzar una audiencia más amplia.
""")

st.divider()

#Gráfica 8: Sistema operativo ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

st.markdown("### Rating Promedio por Sistema Operativo")

so_data = pd.DataFrame({
    'Sistema Operativo': [
        'Windows',
        'Mac',
        'Linux'
    ],
    'Rating Promedio': [
        df_filtrado[df_filtrado['windows']==True]['rating'].mean(),
        df_filtrado[df_filtrado['mac']==True]['rating'].mean(),
        df_filtrado[df_filtrado['linux']==True]['rating'].mean()
    ]
})

fig, ax = plt.subplots(figsize=(8,5))

sns.barplot(
    data=so_data,
    x='Sistema Operativo',
    y='Rating Promedio',
    ax=ax
)

ax.set_ylim(0,100)

st.pyplot(fig)

st.info("""
Esta gráfica compara el rating promedio de los videojuegos según los sistemas operativos que soportan.
Permite observar si existe alguna diferencia en la percepción de calidad entre plataformas.
""")
st.divider()

#ML ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

st.markdown("### Machine Learning: ")
st.info("""
Se utilizó un modelo Random Forest para estimar su calificación o rating por medio de las variables que tienen mayor influencia sobre la calificación positiva de un videojuego
""")

st.divider()
#Conclusiones----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.markdown("## Conclusiones")

