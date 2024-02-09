import mysql.connector
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score

df = pd.read_csv('detiknews_prepro.csv')

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Isi Berita'])

# Evaluasi Silhouette Score untuk jumlah klaster dari 2 hingga 10
max_clusters = 10
best_score = -1
optimal_clusters = 0

for n_clusters in range(2, max_clusters + 1):
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    cluster_labels = kmeans.fit_predict(tfidf_matrix)
    silhouette_avg = silhouette_score(tfidf_matrix, cluster_labels)
    print(f"For n_clusters = {n_clusters}, the average silhouette_score is: {silhouette_avg}")

    # Memilih jumlah klaster dengan nilai silhouette score tertinggi
    if silhouette_avg > best_score:
        best_score = silhouette_avg
        optimal_clusters = n_clusters

# Menggunakan jumlah klaster optimal untuk klasterisasi
kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
cluster_labels = kmeans.fit_predict(tfidf_matrix)

# Menambahkan kolom klaster ke dalam DataFrame
df['Cluster'] = cluster_labels

# Mengunggah data yang telah diproses ke dalam MySQL
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="clustering_online_news"
    )

    if connection.is_connected():
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS detiknews_clustered (
            Id INT PRIMARY KEY,
            Kategori VARCHAR(255),
            Judul VARCHAR(255),
            Tanggal_dan_Waktu_Terbit DATETIME,
            Penulis VARCHAR(255),
            Isi_Berita TEXT,
            Cluster INT
        )
        """
        cursor.execute(create_table_query)

        # Unggah data ke dalam tabel MySQL
        for index, row in df.iterrows():
            cursor.execute(
    "INSERT IGNORE INTO detiknews_clustered (Id, Kategori, Judul, Penulis, Isi_Berita, Cluster) VALUES (%s, %s, %s, %s, %s, %s)",
    (row['Id'], row['Kategori'], row['Judul'], row['Penulis'], row['Isi Berita'], row['Cluster'])
)

        connection.commit()
        print("Data berhasil diunggah ke MySQL")

except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Koneksi ke MySQL ditutup")
