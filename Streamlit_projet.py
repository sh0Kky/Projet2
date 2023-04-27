import plotly.graph_objs as go
import plotly.express as px
import streamlit as st
import pandas as pd

top_actors= pd.read_csv(r"df_grouped.csv", sep = ";", low_memory=False)
result_df = pd.read_csv(r"result_df.csv", sep = ";" , low_memory=False)
df_grouped = pd.read_csv(r"top_actors_df.csv", sep = ";", low_memory=False)



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


result_df = result_df[['decade', 'total_count']]


fig2 = px.line(result_df, x="decade", y="total_count", title='Évolution du nombre de film par décennie')
fig2.update_xaxes(range=[1940, 2010], title= "Décennie")
fig2.update_yaxes(title= "Nombre de film")
st.plotly_chart(fig2)


#---------------------------------------------------------------------------


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