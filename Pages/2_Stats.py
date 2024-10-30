import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("embedded_beer_list.csv").sort_values(by="review_count", ascending=False).reset_index().drop(columns=["index", "style_embed"])


with st.sidebar:
    styles = st.multiselect("Choose from "+ str(len(df["beer_style"].drop_duplicates()))+" beer styles", df["beer_style"].drop_duplicates().values, placeholder="All styles")
    if not styles:
        styles = df["beer_style"].values
    data = df[df["beer_style"].isin(styles)]

    abvdata = data["beer_abv"].sort_values().values
    startabv, endabv = st.select_slider("ABV", options=abvdata, value =(min(abvdata), max(abvdata)))
    data = data[(data["beer_abv"] <= endabv) & (data["beer_abv"] >= startabv)]

    startrating, endrating = st.select_slider("Rating", options=[1,2,3,4,5], value=(1,5))
    data = data[(data["review_overall"] <= endrating) & (data["review_overall"] >= startrating)]

#ROW 1
with st.container(key="popular"):
    c1,c2 = st.columns(2)
    with c1:
        value = data.sort_values(by="review_count", ascending=False)[:1].values[0]
        st.metric(label="Most popular beer", value=value[0], delta=str(value[-1])+ " reviews")
    with c2:
        value = data[["brewery_name", "review_count"]].groupby("brewery_name").sum().sort_values(by="review_count", ascending=False).reset_index().values[0]
        st.metric(label="Most popular brewery", value=value[0], delta=str(value[-1])+ " reviews")

#Fig1: Reviews per beer
fig1 = px.bar(data.sort_values(by="review_count", ascending=False)[:7], x="review_count", y="beer_name", text= "beer_name", color="review_count", color_continuous_scale="ylorbr", text_auto=True, orientation="h", height=300)
fig1.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False, title="Reviews per beer")
fig1.update_traces(texttemplate = '%{y} (%{x})', textposition = "inside")
fig1.update_yaxes(showticklabels=False)

numcols = ['review_overall', 'review_aroma', 'review_appearance', 'review_palate', 'review_taste', 'beer_abv']
review_corr = data[numcols].corr()["review_overall"].drop("review_overall").sort_values(ascending=False).reset_index()
review_corr = review_corr.rename(columns={"index": "factor", "review_overall":"correlation"})
review_corr["correlation"] = round(review_corr["correlation"],2)

fig2 = px.bar(review_corr, x="correlation", y="factor", color="correlation", color_continuous_scale="ylorbr", text_auto=True, orientation="h", height=300)
fig2.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False, title="Factors affecting overall rating")
fig2.update_traces(texttemplate = '%{y} (%{x})', textposition = "inside")
fig2.update_yaxes(showticklabels=False)

#ROW 2
with st.container(key="middlecharts", height=300, border=True):
    c1,c2, col3 = st.columns(3, vertical_alignment="top")
    c1.plotly_chart(fig1)

    with c2.container(key="ratings", border=False, height = 225):
        st.write("**Average Ratings**")
        c1, c2, c3, c4 = st.columns([1,4,4,4])
        c2.metric(label="Overall", value=round(data["review_overall"].mean(), 2))
        c2.metric(label="Aroma", value=round(data["review_aroma"].mean(), 2))
        c3.metric(label="Appearance", value=round(data["review_appearance"].mean(), 2))
        c3.metric(label="Palate", value=round(data["review_palate"].mean(), 2))
        c4.metric(label="Taste", value=round(data["review_taste"].mean(), 2))
    
    col3.plotly_chart(fig2)


data_avg = data[numcols].groupby("beer_abv").median().reset_index()

bins = [1.0, 3.0, 5.0, 8.0, 10.0, 12.0, 15.0,18.0, 25.0, 30.0, 40.0, 50.0, 60.0]
labels = [f"{bins[i]}-{bins[i + 1]}" for i in range(len(bins) - 1)]

data_avg["abv_bins"] = pd.cut(data_avg['beer_abv'], bins=bins, labels=labels, right=False)
data_avg = data_avg.groupby("abv_bins").median().reset_index()

colorscale=["#f0e76e", "#cda037", "#b38e2e", "#9a751e", "#755e14"]

fig3 = px.line(data_avg[:9], x="abv_bins", y=["review_overall", "review_aroma", "review_appearance", "review_taste", "review_palate"], height=370, color_discrete_sequence=colorscale)
fig3.update_layout(title="Customer preference changing by ABV", showlegend=False, width=900, xaxis=dict(range=[0, 10]), yaxis=dict(range=[3,4.48]))

fig3.update_yaxes(showgrid=False)
for i, d in enumerate(fig3.data):
    fig3.add_scatter(x=[d.x[-1]], y = [d.y[-1]],
                    mode = 'markers+text',
                    text = f'{d.name}: {d.y[-1]}',
                    textfont = dict(color=d.line.color),
                    textposition='middle right',
                    marker = dict(color = d.line.color, size = 12),
                    legendgroup = d.name,
                    showlegend=False)
    
#ROW 3
with st.container(key="bottomcharts"):  
    c1, c2=st.columns([1.2,2])
    c1.write("**Data**")
    c1.dataframe(data, height=300, hide_index=True)
    c2.plotly_chart(fig3)
