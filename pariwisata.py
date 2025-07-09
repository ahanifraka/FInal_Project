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
st.title("\U0001F4CA Dashboard Analisis Review Wisatawan")

# Fungsi filter data
def filter_data(data):
    with st.expander("\U0001F50E Filter Review"):
        sentiment_filter = st.multiselect(
            "Pilih jenis sentimen:",
            options=['Positif', 'Netral', 'Negatif'],
            default=['Positif', 'Netral', 'Negatif']
        )
        data = data[data['sentiment'].isin(sentiment_filter)]

        keyword = st.text_input("Cari kata kunci dalam komentar")
        if keyword:
            data = data[data['text'].str.lower().str.contains(keyword.lower())]

        min_len = int(data['text'].str.len().min())
        max_len = int(data['text'].str.len().max())
        panjang = st.slider(
            "Filter berdasarkan panjang komentar",
            min_value=min_len,
            max_value=max_len,
            value=(min_len, max_len)
        )
        data = data[data['text'].str.len().between(panjang[0], panjang[1])]

    return data

# Sidebar Tab
tab = st.sidebar.radio("Pilih Halaman", ["Google Maps Kaggle", "Review Youtube", "Perbandingan Sumber Review", "Kesimpulan"])

# Google Maps Tab
if tab == "Google Maps Kaggle":
    st.header("\U0001F4CD Review Google Maps (Goa Gong)")
    data = df_gmaps.copy()
    data = filter_data(data)

    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Review", len(data))
    col2.metric("Review Positif", data[data['sentiment'] == 'Positif'].shape[0])
    col3.metric("Review Negatif", data[data['sentiment'] == 'Negatif'].shape[0])

    st.subheader("Distribusi Sentimen")
    fig, ax = plt.subplots()
    sns.countplot(data=data, x='sentiment', order=['Positif', 'Netral', 'Negatif'], ax=ax)
    st.pyplot(fig)

    st.subheader("Tabel Review / Komentar")
    st.dataframe(data[['text', 'sentiment_score', 'sentiment']], use_container_width=True)

    st.subheader("\U0001F4DD Kesimpulan Review Google Maps")
    st.markdown("""
    Review yang berasal dari Google Maps cenderung menunjukkan **kesan positif** dari para pengunjung yang sudah mengunjungi Goa Gong secara langsung.  
    Banyak pengguna memberikan penilaian yang baik terhadap keindahan alam, kebersihan, dan pengelolaan tempat wisata.  
    Namun, terdapat juga beberapa komentar negatif terkait **aksesibilitas**, **kebisingan**, atau **biaya masuk**.  
    Secara umum, review di Google Maps merepresentasikan **pengalaman langsung wisatawan** secara nyata.
    """)

# YouTube Tab
elif tab == "Review Youtube":
    st.header("\U0001F3A5 Review YouTube (Goa Gong)")
    data = df_yt.copy()
    data = filter_data(data)

    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Review", len(data))
    col2.metric("Review Positif", data[data['sentiment'] == 'Positif'].shape[0])
    col3.metric("Review Negatif", data[data['sentiment'] == 'Negatif'].shape[0])

    st.subheader("Distribusi Sentimen")
    fig, ax = plt.subplots()
    sns.countplot(data=data, x='sentiment', order=['Positif', 'Netral', 'Negatif'], ax=ax)
    st.pyplot(fig)

    st.subheader("Tabel Review / Komentar")
    st.dataframe(data[['text', 'sentiment_score', 'sentiment']], use_container_width=True)

    st.subheader("\U0001F4DD Kesimpulan Review YouTube")
    st.markdown("""
    Komentar dari YouTube memperlihatkan **keragaman opini** masyarakat.  
    Sebagian komentar bersifat positif karena **tampilan video yang menarik** dan **konten visual yang informatif**.  
    Namun, komentar negatif juga muncul, terutama yang berkaitan dengan **kualitas produksi video**, **nada suara**, atau **pendapat subjektif** terhadap tempat wisata.  
    Hal ini menunjukkan bahwa review dari YouTube lebih mencerminkan **persepsi digital masyarakat**, bukan hanya pengalaman kunjungan.
    """)

