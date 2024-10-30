import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("merged_brewery_data.csv")
df["Barrel Growth"]*=100
with st.sidebar:
    factor = st.selectbox("Variables", df.drop(columns="State").columns)
    states = st.multiselect("States", df["State"].values)

    if not states:
        states = df["State"].values

    data = df[["State", factor]]
    data = data[data["State"].isin(states)]

map = px.choropleth(data, locations=states, color=factor, locationmode='USA-states', scope='usa', color_continuous_scale="ylorbr")
title = factor+" (US States)"
map.update_layout(title=title, coloraxis_showscale=False, geo_bgcolor="#fffff2")

with st.container(key='map', border=True, height=420):
    c1, c2 = st.columns([2.5,1])
    c1.plotly_chart(map)
    c2.write(data.sort_values(by=factor, ascending=False).reset_index().drop(columns="index"))

with st.container(key="leaderboard", border=True):
    st.write("**Leaderboard**")
    c1, c2, c3, c4 = st.columns([1,0.9,1.1,1.11])
    c1.write(df[["State", "2012 Craft Barrels"]].sort_values(by="2012 Craft Barrels", ascending=False)[:6].reset_index().drop(columns="index"))
    c2.write(df[["State", "Barrel Growth"]].sort_values(by="Barrel Growth", ascending=False)[:6].reset_index().drop(columns="index"))
    c3.write(df[["State", "Capita/ Craft Brewery"]].sort_values(by="Capita/ Craft Brewery", ascending=False)[:6].reset_index().drop(columns="index"))
    c4.write(df[["State", "Total Capita/ Breweries"]].sort_values(by="Total Capita/ Breweries", ascending=False)[:6].reset_index().drop(columns="index"))