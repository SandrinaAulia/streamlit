import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from model import model as data
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_option_menu import option_menu

# Load cleaned data
data_clean = data.load_data_clean()

URL = 'Data Modeling.csv'
df = pd.read_csv(URL)

url_data_clean_before_mapping = 'Dataset Penjualan Air Minum G-24 2023.csv'
dfa = pd.read_csv(url_data_clean_before_mapping)

def dataset(df):
    default_values = ['Beli Langsung Siang', 'Beli Langsung Malam', 'Total Beli Langsung', 'Total Beli Antar', 'Merek AQUA', 'Merek DC', 'Total Penjualan', 'Total Pengeluaran', 'Hasil Pendapatan', 'Bulan', 'Kategori Penjualan', 'Kategori Pendapatan', 'cluster_kmeans', 'cluster_hierarchical']
    available_options = df.columns.tolist()
    default_show_data = [val for val in default_values if val in available_options]
    show_data = st.multiselect('Filter: ', available_options, default=default_show_data)
    st.dataframe(df[show_data], use_container_width=True)

def main():
    st.header('Dashboard Analisis Segmentasi Pelanggan')
    with st.expander("🔎 LIHAT ORIGINAL DATASET "):
        st.dataframe(dfa, use_container_width=True)
    
    # Compute total sum for Total Penjualan
    total_penjualan_sum = df['Total Penjualan'].sum()

    # Display descriptive statistics for Total Penjualan
    total1, total2, total3= st.columns(3, gap='small')
    with total1:
        st.info('Sum Total Penjualan', icon="💰")
        st.metric(label="Jumlah Penjualan", value=f"{total_penjualan_sum:,.0f}")

    with total2:
        st.info('Average Total Penjualan', icon="💰")
        st.metric(label="Rata Rata Penjualan", value=f"{df['Total Penjualan'].mean():,.2f}")

    with total3:
        st.info('Rentang Total Penjualan', icon="💰")
        st.metric(label="Range (Min-Max)", value=f"{df['Total Penjualan'].max() - df['Total Penjualan'].min():,.0f}")
        style_metric_cards(background_color="#FFFFFF", border_left_color="#53a2c2", border_color="#000000", box_shadow="#F71938")
        3
    penjualan_per_bulan = df.groupby('Bulan').sum().reset_index()

    # Mengurutkan DataFrame berdasarkan kolom 'Bulan'
    bulan_order = ['Jan 2023', 'Feb 2023', 'Mar 2023', 'Apr 2023', 'May 2023', 'Jun 2023', 'Jul 2023']
    penjualan_per_bulan['Bulan'] = pd.Categorical(penjualan_per_bulan['Bulan'], categories=bulan_order, ordered=True)
    penjualan_per_bulan = penjualan_per_bulan.sort_values('Bulan')

    # Membuat line chart menggunakan Plotly
    fig = px.line(penjualan_per_bulan, x='Bulan', y='Total Penjualan')
    fig.update_layout(title={'text': "Total Penjualan per Bulan", 'x':0.4})
    fig.update_traces(mode='markers+lines', marker=dict(symbol='circle', size=8))
    fig.update_layout(xaxis_title='Bulan', yaxis_title='Total Penjualan', xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

        
    # Remove non-numeric characters and convert to numeric
    dfa['Total Penjualan'] = df['Total Penjualan'].replace('[^\d.]', '', regex=True).astype(float)
    dfa['Total Pengeluaran'] = df['Total Pengeluaran'].replace('[^\d.]', '', regex=True).astype(float)
    dfa['Hasil Pendapatan'] = df['Hasil Pendapatan'].replace('[^\d.]', '', regex=True).astype(float)

    # Compute descriptive statistics
    descriptive_stats = dfa[['Beli Langsung Siang', 'Beli Langsung Malam', 'Total Beli Langsung', 'Total Beli Antar', 
                            'Total Keseluruhan', 'Merek AQUA', 'Merek DC', 'Total Penjualan', 'Total Pengeluaran', 'Hasil Pendapatan']].describe()

    # Menampilkan statistik deskriptif
    st.write("**Statistik Deskriptif**")
    st.write(descriptive_stats)

    # Display filtered dataset
    with st.expander(" 🔎 LIHAT DATASET CLEANING "):
        dataset(data_clean)

    st.markdown(
    """
    <h4 style="text-align: left; margin-left: 10px; font-size: 20px;"> 4 PILAR VISUALIZATION""",unsafe_allow_html=True)
    feature_options = ['Comparison', 'Relation', 'Composition', 'Distribution']
    selected_feature = st.selectbox('Select Feature', feature_options)

    if selected_feature == 'Comparison':
        # Visualisasi 1
        data = df[['Beli Langsung Siang', 'Beli Langsung Malam']].sum()
        fig = px.bar(x=data.index, y=data.values, title='Perbandingan Antara Beli Langsung Siang dan Beli Langsung Malam', color_discrete_sequence=['#3b668d'])
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True, style={'border': '1px solid black'})
        st.write("""Berdasarkan bar plot/grafik di atas, terlihat bahwa konsumen cenderung melakukan pembelian langsung lebih banyak pada siang hari dibandingkan malam hari. Jumlah pembelian langsung pada siang hari adalah sekitar 6000, 
                 sedangkan pada malam hari adalah sekitar 5051. Ini menunjukkan bahwa penjualan pada siang hari lebih tinggi sekitar 949 unit dibandingkan malam hari.
                 Serta menunjukkan bahwa jam operasional siang hari mungkin lebih menguntungkan bagi bisnis dan bisa menjadi waktu yang tepat untuk memaksimalkan penjualan atau menjalankan promosi.
                 """)

        # Visualisasi 2
        data = df[['Total Beli Langsung', 'Total Beli Antar']].sum()
        fig = px.bar(x=data.index, y=data.values, title='Perbandingan Antara Total Beli Langsung dan Total Beli Antar', color_discrete_sequence=['#9fc5e8'])
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True, style={'border': '1px solid black'})
        st.write(""" Berdasarkan bar plot/grafik diatas, terlihat bahwa total pembelian antar lebih tinggi dibandingkan dengan total pembelian langsung. Total pembelian langsung sekitar 11.427, sedangkan total pembelian antar adalah sekitar 47.462. 
                 Ini menunjukkan bahwa penjualan antar lebih tinggi sekitar 36.035 unit dibandingkan dengan penjualan langsung. Dari hal ini juga dapat ditunjukkan bahwa konsumen cenderung lebih suka melakukan pembelian antar dibandingkan dengan pembelian langsung. 
                 Oleh karena itu, memastikan efisiensi dan efektivitas layanan pengantaran adalah penting untuk mempertahankan dan meningkatkan penjualan.
                 """)

        # Visualisasi 3
        data = df[['Total Penjualan', 'Total Pengeluaran']].sum() 
        fig = px.bar(x=data.index, y=data.values, title='Perbandingan Antara Total Penjualan dan Total Pengeluaran',color_discrete_sequence=['#d2d2d2'])
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True, style={'border': '1px solid black'})
        st.write("""Berdasarkan bar plot/grafik diatas, terlihat bahwa total penjualan lebih tinggi dibandingkan dengan total pengeluaran. 
                 Total Penjualan adalah sekitar Rp. 351.266.000, sedangkan total pengeluaran adalah sekitar Rp. 77.101.500. Ini menunjukkan bahwa penjualan lebih tinggi sekitar Rp. 274.164.500 dibandingkan dengan pengeluaran.
                 Ini adalah indikasi yang baik bahwa bisnis berjalan dengan baik dan menguntungkan. Namun, perlu diperhatikan bahwa pengelolaan pengeluaran yang efisien tetap penting untuk memastikan keberlanjutan bisnis.
                 """)

    elif selected_feature == 'Relation':
        st.markdown("**Korelasi antara Fitur Numerik menggunakan Heatmap**", unsafe_allow_html=True)
        sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cbar=True, cmap="Blues")
        plt.gcf().set_size_inches(15, 10)
        st.pyplot(plt)
        st.write("""Berdasarkan hasil visualisasi korelasi Heatmap di atas, terlihat bahwa setiap variabel memiliki nilai yang menggambarkan hubungannya dengan variabel lainnya. 
                 Sebagai contoh, variabel “Beli Langsung Siang” menunjukkan korelasi yang signifikan dengan “Beli Langsung Malam”. Hal ini menunjukkan bahwa konsumen yang melakukan pembelian langsung pada siang hari cenderung juga melakukan pembelian langsung pada malam hari. 
                 Selain itu, “Merek AQUA” memiliki korelasi positif yang moderat dengan total penjualan, menunjukkan bahwa merek ini berkontribusi signifikan terhadap penjualan keseluruhan. 
                """)

    elif selected_feature == 'Composition':
        # Visualisasi untuk komposisi
        data = df[['Merek AQUA', 'Merek DC']].sum()
        fig = px.pie(names=data.index, values=data.values, title='Perbandingan Antara Total Merek AQUA dan DC')
        fig.update_traces(marker=dict(colors=['#6B5B95', '#FF6F61'], line=dict(color='#FFFFFF', width=2)))
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True, style={'border': '1px solid black'})
        st.write(""" Berdasarkan Pie chart diatas, terlihat bahwa merek AQUA memiliki porsi yang sedikit lebih besar (50.6%) dibandingkan dengan merek DC (49.4%). 
                 Ini menunjukkan bahwa kedua produk memiliki penerimaan yang hampir sama di pasar, namun merek AQUA sedikit lebih unggul.
                 Mengingat persaingan ketat antara kedua merek ini, strategi pemasaran harus difokuskan pada peningkatan brand dan loyalitas pelanggan. 
                 Misalnya, bisnis dapat menjalankan promosi atau diskon khusus untuk merek yang kurang unggul untuk meningkatkan penjualannya.
                 """)

    elif selected_feature == 'Distribution':
        st.markdown(" **Distribusi Total Penjualan, Total Pengeluaran, Total Beli Langsung, dan Total Beli Antar**", unsafe_allow_html=True)
        plt.figure(figsize=(10, 8))

        # Boxplot untuk Total Penjualan
        plt.subplot(2, 2, 1)
        sns.boxplot(y=df['Total Penjualan'])
        plt.title('Distribusi Total Penjualan')
        plt.ylabel('Total Penjualan')

        # Boxplot untuk Total Pengeluaran
        plt.subplot(2, 2, 2)
        sns.boxplot(y=df['Total Pengeluaran'])
        plt.title('Distribusi Total Pengeluaran')
        plt.ylabel('Total Pengeluaran')

        # Boxplot untuk Total Beli Langsung
        plt.subplot(2, 2, 3)
        sns.boxplot(y=df['Total Beli Langsung'])
        plt.title('Distribusi Total Beli Langsung')
        plt.ylabel('Total Beli Langsung')

        # Boxplot untuk Total Beli Antar
        plt.subplot(2, 2, 4)
        sns.boxplot(y=df['Total Beli Antar'])
        plt.title('Distribusi Total Beli Antar')
        plt.ylabel('Total Beli Antar')

        plt.tight_layout()
        st.pyplot(plt)

        st.markdown('''
        Berdasarkan visualisasi box plot diatas, terlihat bahwa setiap variabel memiliki distribusi yang berbeda-beda. 
        - Sebagai contoh variabel “Total Penjualan” menunjukkan distribusi yang stabil dan tidak memiliki variasi yang signifikan, menunjukkan bahwa penjualan cenderung konsisten. Outliers dalam total penjualan bisa disebabkan oleh penjualan yang sangat tinggi pada periode tertentu, misalnya saat ada promosi atau event khusus. Selain itu, bisa juga disebabkan oleh pembelian dalam jumlah besar oleh beberapa pelanggan. 
        - Sementara itu, “Total Pengeluaran” memiliki beberapa outlier, namun secara umum distribusinya juga stabil. Sedangkan untuk Outliers dalam total pengeluaran bisa disebabkan oleh pengeluaran yang tidak biasa atau biaya tak terduga lainnya. 
        - Distribusi Total Beli Langsung: Distribusi ini menunjukkan bahwa kebanyakan pelanggan membeli dalam kisaran yang relatif seragam. Ini menunjukkan bahwa metode penjualan langsung cukup efektif dan diterima oleh sebagian besar pelanggan. 
        - Distribusi Total Beli Antar: Distribusi ini menunjukkan konsistensi dalam layanan pembelian antar, menunjukkan bahwa layanan ini cukup efektif dan diterima oleh pelanggan.
                 ''')

if __name__ == "__main__":
    main()