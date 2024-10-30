import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans


st.header("MyNextPint: App based on 1M+ beer reviews from Untappd")

#Recommendation Engine Backend
df = pd.read_csv("embedded_beer_list.csv")
embed = df.drop(columns=["beer_name", "beer_style", "brewery_name", "review_count"])

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

#Frontend
st.write("")
st.write("**Your Next Pint:** Give us your favorite beer, we'll recommend you 5 more just like it")

@st.cache_resource
def cluster(embed, n):
            kmeans = KMeans(n_clusters=30)
            cluster_labels = kmeans.fit_predict(embed)
            embed['style_cluster'] = cluster_labels
            return embed

embed = cluster(embed, 30)

with st.sidebar:
    options = df.sort_values(by="review_count", ascending=False)["beer_name"].values.tolist()
    input = st.selectbox("Choose from 22644 beers",options, index=None, placeholder="Select beer...")
    generate = st.button("Generate")

if generate and input:
    cols = st.columns([1,1.2])
    with cols[0]:
        st.header("Chosen beer:")
        choice = df[df["beer_name"]==input]
        display_cards(choice)

    with cols[1]:

        def recommend_beers(beer_name, embed=embed, df=df):
            selected_idx = df[df["beer_name"] == beer_name].index[0]
            selected_cluster = embed.loc[selected_idx, 'style_cluster']
            
            # Filter for the same cluster
            cluster_df = df[embed['style_cluster'] == selected_cluster]
            cluster_embed = embed[embed['style_cluster'] == selected_cluster].drop(columns=['style_cluster'])

            # Compute cosine similarity within the cluster
            cosine_sim = cosine_similarity(cluster_embed)
            selected_cluster_idx = cluster_df.index.get_loc(selected_idx)  # Index within the cluster

            # Get similarity scores for the selected beer
            sim_scores = list(enumerate(cosine_sim[selected_cluster_idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]  # Top 5 similar beers

            # Map to original indices
            beer_indices = cluster_df.iloc[[i[0] for i in sim_scores]].index
            return df.loc[beer_indices].reset_index(drop=True)

        
        st.header("Similar beers:")
        output = recommend_beers(input)

        with st.container(border=True, key="recommendations", height=550):
            for index, row in output.iterrows():
                row = output[output["beer_name"]==output.loc[index, "beer_name"]]
                display_cards(row)

elif generate and not input:
    st.warning("Enter input")
