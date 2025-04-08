import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Schoenen Analyse", layout="wide")

st.title("Exclusieve Schoenen Verkoop Analyse")

# ---------- Data laden ----------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/LeonSpil/Streamlit/refs/heads/main/exclusieve_schoenen_verkoop_met_locatie.csv"
    df = pd.read_csv(url)

    # Aankoopdatum als datetime, met fouttolerantie
    df['aankoopdatum'] = pd.to_datetime(df['aankoopdatum'], errors='coerce')
    df['jaar'] = df['aankoopdatum'].dt.year
    df['maand'] = df['aankoopdatum'].dt.month
    return df

df = load_data()

# Controleer verplichte kolommen
vereiste_kolommen = ['merk', 'land', 'aankoopdatum', 'totaal_bedrag']
if not all(kol in df.columns for kol in vereiste_kolommen):
    st.error(f"CSV mist verplichte kolommen: {vereiste_kolommen}")
    st.stop()

merken = df['merk'].dropna().unique()

# ---------- Tabs ----------
tab1, tab2, tab3 = st.tabs(["Totaal per Land", "Totaal per Maand
