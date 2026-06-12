import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split


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


show_header("Descifrando el éxito en Steam")

st.divider()

# DATA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

url = "https://github.com/pamelayva-8/Proyecto-BI-Videojuegos-Steam/raw/refs/heads/main/steam_limpio_3.csv"



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

#Gráfica 9: Género ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


st.markdown("### Rating Promedio por Género")

from collections import defaultdict

genre_ratings = defaultdict(list)

for _, row in df_filtrado.iterrows():

    if pd.notna(row['genres']):

        generos = (
            str(row['genres'])
            .replace("[","")
            .replace("]","")
            .replace("'","")
            .split(",")
        )

        for genero in generos:
            genre_ratings[genero.strip()].append(row['rating'])

# Promedio por género
genre_avg = {
    genero: sum(ratings)/len(ratings)
    for genero, ratings in genre_ratings.items()
    if len(ratings) > 50
}

genre_avg = (
    pd.DataFrame(
        genre_avg.items(),
        columns=['Genero','Rating']
    )
    .sort_values('Rating', ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,6))

sns.barplot(
    data=genre_avg,
    x='Rating',
    y='Genero',
    ax=ax
)

ax.set_title("Top Géneros por Rating Promedio")

st.pyplot(fig)

st.info("""
Esta gráfica muestra el rating promedio de los géneros más relevantes de Steam.
Permite identificar qué tipos de videojuegos suelen recibir mejores calificaciones por parte de los usuarios.
""")

st.divider()
#ML ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

st.markdown("### Machine Learning: Random Forest ")
st.info("""
Se  utilizó un modelo Random Forest Regressor para identificar qué características del videojuego tienen mayor influencia sobre su calificación positiva. Se ajustaron los hiperparámetros del modelo
(n_estimators=500, max_depth=20, min_samples_split=5) para mejorar su desempeño.
""")


@st.cache_resource
def cargar_modelo():
    import gdown
    import joblib
    import os
    ruta = "modelo_steam_rf.pkl"
    if not os.path.exists(ruta):
        gdown.download(
            "https://drive.google.com/uc?id=1EGpHQ_KkMyPqEVXxCUeVESI5oU3DoicI",
            ruta,
            quiet=True
        )
    return joblib.load(ruta)
 
with st.spinner("Cargando modelo... esto solo tarda la primera vez ⏳"):
    modelo = cargar_modelo()
 
# Preparar variables
variables_modelo = [
    'price', 'peak_ccu_log', 'total_languages', 'tipo_publisher',
    'owners_numeric', 'achievements', 'dlc_count', 'os_score',
    'genre_Indie', 'genre_Adventure', 'genre_Action', 'genre_Casual',
    'genre_Simulation', 'genre_Strategy', 'genre_RPG',
    'genre_Early Access', 'genre_Free To Play', 'genre_Sports'
]
 
if 'peak_ccu_log' not in df.columns:
    df['peak_ccu_log'] = np.log1p(df['peak_ccu'])
 
if 'os_score' not in df.columns:
    df['os_score'] = df[['windows', 'mac', 'linux']].sum(axis=1)
 
cols_disponibles = [c for c in variables_modelo if c in df.columns]
df_ml = df[cols_disponibles + ['rating']].dropna()
 
X = df_ml[cols_disponibles]
y = df_ml['rating']
 
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
y_pred = modelo.predict(X_test)
 
r2  = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
 
# Métricas
col1, col2 = st.columns(2)
with col1:
    st.metric("R² Score", round(r2, 4),
              help="Qué tan bien explica el modelo la variación del rating (1.0 = perfecto)")
with col2:
    st.metric("Error promedio (MAE)", f"± {round(mae, 2)}%",
              help="En promedio, el modelo se equivoca este % al estimar el rating")
 
st.divider()


# ==================================================================================================================================================================================
# --- SIMULADOR INTERACTIVO (PREDICCIÓN EN VIVO) ---
# ==================================================================================================================================================================================
st.markdown("### 🔮 Simulador de Éxito: Estima tu Rating preliminar")
st.write("Configura las características de tu nuevo proyecto de videojuego para calcular la estimación del Rating esperado en Steam:")

# Creamos dos columnas estéticas para los inputs numéricos y de control
col_sim1, col_sim2 = st.columns(2)

with col_sim1:
    st.markdown("##### 💰 Métricas Comerciales y de Mercado")
    input_precio = st.slider("Precio sugerido de lanzamiento (USD)", min_value=0.0, max_value=120.0, value=19.99, step=0.99)
    input_peak = st.number_input("Pico esperado de jugadores simultáneos (Peak CCU)", min_value=0, max_value=1000000, value=1200, step=100)
    input_owners = st.number_input("Estimación base de propietarios (Owners)", min_value=0, max_value=50000000, value=50000, step=10000)
    input_dlc = st.slider("Cantidad de contenidos descargables (DLCs)", min_value=0, max_value=30, value=0, step=1)

with col_sim2:
    st.markdown("##### ⚙️ Localización y Atributos Técnicos")
    input_idiomas = st.slider("Número de idiomas con soporte completo", min_value=1, max_value=35, value=5, step=1)
    input_achievements = st.number_input("Cantidad de logros integrados (Achievements)", min_value=0, max_value=2000, value=40, step=10)
    input_os = st.slider("Sistemas operativos compatibles (Windows / Mac / Linux)", min_value=1, max_value=3, value=1, step=1, 
                         help="1 = Solo Windows, 2 = Dos plataformas, 3 = Multiplataforma completo")
    input_pub = st.slider("Índice de jerarquía del Publisher (Estrategia comercial)", min_value=0, max_value=5, value=1, step=1,
                         help="0-1 = Indie/Autopublicado, 2-3 = Distribuidor mediano, 4-5 = Gran Empresa AAA")

