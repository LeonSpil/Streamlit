import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Schoenen Analyse", layout="wide")
st.title("👟 Exclusieve Schoenen Verkoop Analyse")

# ---------- Data laden ----------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/LeonSpil/Streamlit/refs/heads/main/exclusieve_schoenen_verkoop_met_locatie.csv"
    df = pd.read_csv(url)
    df['aankoopdatum'] = pd.to_datetime(df['aankoopdatum'], errors='coerce')
    df = df.dropna(subset=['aankoopdatum', 'merk', 'land', 'totaal_bedrag'])
    df['jaar'] = df['aankoopdatum'].dt.year
    df['maand'] = df['aankoopdatum'].dt.month
    return df

# Data éénmalig laden
if "data" not in st.session_state:
    st.session_state["data"] = load_data()

df = st.session_state["data"]

merken = df['merk'].dropna().unique()

# ---------- Tabs ----------
tab1, tab2, tab3 = st.tabs(["Totaal per Land", "Totaal per Maand/Jaar", "Data Bewerken"])

# Tab 1: Totaal per Land
with tab1:
    st.subheader("🌍 Totaal Verkoop per Land")
    geselecteerde_merken = st.multiselect("Filter op Merk", merken, default=list(merken), key="merkfilter1")
    df_filtered = df[df['merk'].isin(geselecteerde_merken)]

    if df_filtered.empty:
        st.warning("Geen data beschikbaar voor de geselecteerde merken.")
    else:
        totaal_per_land = df_filtered.groupby('land')['totaal_bedrag'].sum().reset_index()
        fig1 = px.bar(totaal_per_land, x='land', y='totaal_bedrag', title='Totale Verkoop per Land')
        st.plotly_chart(fig1, use_container_width=True)

# Tab 2: Totaal per Maand en Jaar
with tab2:
    st.subheader("📅 Totaal Verkoop per Maand en Jaar")
    geselecteerde_merken2 = st.multiselect("Filter op Merk", merken, default=list(merken), key="merkfilter2")
    df_filtered2 = df[df['merk'].isin(geselecteerde_merken2)]

    if df_filtered2.empty:
        st.warning("Geen data beschikbaar voor de geselecteerde merken.")
    else:
        totaal_per_maand_jaar = df_filtered2.groupby(['jaar', 'maand'])['totaal_bedrag'].sum().reset_index()
        totaal_per_maand_jaar['jaar-maand'] = totaal_per_maand_jaar['jaar'].astype(str) + '-' + totaal_per_maand_jaar['maand'].astype(str).str.zfill(2)
        fig2 = px.line(totaal_per_maand_jaar, x='jaar-maand', y='totaal_bedrag', title='Totale Verkoop per Maand/Jaar')
        st.plotly_chart(fig2, use_container_width=True)

# Tab 3: Data Bewerken
with tab3:
    # Plaats de update-knop bovenaan
    st.subheader("🛠️ Data Bewerken")
    
    # Knop om de wijzigingen bij te werken
    if st.button("🔄 Update Data"):
        gewijzigde_df = st.session_state["gewijzigde_data"]
        gewijzigde_df['aankoopdatum'] = pd.to_datetime(gewijzigde_df['aankoopdatum'], errors='coerce')
        gewijzigde_df['jaar'] = gewijzigde_df['aankoopdatum'].dt.year
        gewijzigde_df['maand'] = gewijzigde_df['aankoopdatum'].dt.month
        st.session_state["data"] = gewijzigde_df
        st.success("Data succesvol bijgewerkt!")

    # Editable dataframe
    kolommen_edit = ['merk', 'land', 'aankoopdatum', 'totaal_bedrag']
    editable_df = df[kolommen_edit].copy()

    # Gebruik session_state om gewijzigde data vast te houden
    st.session_state["gewijzigde_data"] = st.data_editor(editable_df, num_rows="dynamic", use_container_width=True)

    # Download-knop als Excel-bestand
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        editable_df.to_excel(writer, index=False, sheet_name='SchoenenData')
    st.download_button(
        label="📥 Download als Excel",
        data=output.getvalue(),
        file_name="bewerkte_schoenen_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
