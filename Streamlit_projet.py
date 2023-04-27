import plotly.graph_objs as go
import plotly.express as px
from load_data_streamlit import title_basics
from load_data_streamlit import big_df
import streamlit as st
import pandas as pd

def separate_genres(genres_str):
    """
    Convert a string of genres separated by commas into a list of separate genres.
    """
    return [g.strip() for g in genres_str.split(",")]

# Utilisation de la fonction "eval" pour transformer les chaînes de caractères en listes d'acteurs
big_df["actor/actress"] = big_df["actor/actress"].apply(lambda x: x.split(", ") if isinstance(x, str) else x)

# Utilisation de la fonction "explode" pour séparer chaque acteur en plusieurs lignes
df_actor = big_df.explode("actor/actress")

# Comptage du nombre d'occurrences de chaque nom d'acteur
actor_counts = df_actor["actor/actress"].value_counts()

# Affichage du nom de l'acteur le plus fréquent
top_actors = actor_counts.head(200)
top_actors_df = top_actors.reset_index().rename(columns={"index": "acteur", "actor/actress": "count"})
print(top_actors_df)

# Boucle sur chaque acteur pour créer des histogrammes individuels
colors = ['blue', 'green', 'red', 'orange', 'purple', 'pink', 'gray', 'brown', 'black', 'yellow']
traces = []
for i, actor in enumerate(top_actors.index):
    actor_data = df_actor["actor/actress"].value_counts()[actor]
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

#---------------------------------------------------------------------------


df_main = title_basics.copy()

df_main["genres_list"] = df_main["genres"].apply(separate_genres)

#Explode la liste des genre pour crée une ligne par genre
df_genres = df_main.explode("genres_list")

# Groupby startYear et genre, et compter le nombre de film pour chaque groupe
df_counts = df_genres.groupby(["startYear", "genres_list"]).size().reset_index(name="count")

# Créer la colonne "decade"
df_counts['decade'] = (df_counts['startYear'] // 10) * 10

# Regrouper par décennie et genre et compter le nombre de films
grouped_df = df_counts.groupby(['decade'])['count'].agg(['count', 'sum'])

# Compter le nombre total de films par décennie
total_count = grouped_df.groupby(['decade'])['sum'].sum().reset_index()
total_count.columns = ['decade', 'total_count']

# Réorganiser le DataFrame
result_df = grouped_df.reset_index()
result_df = result_df.merge(total_count, on='decade')
result_df = result_df[['decade', 'total_count']]


fig2 = px.line(result_df, x="decade", y="total_count", title='Évolution du nombre de film par décennie')
fig2.update_xaxes(range=[1940, 2010], title= "Décennie")
fig2.update_yaxes(title= "Nombre de film")
st.plotly_chart(fig2)


#---------------------------------------------------------------------------


df_main2 = title_basics.copy()

df_main2["genres_list"] = df_main2["genres"].apply(separate_genres)

# Explode la liste des genre pour crée une ligne par genre
df_genres = df_main2.explode("genres_list")

# Group by startYear et genre, et compter le nombre de film pour chaque groupe
df_counts = df_genres.groupby(["startYear", "genres_list"]).size().reset_index(name="count")


# Créer une colonne "decade" à partir de la colonne "startYear"
decade_intervals = list(range(1940, 2031, 10))
df_counts["decade"] = pd.cut(df_counts["startYear"], bins=decade_intervals, labels=decade_intervals[:-1])

# Regrouper les données par décennie et genre et faire la somme des comptages
df_grouped = df_counts.groupby(["decade", "genres_list"]).sum().reset_index()

# Créer un graphique en barres avec un curseur pour sélectionner la décennie
fig3 = go.Figure()

for decade in df_grouped["decade"].unique():
    df_decade = df_grouped[df_grouped["decade"] == decade]
    fig3.add_trace(go.Bar(
        x=df_decade["genres_list"],
        y=df_decade["count"],
        name=str(decade),
        visible=(decade == 1940)
    ))

fig3.update_layout(
    title="Nombre de films par décennie et par genre",
    xaxis_title="Genre",
    yaxis_title="Nombre de films",
    updatemenus=[
        {
            "buttons": [
                {
                    "label": str(decade),
                    "method": "update",
                    "args": [
                        {"visible": [d == decade for d in df_grouped["decade"].unique()]},
                        {"title": "Nombre de films par décennie et par genre - Années " + str(decade)}
                    ]
                } for decade in df_grouped["decade"].unique()
            ],
            "direction": "down",
            "showactive": True,
            "type": "dropdown",
            "x": 0.9,
            "y": 1.2
        }
    ]
)

st.plotly_chart(fig3)