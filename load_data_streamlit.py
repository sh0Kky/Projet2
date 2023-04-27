import pandas as pd
name_basics = pd.read_csv(r"https://raw.githubusercontent.com/sh0Kky/Projet2/name_basics_tri.csv", na_values=['\\N'], sep = ";", low_memory=False)
title_basics = pd.read_csv(r"https://raw.githubusercontent.com/sh0Kky/Projet2/title_basics_tri_export.csv", low_memory=False)
title_ratings = pd.read_csv(r"https://raw.githubusercontent.com/sh0Kky/Projet2/title_ratings_data.tsv", sep = "\t", low_memory=False)
big_df = pd.read_csv(r"https://raw.githubusercontent.com/sh0Kky/Projet2/Datadf_main.csv", sep = ";", low_memory=False)
                                            