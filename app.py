import plotly.express as px
import streamlit as st
import pandas as pd

df=pd.read_csv('2010.csv',index_col=0)
T=df.PERMTH_EXM
E=df.MORTSTAT
available_indicators = ['RIDAGEYR','RIAGENDR','LBDGLUSI','Biological Age']

df = px.data.gapminder()

fig = px.scatter(
    df.query("year==2007"),
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
)

st.plotly_chart(fig, theme="streamlit", use_container_width=True)
