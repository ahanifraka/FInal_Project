import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load data
df_gmaps = pd.read_csv("hasil_analisis_review_goa_gong.csv")
df_yt = pd.read_csv("hasil_analisis_youtube_goa.csv")

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Analisis Wisata", layout="wide")
st.title("📊 Dashboard Analisis Review Wisatawan")

# Sidebar Tab
tab = st.sidebar.radio("Pilih Halaman", ["Google Maps Kaggle", "Review Youtube", "Perbandingan Sumber Review", "Kesimpulan"])

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

elif tab == "Kesimpulan":
    st.header("📝 Kesimpulan Analisis Review Goa Gong")

    # Tambahkan kolom sumber jika belum ada
    df_gmaps['sumber'] = 'Google Maps'
    df_yt['sumber'] = 'YouTube'
    combined_df = pd.concat([df_gmaps, df_yt], ignore_index=True)

    # Statistik total
    total_review = combined_df.shape[0]
    total_maps = df_gmaps.shape[0]
    total_yt = df_yt.shape[0]

    # Rata-rata skor sentimen
    avg_maps = df_gmaps['sentiment_score'].mean()
    avg_yt = df_yt['sentiment_score'].mean()

    # Persentase positif
    pos_maps = (df_gmaps[df_gmaps['sentiment'] == 'Positif'].shape[0]) / total_maps * 100
    pos_yt = (df_yt[df_yt['sentiment'] == 'Positif'].shape[0]) / total_yt * 100

    # Layout metrik ringkas
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Review", total_review)
    col2.metric("Google Maps Review", total_maps)
    col3.metric("YouTube Review", total_yt)

    col4, col5 = st.columns(2)
    col4.metric("Rata-rata Sentimen Google Maps", f"{avg_maps:.2f}")
    col5.metric("Rata-rata Sentimen YouTube", f"{avg_yt:.2f}")

    col6, col7 = st.columns(2)
    col6.metric("Persentase Positif Google Maps", f"{pos_maps:.1f}%")
    col7.metric("Persentase Positif YouTube", f"{pos_yt:.1f}%")

    # Narasi kesimpulan
    st.subheader("📌 Ringkasan Analisis")
    st.markdown(f"""
    - Google Maps memiliki total **{total_maps}** review, sedangkan YouTube memiliki **{total_yt}** komentar.
    - Rata-rata skor sentimen dari review Google Maps adalah **{avg_maps:.2f}**, sedangkan YouTube adalah **{avg_yt:.2f}**.
    - Persentase review **positif** di Google Maps lebih tinggi sebesar **{pos_maps:.1f}%**, dibandingkan dengan YouTube yang sebesar **{pos_yt:.1f}%**.
    - Secara umum, **Google Maps cenderung memiliki ulasan yang lebih positif** dibandingkan YouTube.
    
    💡 **Kesimpulan Analisis**: Meskipun kedua sumber memberikan insight penting, review dari Google Maps tampak lebih positif secara umum, sedangkan YouTube lebih bervariasi dan berisi kritik langsung dari visualisasi video.""")

# Halaman Perbandingan
else:
    st.header("📊 Perbandingan Sumber Review: Google Maps vs YouTube")

    df_gmaps['sumber'] = 'Google Maps'
    df_yt['sumber'] = 'YouTube'
    combined_df = pd.concat([df_gmaps, df_yt], ignore_index=True)

    # Grafik Jumlah Review per Sumber
    st.subheader("Jumlah Review per Sumber")
    fig, ax = plt.subplots()
    sns.countplot(data=combined_df, x='sumber', ax=ax)
    st.pyplot(fig)

    # Grafik Distribusi Sentimen per Sumber
    st.subheader("Distribusi Sentimen per Sumber")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.countplot(data=combined_df, x='sentiment', hue='sumber', order=['Positif', 'Netral', 'Negatif'], ax=ax)
    st.pyplot(fig)

    # WordCloud Perbandingan
    st.subheader("WordCloud Review Google Maps vs YouTube")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Google Maps**")
        text_col = 'cleaned_review' if 'cleaned_review' in df_gmaps.columns else 'cleaned_text'
        if text_col and not df_gmaps[text_col].dropna().empty:
            wordcloud1 = WordCloud(width=400, height=300, background_color='white').generate(' '.join(df_gmaps[text_col].dropna()))
            fig1, ax1 = plt.subplots()
            ax1.imshow(wordcloud1, interpolation='bilinear')
            ax1.axis('off')
            st.pyplot(fig1)
        else:
            st.info("Tidak ada data teks untuk WordCloud.")

    with col2:
        st.write("**YouTube**")
        text_col = 'cleaned_review' if 'cleaned_review' in df_yt.columns else 'cleaned_text'
        if text_col and not df_yt[text_col].dropna().empty:
            wordcloud2 = WordCloud(width=400, height=300, background_color='white').generate(' '.join(df_yt[text_col].dropna()))
            fig2, ax2 = plt.subplots()
            ax2.imshow(wordcloud2, interpolation='bilinear')
            ax2.axis('off')
            st.pyplot(fig2)
        else:
            st.info("Tidak ada data teks untuk WordCloud.")

    # TABEL DENGAN FILTER – HANYA DI HALAMAN INI
    st.subheader("📋 Gabungan Tabel Review (Dengan Filter)")

    with st.expander("🔎 Filter Review"):
        sumber_filter = st.multiselect(
            "Filter berdasarkan Sumber",
            options=combined_df['sumber'].unique(),
            default=combined_df['sumber'].unique()
        )

        sentiment_filter = st.multiselect(
            "Filter berdasarkan Sentimen",
            options=['Positif', 'Netral', 'Negatif'],
            default=['Positif', 'Netral', 'Negatif']
        )

        keyword = st.text_input("Cari kata kunci dalam review")

    # Terapkan filter
    filtered_df = combined_df[
        combined_df['sumber'].isin(sumber_filter) &
        combined_df['sentiment'].isin(sentiment_filter) &
        combined_df['text'].str.lower().str.contains(keyword.lower())
    ]

    st.dataframe(filtered_df[['sumber', 'text', 'sentiment_score', 'sentiment']], use_container_width=True)

