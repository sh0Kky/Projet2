import pandas as pd
import pandas_profiling
import streamlit as st
from st_on_hover_tabs import on_hover_tabs
import os
from streamlit_pandas_profiling import st_profile_report




st.set_page_config(layout="wide", page_title=" 💻📊 IIIDATA TUTO ")
st.markdown('<style>' + open('./style/style.css').read() + '</style>', unsafe_allow_html=True)

st.title("  💻 Analyse des données 📊 ")


if os.path.exists('./data/dataset.csv'): 
    df = pd.read_csv('./data/dataset.csv', index_col=None)

with st.sidebar:
    
    tabs = on_hover_tabs(tabName=['Charger les données', 'Visualiser'], 
                         iconName=['upload file', 'analytics', 'download'], default_choice=0)
    st.image("./style/iiidata.png")

if tabs == 'Charger les données':
    file = st.file_uploader("Chargez votre fichier .csv")
    #separator = st.radio("Si votre dataset ne s'affiche pas correctement, sélectionner le bon séparateur", [",", ";"])
    if file: 
        df = pd.read_csv(file, index_col=None, sep = None)
        df.to_csv('dataset.csv', index=None)
        # if len(df.columns) >= 2 : 
        st.success("Données chargées correctement, vous pouvez passer à l'analyse. Rendez-vous dans l'onglet 'ANALYSER' 📊")
        # else : 
        #     st.error('Il semblerait que vous avez sélectionné le mauvais séparateur')
        st.dataframe(df)
    
        
        

elif tabs == 'Analyser':
    st.header("Analyse de la qualité et exploration des données")
    # Boucle sur chaque acteur pour créer des histogrammes individuels
colors = ['blue', 'green', 'red', 'orange', 'purple', 'pink', 'gray', 'brown', 'black', 'yellow']
traces = []
for i, actor in enumerate(top_actors.index):
    actor_data = df["actor/actress"].value_counts()[actor]
    trace = go.Bar(x=[actor], y=[actor_data], name=actor, visible=(i==0),
                   marker=dict(color=colors[i % len(colors)]))
    traces.append(trace)

# Création de la figure
fig1 = go.Figure(data=traces)

# Ajout d'un curseur pour naviguer entre les différentes barres
updatemenus = [
    {
        "buttons": [
            {
                "label": "Top 10",
                "method": "update",
                "args": [{"visible": [True] * 10 + [False] * (len(traces) - 10)}, {"title": "Top 10 acteurs"}],
            },
            {
                "label": "11-20",
                "method": "update",
                "args": [{"visible": [False] * 10 + [True] * 10 + [False] * (len(traces) - 20)}, {"title": "Acteurs 11 à 20"}],
            },
            {
                "label": "21-30",
                "method": "update",
                "args": [{"visible": [False] * 20 + [True] * 10 + [False] * (len(traces) - 30)}, {"title": "Acteurs 21 à 30"}],
            },
            {
                "label": "31-40",
                "method": "update",
                "args": [{"visible": [False] * 30 + [True] * 10 + [False] * (len(traces) - 40)}, {"title": "Acteurs 31 à 40"}],
            },
            {
                "label": "41-50",
                "method": "update",
                "args": [{"visible": [False] * 40 + [True] * 10 + [False] * (len(traces) - 50)}, {"title": "Acteurs 41 à 50"}],
            },
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 10},
        "showactive": True,
        "type": "buttons",
        "x": 0.1,
        "y": 1.1,
    }
]

# Configuration de la mise en page
fig1.update_layout(
    title="Top 10 acteurs",
    xaxis_title="Acteur",
    yaxis_title="Nombre d'apparitions",
    updatemenus=updatemenus,
)
st.plotly_chart(fig1)
st.success("Rapport genéré correctement, rendez-vous dans l'onglet 'EXPORTER' pour télécharger votre rapport 💾 ")
    


   
    



