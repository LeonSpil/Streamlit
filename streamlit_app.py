import streamlit as st
import pandas as pd
import plotly.express as px

# Titel van de app
st.title("Exclusieve Schoenen Verkoop Analyse")

# Laad de CSV vanuit dezelfde directory (of GitHub indien nodig)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/LeonSpil/Streamlit/refs/heads/main/exclusieve_schoenen_verkoop_met_locatie.csv"
    df = pd.read_csv(url, parse_dates=['aankoopdatum'])
    df['jaar'] = df['aankoopdatum'].dt.year
    df['maand'] = df['aankoopdatum'].dt.month
    return df

df = load_data()

# Unieke merken voor filter
merken = df['merk'].unique()
geselecteerde_merken = st.sidebar.multiselect("Filter op Merk", merken, default=merken)

# Filter op geselecteerde merken
df_filtered = df[df['merk'].isin(geselecteerde_merken)]

# Tabs
tab1, tab2 = st.tabs(["Totaal per Land", "Totaal per Maand/Jaar"])

with tab1:
    st.subheader("Totaal Bedrag per Land")
    totaal_per_land = df_filtered.groupby('land')['totaal_bedrag'].sum().reset_index()
    fig1 = px.bar(totaal_per_land, x='land', y='totaal_bedrag', title='Totale Verkoop per Land')
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Totaal Bedrag per Maand en Jaar")
    totaal_per_maand_jaar = df_filtered.groupby(['jaar', 'maand'])['totaal_bedrag'].sum().reset_index()
    totaal_per_maand_jaar['jaar-maand'] = totaal_per_maand_jaar['jaar'].astype(str) + '-' + totaal_per_maand_jaar['maand'].astype(str).str.zfill(2)
    fig2 = px.line(totaal_per_maand_jaar, x='jaar-maand', y='totaal_bedrag', title='Totale Verkoop per Maand/Jaar')
    st.plotly_chart(fig2, use_container_width=True)
