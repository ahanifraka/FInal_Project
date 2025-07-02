import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load data
df_gmaps = pd.read_csv("hasil_analisis_review_goa_gong.csv")
df_yt = pd.read_csv("hasil_analisis_youtube.csv")

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Analisis Wisata", layout="wide")
st.title("📊 Dashboard Analisis Review Wisatawan")

# Sidebar Tab
tab = st.sidebar.radio("Pilih Halaman", ["Google Maps Kaggle", "Review Youtube", "Perbandingan Sumber Review"])

# Halaman Google Maps
if tab == "Google Maps Kaggle":
    st.header("📍 Review Google Maps (Goa Gong)")
    data = df_gmaps.copy()
    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Review", len(data))
    col2.metric("Review Positif", data[data['sentiment'] == 'Positif'].shape[0])
    col3.metric("Review Negatif", data[data['sentiment'] == 'Negatif'].shape[0])

    st.subheader("Distribusi Sentimen")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=data, x='sentiment', order=['Positif', 'Netral', 'Negatif'], ax=ax1)
    st.pyplot(fig1)

    st.subheader("WordCloud Review")
    text_col = 'cleaned_review' if 'cleaned_review' in data.columns else 'cleaned_text'
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(data[text_col].dropna()))
    fig2, ax2 = plt.subplots()
    ax2.imshow(wordcloud, interpolation='bilinear')
    ax2.axis('off')
    st.pyplot(fig2)

    st.subheader("Tabel Review / Komentar")
    st.dataframe(data[['text', 'sentiment_score', 'sentiment']])

# Halaman YouTube
elif tab == "Review Youtube":
    st.header("🎥 Review Youtube")
    data = df_yt.copy()
    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Review", len(data))
    col2.metric("Review Positif", data[data['sentiment'] == 'Positif'].shape[0])
    col3.metric("Review Negatif", data[data['sentiment'] == 'Negatif'].shape[0])

    st.subheader("Distribusi Sentimen")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=data, x='sentiment', order=['Positif', 'Netral', 'Negatif'], ax=ax1)
    st.pyplot(fig1)

    st.subheader("WordCloud Review")
    text_col = 'cleaned_review' if 'cleaned_review' in data.columns else 'cleaned_text'
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(data[text_col].dropna()))
    fig2, ax2 = plt.subplots()
    ax2.imshow(wordcloud, interpolation='bilinear')
    ax2.axis('off')
    st.pyplot(fig2)

    st.subheader("Tabel Review / Komentar")
    st.dataframe(data[['text', 'sentiment_score', 'sentiment']])

# Halaman Perbandingan
else:
    st.header("📊 Perbandingan Sumber Review: Google Maps vs YouTube")

    df_gmaps['sumber'] = 'Google Maps'
    df_yt['sumber'] = 'YouTube'

    combined_df = pd.concat([df_gmaps, df_yt], ignore_index=True)

    # Jumlah Review per Sumber
    st.subheader("Jumlah Review per Sumber")
    fig, ax = plt.subplots()
    sns.countplot(data=combined_df, x='sumber', ax=ax)
    st.pyplot(fig)

    # Distribusi Sentimen per Sumber
    st.subheader("Distribusi Sentimen per Sumber")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.countplot(data=combined_df, x='sentiment', hue='sumber', order=['Positif', 'Netral', 'Negatif'], ax=ax)
    st.pyplot(fig)

    # WordCloud per Sumber
    st.subheader("WordCloud Review Google Maps vs YouTube")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Google Maps**")
        text_col = 'cleaned_review' if 'cleaned_review' in df_gmaps.columns else 'cleaned_text'
        wordcloud1 = WordCloud(width=400, height=300, background_color='white').generate(' '.join(df_gmaps[text_col].dropna()))
        fig1, ax1 = plt.subplots()
        ax1.imshow(wordcloud1, interpolation='bilinear')
        ax1.axis('off')
        st.pyplot(fig1)

    with col2:
        st.write("**YouTube**")
        text_col = 'cleaned_review' if 'cleaned_review' in df_yt.columns else 'cleaned_text'
        wordcloud2 = WordCloud(width=400, height=300, background_color='white').generate(' '.join(df_yt[text_col].dropna()))
        fig2, ax2 = plt.subplots()
        ax2.imshow(wordcloud2, interpolation='bilinear')
        ax2.axis('off')
        st.pyplot(fig2)

    # Gabungan Tabel Data Interaktif
st.subheader("📋 Gabungan Tabel Review (Filter & Cari)")

# Filter interaktif
with st.expander("🔎 Filter Data Review"):
    sumber_filter = st.multiselect(
        "Pilih Sumber Review",
        options=combined_df['sumber'].unique(),
        default=combined_df['sumber'].unique()
    )

    sentiment_filter = st.multiselect(
        "Pilih Sentimen",
        options=['Positif', 'Netral', 'Negatif'],
        default=['Positif', 'Netral', 'Negatif']
    )

    keyword = st.text_input("Cari Kata Kunci dalam Review", "")

# Terapkan filter
filtered_df = combined_df[
    combined_df['sumber'].isin(sumber_filter) &
    combined_df['sentiment'].isin(sentiment_filter) &
    combined_df['text'].str.lower().str.contains(keyword.lower())
]

# Tampilkan tabel
st.dataframe(filtered_df[['sumber', 'text', 'sentiment_score', 'sentiment']], use_container_width=True)
