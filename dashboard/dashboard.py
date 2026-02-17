import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

sns.set_theme(style="darkgrid")
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "main_data.csv")
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    return df

day_df = load_data()

#Sidebar 
with st.sidebar:
    st.header("🚲 Bike Sharing Analytics")
    st.markdown("---")
    
    min_date = day_df["date"].min()
    max_date = day_df["date"].max()
    
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["date"] >= pd.to_datetime(start_date)) & 
                 (day_df["date"] <= pd.to_datetime(end_date))]


#Main Halaman Dashboard
st.title("🚲 Bike Sharing Data Dashboard")
st.markdown("Dashboard ini menampilkan hasil analisis penyewaan sepeda berdasarkan faktor lingkungan dan perilaku pengguna.")


col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_df['total_rentals'].sum()
    st.metric("Total Penyewaan (Keseluruhan)", value=f"{total_rentals:,}")

with col2:
    total_registered = main_df['registered'].sum()
    st.metric("Total Pengguna Terdaftar", value=f"{total_registered:,}")

with col3:
    total_casual = main_df['casual'].sum()
    st.metric("Total Pengguna Biasa", value=f"{total_casual:,}")

st.markdown("---")



tab1, tab2, tab3 = st.tabs(["Cuaca & Musim", "Pola Pengguna", "Analisis Suhu (Binning)"])

#TAB 1 Cuaca dan Musim
with tab1:
    st.subheader("Pengaruh Musim dan Cuaca Terhadap Penyewaan")
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))
    
    sns.barplot(
        x="season", y="total_rentals", data=main_df, 
        palette="Blues_d", ax=ax[0], errorbar=None,
        hue="season", legend=False
    )
    ax[0].set_title("Berdasarkan Musim", fontsize=15)
    ax[0].set_ylabel("Rata-rata Penyewaan")
    ax[0].set_xlabel("Musim")

    sns.barplot(
        x="weather_condition", y="total_rentals", data=main_df, 
        palette="Blues_d", ax=ax[1], errorbar=None,
        hue="weather_condition", legend=False
    )
    ax[1].set_title("Berdasarkan Cuaca", fontsize=15)
    ax[1].set_ylabel("Rata-rata Penyewaan")
    ax[1].set_xlabel("Kondisi Cuaca")
    
    st.pyplot(fig)

#TAB 2 Perilaku Pengguna
with tab2:
    st.subheader("Perbandingan Pengguna Casual vs Registered")
    
    
    user_behavior = main_df.groupby('workingday')[['casual', 'registered']].mean().reset_index()
    user_behavior['workingday'] = user_behavior['workingday'].map({0: 'Hari Libur / Akhir Pekan', 1: 'Hari Kerja'})
    user_behavior_melted = user_behavior.melt(id_vars='workingday', var_name='Tipe Pengguna', value_name='Rata-rata Penyewaan')

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x='workingday', y='Rata-rata Penyewaan', hue='Tipe Pengguna', 
        data=user_behavior_melted, palette=["#FF9999", "#66B2FF"], ax=ax2
    )
    ax2.set_title("Penyewaan di Hari Kerja vs Hari Libur", fontsize=15)
    ax2.set_xlabel("Tipe Hari")
    
    st.pyplot(fig2)

#TAB 3 Analisis Lanjutan (Binning)
with tab3:
    st.subheader("Analisis Lanjutan: Penyewaan Berdasarkan Kategori Suhu")
    
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.barplot(
        x="temp_category", y="total_rentals", data=main_df,
        order=['Dingin', 'Nyaman', 'Panas'],
        palette=["#A2C4C9", "#72BCD4", "#FF7F50"], errorbar=None,
        hue="temp_category", legend=False, ax=ax3
    )
    ax3.set_title("Rata-rata Penyewaan Berdasarkan Suhu Lingkungan", fontsize=15)
    ax3.set_xlabel("Kategori Suhu")
    ax3.set_ylabel("Rata-rata Penyewaan")
    
    st.pyplot(fig3)

st.caption('Dicoding Data Analysis Project - Bike Sharing Analytics')