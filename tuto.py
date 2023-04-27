import pandas as pd
import pandas_profiling
import streamlit as st
from st_on_hover_tabs import on_hover_tabs
import os
from streamlit_pandas_profiling import st_profile_report



st.set_page_config(layout="wide")
st.markdown('<style>' + open('./style/style.css').read() + '</style>', unsafe_allow_html=True)
if os.path.exists('./data/dataset.csv'): 
    df = pd.read_csv('./data/dataset.csv', index_col=None)
st.title("Tuto analyse automatisée de vos données ")
with st.sidebar:
    tabs = on_hover_tabs(tabName=['Charger les données', 'Analyser', 'Exporter'], 
                         iconName=['upload file', 'analytics', 'download'], default_choice=0)
    st.image("./style/iiidata.png")

if tabs == 'Charger les données':
    file = st.file_uploader("Chargez vos données")
    separator = st.radio("Si votre dataset ne s'affiche pas correctement,sélectionner le bon séparateur", 
                         [",", ";"])
    if file: 
        df = pd.read_csv(file, index_col=None, sep = separator)
        df.to_csv('./data/dataset.csv', index=None)
        if len(df.columns) >= 2 : 
            st.success("Données chargées correctement, vous pouvez passer à l'analyse")
        else : 
            st.error('Il semblerait que vous avez sélectionné le mauvais séparateur')
        st.dataframe(df)
    
        
        

elif tabs == 'Analyser':
    st.header("Rapport d'analyse exploratoire des données")
    profile_df = df.profile_report()
    st_profile_report(profile_df)
    profile_df.to_file("output.html")
    

elif tabs == 'Exporter':
    with open("output.html", "rb") as f: 
        dl = st.download_button("Télécharger le rapport 💾 ", f, "rapport_analyse_data.html")
        st.balloons()
        # if dl : 
            
    
   
    






