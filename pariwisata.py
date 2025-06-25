import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

df_gmaps = pd.read_csv("hasil_analisis_review_goa_gong.csv")
df_yt = pd.read_csv("hasil_analisis_youtube.csv")

st.set_page_config(page_title="Dashboard Analisis Wisata", layout="wide")
st.title("📊 Dashboard Analisis Review Wisatawan")
tab = st.sidebar.radio("Pilih Sumber Data", ["Google Maps Kaggle", "Review Youtube"])

if tab == "Google Maps Kaggle":
    st.header("📍 Review Google Maps (Goa Gong)")
    data = df_gmaps.copy()
else:
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
if 'cleaned_review' in data.columns:
    text_col = 'cleaned_review'
else:
    text_col = 'cleaned_text'

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(data[text_col].dropna()))
fig2, ax2 = plt.subplots()
ax2.imshow(wordcloud, interpolation='bilinear')
ax2.axis('off')
st.pyplot(fig2)
st.subheader("Tabel Review / Komentar")
st.dataframe(data[['text', 'sentiment_score', 'sentiment']])
