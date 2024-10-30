import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

st.header("MyNextPint: App based on 1M+ beer reviews from Untappd")

#Recommendation Engine Backend
df = pd.read_csv("embedded_beer_list.csv")
embed = df.drop(columns=["beer_name", "beer_style", "brewery_name", "review_count"])
metadata = df[["beer_name", "beer_style", "brewery_name", "review_count"]]

def display_cards(series):
    with st.container(key = series['beer_name'], border=True):
        st.subheader(series['beer_name'].values[0])
        st.caption(series['beer_style'].values[0])
        st.write("ABV: "+str(round(series['beer_abv'].values[0], 3))+" | Brewed by: "+series['brewery_name'].values[0]+" | "+str(round(series['review_count'].values[0], 3))+" reviews")
        st.write("**Reviews:**")
        c1, c2 = st.columns(2)
        c1.write("Overall: "+str(round(series['review_overall'].values[0], 3)))
        c1.write("Aroma : "+str(round(series['review_aroma'].values[0], 3)))
        c1.write("Appearance: "+str(round(series['review_appearance'].values[0], 3)))
        c2.write("Palate: "+str(round(series['review_palate'].values[0], 3)))
        c2.write("Taste: "+str(round(series['review_taste'].values[0], 3)))

#def display_card_output(series):
#Frontend
st.write("")
st.write("**Your Next Pint:** Give us your favorite beer, we'll recommend you 5 more just like it")

with st.sidebar:
    options = df.sort_values(by="review_count", ascending=False)["beer_name"].values.tolist()
    input = st.selectbox("Choose from 22644 beers",options, index=None, placeholder="Select beer...")
    dis = True
    if input:
        dis=False
    generate = st.button("Generate", disabled=dis)

if generate:
    cols = st.columns([1,1.2])
    with cols[0]:
        st.header("Chosen beer:")
        choice = df[df["beer_name"]==input]
        display_cards(choice)


    with cols[1]:
        @st.cache_resource
        def similarity(embed):
            cosine_sim = cosine_similarity(embed)
            return cosine_sim

        cosine_sim = similarity(embed)

        def recommend_beers(beer_name, cosine_sim=cosine_sim, df=df):
            idx = df[df['beer_name'] == beer_name].index[0]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:6]
            beer_indices = [i[0] for i in sim_scores]
            return df.iloc[beer_indices].reset_index()
        
        st.header("Similar beers:")
        output = recommend_beers(input)

        with st.container(border=True, key="recommendations", height=550):
            for index, row in output.iterrows():
                row = output[output["beer_name"]==output.loc[index, "beer_name"]]
                display_cards(row)

