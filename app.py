import pandas as pd
import plotly.express as px
import streamlit as st
from lifelines import KaplanMeierFitter

# Initialize Kaplan Meier Fitter
kmf = KaplanMeierFitter()

# Predefined datasets and measures
datasets = ['National Health and Nutrition Examination Survey','Framingham Heart Study','UK Biobank','Mass General Biobank']
measure_parameters = {
    'None': {
        'column': None,
        'group_condition': lambda df: slice(None),
        'labels': ['None']
    },
    'Gender': {
        'column': 'RIAGENDR',
        'group_condition': lambda df: df['RIAGENDR'] == 1,
        'labels': ['Male', 'Female']
    },
    'Blood glucose': {
        'column': 'LBDGLUSI',
        'group_condition': lambda df: df['LBDGLUSI'] < 5.5,
        'labels': ['Low Glucose', 'High Glucose']
    },
    'Biological Age': {
        'column': 'Biological Age',
        'group_condition': lambda df: df['Biological Age'] == 0,
        'labels': ['Biologically younger', 'Biologically older']
    },
}

# Streamlit selectbox inputs
dataset = st.selectbox('Dataset', datasets, disabled=True)
measure = st.selectbox('Category', measure_parameters.keys())

# Load DataFrame
data_frame = pd.read_csv('2010.csv', index_col=0)

def prepare_survival_dataframe(df, group_condition, label):
    """Prepares a survival function DataFrame based on a group condition and a label."""
    time_to_event = df.PERMTH_EXM
    event_occurred = df.MORTSTAT
    kmf.fit(time_to_event[group_condition], event_occurred[group_condition], label=label)
    survival_function = kmf.survival_function_
    survival_function.columns = ['Survival']
    survival_function['Category'] = label
    survival_function['Time (months)'] = survival_function.index
    return survival_function

def update_fig(df, measure_params):
    """Updates the figure based on the chosen measure parameters."""
    group_condition = measure_params['group_condition'](df)
    labels = measure_params['labels']

    if len(labels) == 1:
        survival_df = prepare_survival_dataframe(df, group_condition, labels[0])
    else:
        survival_df_group1 = prepare_survival_dataframe(df, group_condition, labels[0])
        survival_df_group2 = prepare_survival_dataframe(df, ~group_condition, labels[1])
        survival_df = pd.concat([survival_df_group1, survival_df_group2])
    return survival_df

# Update figure based on chosen measure
survival_df = update_fig(data_frame, measure_parameters[measure])

# Create and display plot
fig = px.line(
    survival_df,
    x="Time (months)",
    y="Survival",
    color='Category',
    hover_name="Survival",
)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)
