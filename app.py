import plotly.express as px
import streamlit as st
import pandas as pd

df=pd.read_csv('2010.csv',index_col=0)
T=df.PERMTH_EXM
E=df.MORTSTAT
available_indicators = ['RIDAGEYR','RIAGENDR','LBDGLUSI','Biological Age']

fig = px.line(
    df,
    x="RIDAGEYR",
    y="Biological Age",
    color="RIAGENDR",
    hover_name="Biological Age",
)

st.plotly_chart(fig, theme="streamlit", use_container_width=True)
