import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Schoenen Analyse", layout="wide")

st.title("Exclusieve Schoenen Verkoop Analyse")

# Laad de data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/LeonSpil/Streamlit/refs/heads/main/exclusieve_schoenen_verkoop_met_locatie.csv"
    df = pd.read_csv(url, parse_dates=['aankoopdatum'])
    df['jaar'] = df['aankoopdatum'].dt.year
    df['maand'] = df['aankoopdatum'].dt.month
    return df

df_origineel = load_data()
merken = df_origineel['merk'].unique()

# Tabs
tab1, tab2, tab3 = st.tabs(["Totaal per Land", "Totaal per Maand/Jaar", "Data Bewerken"])

with tab1:
    st.subheader("Totaal Bedrag per Land")
    geselecteerde_merken = st.multiselect("Filter op Merk", merken, default=merken, key="filter_tab1")
    df_filtered = df_origineel[df_origineel['merk'].isin(geselecteerde_merken)]
    
    totaal_per_land = df_filtered.groupby('land_
