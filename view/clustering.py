import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from model import model as data
import seaborn as sns
import matplotlib.pyplot as plt

data_modeling = data.load_data_modelling().copy()
data_modeling.drop(columns=data_modeling.filter(regex='Unnamed').columns, inplace=True)
data_modeling['cluster_kmeans'] = data_modeling['cluster_kmeans'].apply(lambda x: x + 1)

data_clean = data.load_data_clean()


def dataset(df):
    showData = st.multiselect('Filter: ', df.columns, default=['Beli Langsung Siang', 'Beli Langsung Malam', 'Total Beli Langsung', 'Total Beli Antar', 'Merek AQUA', 'Merek DC', 'Total Penjualan', 'Total Pengeluaran', 'Hasil Pendapatan', 'Bulan', 'Kategori Penjualan', 'Kategori Pendapatan', 'cluster_kmeans', 'cluster_hierarchical'])
    st.dataframe(df[showData], use_container_width=True)

def display_kmeans_cluster1(data_modeling):
    cluster_1_data_modeling = data_modeling[data_modeling['cluster_kmeans'] == 1]
    st.write(cluster_1_data_modeling)


def display_kmeans_cluster2(data_modeling):
    cluster_2_data_modeling = data_modeling[data_modeling['cluster_kmeans'] == 2]
    st.write(cluster_2_data_modeling)


def display_kmeans_cluster3(data_modeling):
    cluster_3_data_modeling = data_modeling[data_modeling['cluster_kmeans'] == 3]
    st.write(cluster_3_data_modeling)

def clustering_kmeans(data_modeling):
    st.subheader("Persebaran Data Setiap Cluster")
    data_model = data_modeling.drop(['cluster_hierarchical'], axis=1).copy()
    st.markdown('''
    Terlihat pada grafik scatter plot di atas terdapat 3 cluster, di mana masing-masing cluster memiliki ciri khas:
    ''')

    selected_tab = option_menu(
        "Dataframe Setiap Cluster",
        options=["Cluster 1", "Cluster 2", "Cluster 3"],
        icons=["bar-chart", "bar-chart", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "nav": {
                "border-radius": "10px",
            },
            "nav-item": {
                "margin": "0px 5px",
            },
            "icon": {
                "color": "black",
                "font-size": "18px",
            },
            "nav-link": {
                "font-size": "15px",
                "text-align": "center",
                "margin": "0px 12px",
                "--hover-color": "#53a2c2",
                "padding": "8px 12px",
                "border-radius": "10px",
            },
            "nav-link-selected": {
                "background-color": "#53a2c2",
                "color": "white",
                "border-radius": "10px",
            },
        }
    )

    if selected_tab == "Cluster 1":
        display_kmeans_cluster1(data_modeling)
    elif selected_tab == "Cluster 2":
        display_kmeans_cluster2(data_modeling)
    elif selected_tab == "Cluster 3":
        display_kmeans_cluster3(data_modeling)
    
    st.markdown('''
    - Cluster 1 (Hijau): Cluster ini menunjukkan pola pembelian di mana konsumen cenderung memiliki jumlah beli antar yang lebih tinggi dibandingkan dengan beli langsung. Ini menunjukkan preferensi kuat konsumen dalam cluster ini untuk melakukan pembelian secara antar.
    - Cluster 2 (Ungu): Meskipun pola pembelian dalam cluster ini mirip dengan cluster biru, namun jumlah pembelian baik langsung maupun antarnya cenderung lebih rendah. Ini menunjukkan bahwa konsumen dalam cluster ini mungkin lebih berhati-hati dalam melakukan pembelian atau memiliki kebutuhan yang lebih sedikit.
    - Cluster 3 (Kuning): Konsumen dalam cluster ini menunjukkan preferensi yang sangat kuat untuk melakukan pembelian secara langsung daripada secara antar. Ini menunjukkan bahwa konsumen dalam cluster ini mungkin lebih suka berbelanja secara langsung, mungkin karena alasan seperti mendapatkan produk lebih cepat atau dapat memeriksa produk secara langsung sebelum membeli.
                ''')


def main():
    st.title("Clustering")

    with st.expander(" 🔎 Lihat Dataset Modelling"):
        dataset(data_modeling)
    st.markdown("**Scatter Plot Untuk Setiap Cluster Berdasarkan Total Beli Antar dan Total Beli Langsung**")
    plt.figure(figsize=(8, 4))
    sns.scatterplot(data=data_modeling, x='Total Beli Langsung', y='Total Beli Antar', hue='cluster_kmeans', palette='viridis', s=100, alpha=0.6)
    plt.title('K-Means Clustering')
    plt.xlabel('Total Beli Langsung')
    plt.ylabel('Total Beli Antar')
    st.pyplot(plt)
    st.markdown('''
    - Cluster 1 (Hijau): Cluster ini menunjukkan pola pembelian dengan total beli langsung berkisar antara 40 hingga 80 dan total beli antar berkisar antara 150 hingga sekitar 400. Ini menunjukkan bahwa konsumen dalam cluster ini cenderung memiliki jumlah beli antar yang lebih tinggi dibandingkan dengan beli langsung.
    - Cluster 2 (Ungu): Cluster ini mencakup konsumen dengan total beli langsung berkisar antara sekitar 50 hingga sekitar 70 dan total beli antar berkisar dari sekitar 200 hingga sekitar 350. Meskipun mirip dengan cluster biru, namun jumlah pembelian baik langsung maupun antarnya cenderung lebih rendah.
    - Cluster 3 (Kuning): Konsumen dalam cluster ini memiliki total beli langsung yang sangat tinggi, berkisar dari sekitar 90 hingga lebih dari 120, sementara total beli antarnya relatif rendah, hanya berkisaran dari sekitar150 hingga kurang dari250. Ini menunjukkan bahwa konsumen dalam cluster ini cenderung melakukan pembelian secara langsung daripada secara antarnya.
            ''')

    st.markdown("---")

    clustering_kmeans(data_modeling)  

if __name__ == "__main__":
    main()