# Kesimpulan Tab
elif tab == "Kesimpulan":
    st.header("\U0001F4DD Kesimpulan Analisis Review Goa Gong")

    df_gmaps['sumber'] = 'Google Maps'
    df_yt['sumber'] = 'YouTube'
    combined_df = pd.concat([df_gmaps, df_yt], ignore_index=True)

    total_review = combined_df.shape[0]
    total_maps = df_gmaps.shape[0]
    total_yt = df_yt.shape[0]

    avg_maps = df_gmaps['sentiment_score'].mean()
    avg_yt = df_yt['sentiment_score'].mean()

    pos_maps = (df_gmaps[df_gmaps['sentiment'] == 'Positif'].shape[0]) / total_maps * 100
    pos_yt = (df_yt[df_yt['sentiment'] == 'Positif'].shape[0]) / total_yt * 100

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

    st.subheader("\U0001F9FE Kesimpulan Gabungan Analisis")
    st.markdown("""
    Berdasarkan hasil analisis dari dua sumber data (Google Maps dan YouTube), dapat disimpulkan bahwa:

    - **Google Maps** mencerminkan **pengalaman langsung dari pengunjung** yang sudah datang ke Goa Gong. Sebagian besar ulasan bersifat positif dan lebih menekankan pada **pengalaman fisik** seperti kebersihan, keindahan, dan suasana wisata.
    - **YouTube** mencerminkan **opini masyarakat digital** yang melihat destinasi dari sisi visual dan narasi video. Opini lebih bervariasi, karena pengunjung bisa saja tidak pernah datang ke lokasi namun memberikan opini berdasarkan tayangan.

    ✨ **Kesimpulan Utama:**  
    Kombinasi review dari kedua sumber memberikan wawasan yang **lebih menyeluruh**:  
    - **Google Maps** unggul dalam mewakili **kepuasan langsung pengunjung**,  
    - **YouTube** mencerminkan **ekspektasi dan persepsi masyarakat luas** terhadap destinasi wisata Goa Gong.
    """)

# Perbandingan Tab
else:
    st.header("\U0001F4CA Perbandingan Sumber Review: Google Maps vs YouTube")

    df_gmaps['sumber'] = 'Google Maps'
    df_yt['sumber'] = 'YouTube'
    combined_df = pd.concat([df_gmaps, df_yt], ignore_index=True)

    st.subheader("Jumlah Review per Sumber")
    fig, ax = plt.subplots()
    sns.countplot(data=combined_df, x='sumber', ax=ax)
    st.pyplot(fig)

    st.subheader("Distribusi Sentimen per Sumber")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=combined_df, x='sentiment', hue='sumber', order=['Positif', 'Netral', 'Negatif'], ax=ax)
    st.pyplot(fig)

    st.subheader("\U0001F4CB Gabungan Tabel Review (Dengan Filter)")

    with st.expander("\U0001F50E Filter Review"):
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

        min_len = int(combined_df['text'].str.len().min())
        max_len = int(combined_df['text'].str.len().max())
        panjang = st.slider(
            "Filter berdasarkan panjang komentar",
            min_value=min_len,
            max_value=max_len,
            value=(min_len, max_len)
        )

    filtered_df = combined_df[
        combined_df['sumber'].isin(sumber_filter) &
        combined_df['sentiment'].isin(sentiment_filter) &
        combined_df['text'].str.lower().str.contains(keyword.lower()) &
        combined_df['text'].str.len().between(panjang[0], panjang[1])
    ]

    st.dataframe(filtered_df[['sumber', 'text', 'sentiment_score', 'sentiment']], use_container_width=True)