# Agregamos un multiselect dinámico para controlar los géneros de forma sumamente intuitiva
st.markdown("##### 🎭 Clasificación por Géneros")
lista_generos_disponibles = [
    'Indie', 'Adventure', 'Action', 'Casual', 'Simulation', 
    'Strategy', 'RPG', 'Early Access', 'Free To Play', 'Sports'
]
generos_seleccionados = st.multiselect(
    "Selecciona todos los géneros que describan a tu videojuego:",
    options=lista_generos_disponibles,
    default=['Indie', 'Action']
)

st.write("") # Espaciador visual

# Botón detonador del modelo predictivo
if st.button("🚀 Calcular Calificación Estimada"):
    
    # 1. Construimos un diccionario base con los inputs mapeados a sus nombres de variables correspondientes
    valores_usuario = {
        'price': input_precio,
        'peak_ccu_log': np.log1p(input_peak),  # Aplicamos la transformación logarítmica exacta que requiere el modelo
        'total_languages': input_idiomas,
        'tipo_publisher': input_pub,
        'owners_numeric': input_owners,
        'achievements': input_achievements,
        'dlc_count': input_dlc,
        'os_score': input_os
    }
    
    # 2. Mapeamos las banderas binarias (0 o 1) para cada uno de los géneros del modelo
    for genero in lista_generos_disponibles:
        nombre_columna = f'genre_{genero}'
        valores_usuario[nombre_columna] = 1 if genero in generos_seleccionados else 0
        
    # 3. EL TRUCO MAGISTRAL: Filtramos y ordenamos la fila de datos usando EXACTAMENTE el orden de 'cols_disponibles'
    # Si alguna variable de la lista general no llegó a quedar en el modelo final, .get(col, 0) la previene de fallar.
    datos_estructurados = {col: valores_usuario.get(col, 0) for col in cols_disponibles}
    
    # 4. Convertimos a DataFrame asegurando un calce matemático perfecto de dimensiones y nombres
    datos_nuevos = pd.DataFrame([datos_estructurados], columns=cols_disponibles)
    
    # 5. Ejecutar la predicción
    prediccion = modelo.predict(datos_nuevos)[0]
    
    # Mostrar resultados en formato KPI corporativo de BI
    st.success("¡Simulación completada con éxito!")
    
    col_res1, col_res2 = st.columns([2, 3])
    with col_res1:
        st.metric(
            label="⭐ Rating Estimado", 
            value=f"{prediccion:.2f} %",
            delta=f"{prediccion - 70:.2f} % vs Media de Steam (70%)"
        )
    with col_res2:
        # Generar un insight de negocio según el porcentaje obtenido
        if prediccion >= 82:
            st.balloons()
            st.markdown("🏅 **Insight de BI:** ¡Éxito potencial! El modelo detecta una combinación altamente competitiva. La estructura de precio y el balance de soporte al usuario predicen una recepción excelente (*Very Positive*).")
        elif prediccion >= 70:
            st.markdown("📈 **Insight de BI:** El título se mantendrá en el promedio saludable del mercado. Para escalar el rating, considera optimizar la localización (añadir más idiomas) o expandir el plan de logros.")
        else:
            st.markdown("⚠️ **Insight de BI:** Riesgo comercial moderado. Una baja tasa de retención o un precio desbalanceado para el nicho de mercado seleccionado podría empujar la calificación a terreno mixto.")

st.divider()




 
# Importancia de variables
st.markdown("#### ¿Qué características influyen más en el rating?")
 
nombres_legibles = {
    'price':              'Precio',
    'peak_ccu_log':       'Pico de jugadores simultáneos (log)',
    'total_languages':    'Cantidad de idiomas',
    'tipo_publisher':     'Tipo de publisher',
    'owners_numeric':     'Estimado de propietarios',
    'achievements':       'Logros (achievements)',
    'dlc_count':          'Número de DLCs',
    'os_score':           'Sistemas operativos soportados',
    'genre_Indie':        'Género: Indie',
    'genre_Adventure':    'Género: Aventura',
    'genre_Action':       'Género: Acción',
    'genre_Casual':       'Género: Casual',
    'genre_Simulation':   'Género: Simulación',
    'genre_Strategy':     'Género: Estrategia',
    'genre_RPG':          'Género: RPG',
    'genre_Early Access': 'Género: Early Access',
    'genre_Free To Play': 'Género: Free to Play',
    'genre_Sports':       'Género: Deportes',
}
 
importancias = pd.DataFrame({
    'Variable':    [nombres_legibles.get(v, v) for v in cols_disponibles],
    'Importancia': modelo.feature_importances_
}).sort_values('Importancia', ascending=True).tail(10)
 
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=importancias, x='Importancia', y='Variable', palette='Blues_r', ax=ax)
ax.set_title('Top 10 variables con mayor influencia en el rating', fontweight='bold')
ax.set_xlabel('Importancia relativa')
ax.set_ylabel('')
st.pyplot(fig)
 
st.success("""
Las variables con mayor peso explican por qué un juego tiene buena calificación.
Características como logros, idiomas soportados y tipo de publisher son factores
que un desarrollador puede considerar antes del lanzamiento.
""")
 

 
st.warning("""
Variables como el pico de jugadores simultáneos y el estimado de
propietarios son parcialmente consecuencia del éxito del juego. Se incluyen en el modelo
pero se interpretan con cautela.
""")
 
st.divider()


