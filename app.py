import plotly.express as px
import streamlit as st
import pandas as pd
from lifelines import KaplanMeierFitter
kmf = KaplanMeierFitter()

measures = ['RIDAGEYR','RIAGENDR','LBDGLUSI','Biological Age']
option = st.selectbox('Measure',measures)

df=pd.read_csv('2010.csv',index_col=0)
T=df.PERMTH_EXM
E=df.MORTSTAT
kmf.fit(T, E)  
val=kmf.survival_function_
val.columns=['Survival']
val['Time (months)']=val.index  
        
fig = px.line(
    val,
    x="Time (months)",
    y="Survival",
    #color="RIAGENDR",
    hover_name="Survival",
)

st.plotly_chart(fig, theme="streamlit", use_container_width=True)
