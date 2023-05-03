import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# charger les données
df_main = pd.read_csv(r"C:\Users\rapha\OneDrive\Bureau\WCS\Projet 2\Data\Datadf_main.csv", sep = ";", low_memory=False)

# faire une copie de df_main
df_copy = df_main.copy()

# remplacer les valeurs manquantes dans genres par "" 
df_copy['genres'] = df_copy['genres'].fillna('')

# créer un dataframe avec des colonnes binaires pour chaque genre
df_dummies = df_copy["genres"].str.get_dummies(sep=",")
df_dummies.columns = ['genre_' + col.replace('-', '_').replace(' ', '_').lower() for col in df_dummies.columns]

# concaténer le dataframe original avec le dataframe des genres binaires
df_search = pd.concat([df_copy, df_dummies], axis=1)

# enlever les colonnes inutiles pour la recherche
df_search.drop(['genres', 'actor/actress', 'tconst', 'director'], axis=1, inplace=True)

# entrainer le modèle
num_col = df_search.select_dtypes('number')
model_KNN_gen = NearestNeighbors(n_neighbors=5).fit(num_col)

st.title("Recherche de films")

film = st.text_input("Nom du film : ")
if film:
    film_search = df_search.loc[df_search['primaryTitle'].str.contains(film, case=False)]
    films_list = film_search['primaryTitle'].tolist()
    film_choice = st.selectbox("De quel film parlez-vous ?", films_list)

    if st.button("Rechercher des films similaires"):
        neighbors_gen = model_KNN_gen.kneighbors(df_search.loc[df_search['primaryTitle'] == film_choice, num_col.columns])
        closest_fil = neighbors_gen[1][0]
        closest_film = df_search['primaryTitle'].iloc[closest_fil]
        st.write("Films les plus similaires : ")
        for film in closest_film:
            st.write("- " + film)
else:
    st.write("Entrez un nom de film pour commencer.")

