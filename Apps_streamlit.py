#Import de tout les modules nécessaires :

import pandas as pd
import streamlit as st
from st_on_hover_tabs import on_hover_tabs
import os
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from unidecode import unidecode
import unicodedata


#Codage de l'image de fond + initialisation de certains paramètres

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("https://media.istockphoto.com/id/1263930234/fr/vectoriel/fond-flou-abstrait-color%C3%A9-lumineux.jpg?s=612x612&w=0&k=20&c=r7iKE_lwe1ezClRnN9vkWZiysV_TRcVuz6Lbhy8e7N0=");
background-size: cover;
}}

[data-testid="stSidebar"] {{
background-image: url("https://i.goopics.net/k7192g.png");
background-size: cover;
}}

</style>
"""
st.markdown(
    """
    <style>
    body {
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(page_bg_img, unsafe_allow_html=True)
selected_genres = []
years_range = []
df_FR = pd.read_csv(r"df_FR.csv", sep=";", low_memory=False)
st.markdown("<style>" + open('./style/style.css').read() + '</style>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: black;'> FilmFinder! 🎬 </h1>", unsafe_allow_html=True)

with st.sidebar:
    tabs = on_hover_tabs(tabName=['Accueil','Recherche par rapport à un film', 'Recherche par genre et dates', 'Rechercher par rapport à un(e) acteur/actrice'],
                         iconName=['home', 'movie', 'settings', 'person'], default_choice=0)
    
if 'tab_selection' not in st.session_state:
    st.session_state.tab_selection = 'Accueil'    
if tabs == 'Accueil':
    st.markdown("<h2 style='text-align: center; color: black;'>Système de recommandation de films</h2>", unsafe_allow_html=True)

if tabs == 'Recherche par rapport à un film':
    st.session_state.tab_selection = 'Recherche par rapport à un film'
    #Titre onglet
    st.markdown("<h2 style='text-align: center; color: black;'>Entrez un film qui vous a plu📹 </h2>", unsafe_allow_html=True)
    # faire une copie de df_main
    df_copy2 = df_FR.copy()

    # Remplacer les valeurs manquantes dans 'genres' par une chaîne vide
    df_copy2['genres'] = df_copy2['genres'].fillna('')

    # Créer un dataframe avec des colonnes binaires pour chaque genre
    df_dummies = df_copy2['genres'].str.get_dummies(sep=',')
    df_dummies.columns = [col.replace('-', '_').replace(' ', '_').lower() for col in df_dummies.columns]

    # Concaténer le dataframe original avec le dataframe des genres binaires
    df_search = pd.concat([df_copy2, df_dummies], axis=1)

    # Enlever les colonnes inutiles pour la recherche
    df_search.drop(['genres', 'actor/actress', 'tconst', 'director', 'region'], axis=1, inplace=True)


    film = st.text_input("Nom du film : ")
    if film:
        film_normalized = unidecode(film)
        film_search = df_search[df_search['title'].apply(unidecode).str.contains(film_normalized, case=False)]
        films_list = film_search['title'].tolist()
        film_choice = st.selectbox("De quel film parlez-vous ?", films_list)

        film_genres = [col for col in df_search.columns if film_search.at[film_search.index[0], col] == 1 and col != 'title']

        # Multiplication des colonnes du genre par 5
        scaler = StandardScaler()
        num_col = df_search.select_dtypes('number')
        num_col_scaled = scaler.fit_transform(num_col)

        for genre in film_genres:
            genre_column_index = df_search.columns.get_loc(genre)
            num_col_scaled[:, genre_column_index] *= 5

        df_search[num_col.columns] = num_col_scaled


        if st.button("Rechercher des films similaires"):
            # Entraîner le modèle
            numerical_cols = df_search.select_dtypes('number')
            model_KNN_gen = NearestNeighbors(n_neighbors=10).fit(numerical_cols)
            film_choice_search = df_search[df_search['title'] == film_choice]
            neighbors_gen = model_KNN_gen.kneighbors(film_choice_search[numerical_cols.columns])
            closest_fil = neighbors_gen[1][0]
            closest_films = df_search['title'].iloc[closest_fil][5:10]

            st.write('<p style="color:black;">Films recommandés</p>',unsafe_allow_html=True)
            for film in closest_films:
                st.write(f'<p style="color:black;">- {film}</p>',unsafe_allow_html=True)
    else:
            st.write('<p style="color:black;">Entrez un film pour commencer</p>',unsafe_allow_html=True)
        
 #Code pour la partie "Recherche par genre et dates"

if tabs == 'Recherche par genre et dates':
    if "selected_genres" not in st.session_state:
        st.session_state.selected_genres = []
    st.session_state.tab_selection = 'Recherche par genre et dates' 
    #Titre onglet
    st.markdown("<h2 style='text-align: center;color:black;'>Selectionnez un ou des genre(s) de films ! 📹 </h2>", unsafe_allow_html=True)
    # Création d'une liste de tous les genres disponibles dans la base de données
    genres_list = list(set([genre for genres in df_FR['genres'].str.split(',') for genre in genres]))

    # Multiselect pour choisir les genres
    st.write("<span style='font-size:24px;font-weight:bold;color:black;'>Sélectionnez les genres que vous souhaitez voir</span>", unsafe_allow_html=True)

    selected_genres = st.multiselect("", genres_list)
    st.session_state.selected_genres = selected_genres
    # Afficher le nombre de lignes filtrées
    st.sidebar.write(f"{len(df_FR[df_FR['genres'].apply(lambda x: any(genre in x for genre in selected_genres))])} films trouvés")

    if st.button('Valider'):
        st.session_state.selected_genres = selected_genres
        st.session_state.tab_selection = "Dates"
             
    if "Dates":
    #Titre onglet
        st.markdown("<h2 style='text-align: center;color:black;'>Selectionnez une plage d'année 📆 </h2>", unsafe_allow_html=True)

        # Curseur pour choisir la plage de dates
        years_range = st.slider('Sélectionnez la plage de dates', 1946, 2023, (1970, 2023))
        years_range = list(years_range)

        # Afficher le nombre de lignes filtrées
        mask = df_FR['genres'].apply(lambda x: any(genre in x for genre in selected_genres)) & (df_FR['startYear'] >= years_range[0]) & (df_FR['startYear'] <= years_range[1])
        st.sidebar.write(f"{len(df_FR[mask])} films trouvés")
        df_FR_mask = df_FR[mask]

        # Bouton pour afficher les résultats
        if st.button('Afficher les résultats'):
            # Filtrage du DataFrame en fonction des genres sélectionnés et de la plage de dates
            filtered_df = df_FR[mask]
        
            # Filtrage du DataFrame en fonction des genres sélectionnés, de la plage de dates, et de la moyenne des numVotes
            mean_num_votes = filtered_df['numVotes'].mean()
            mask = mask & (filtered_df['numVotes'] >= mean_num_votes)
            # Sélection des 10 films les mieux notés
            top_films = filtered_df.sort_values('averageRating', ascending=False).head(5)['title'].tolist()
        
            # Création d'une liste de noms de films
            # Convertir la liste en ensemble pour supprimer les doublons
            unique_films = set(top_films)

            # Convertir l'ensemble en liste
            film_names = list(unique_films)

            # Affichage des noms de films
            st.write('<p style="color:black;">Voici la liste des 5 meilleurs films</p>',unsafe_allow_html=True)
            for i, name in enumerate(film_names):
                st.write(f'<p style="color:black;">- {name}</p>',unsafe_allow_html=True)
                
        
   
 
 #Code pour la partie "Recherche par rapport à un film"


    
 #Code pour la partie "Rechercher par rapport à un(e) acteur/actrice"

if tabs == 'Rechercher par rapport à un(e) acteur/actrice':

    st.session_state.tab_selection = 'Rechercher par rapport à un(e) acteur/actrice'
    #Titre onglet
    st.markdown("<h2 style='text-align: center;color:black;'>Entrez le nom d'un acteur ou actrice </h2>", unsafe_allow_html=True)
    # faire une copie de df_main
    df_copy3 = df_FR.copy()
    df_copy3['actor/actress'] = df_copy3['actor/actress'].fillna("")
    

    actor_actress = st.text_input("Nom d'un acteur ou actrice : ")
    if actor_actress:
        actor_films = df_copy3.loc[df_copy3['actor/actress'].str.contains(actor_actress, case=False)]
        # Calculer la moyenne des notes pour chaque film
        actor_films_avg = actor_films.groupby('title')['averageRating'].mean()
        # Trier les films en fonction de leur note moyenne
        actor_top_films = actor_films_avg.sort_values(ascending=False).head(5).index.tolist()
        
    else:
        st.write(f"Aucun film avec {actor_actress} trouvé.")

    if st.button("Rechercher des films"):
        # Afficher les cinq meilleurs films
        st.write(f'<p style="color:black;">Les cinqs meilleurs film avec {actor_actress}</p>',unsafe_allow_html=True)
        for i, title in enumerate(actor_top_films):
            st.write(f'<p style="color:black;">- {title}</p>',unsafe_allow_html=True)
    else:
        st.write('<p style="color:black;">Entrez un nom d acteur/actice pour commencer</p>',unsafe_allow_html=True)