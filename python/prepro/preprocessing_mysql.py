import mysql.connector
import pandas as pd
from mysql.connector import Error

df = pd.read_csv('detiknews_prepro.csv')

host = 'localhost'
user = 'root'
password = ''
database = 'clustering_online_news'

# koneksi ke MySQL
try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Membuat tabel di database 
        create_table_query = """
        CREATE TABLE IF NOT EXISTS detiknews_preprocessed (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            Isi_Berita TEXT
        )
        """
        cursor.execute(create_table_query)

        # Mengunggah data dari file CSV ke tabel di database
        for index, row in df.iterrows():
            cursor.execute(
                "INSERT INTO detiknews_preprocessed (Isi_Berita) VALUES (%s)",
                (row['Isi Berita'],)
            )

        connection.commit()
        print("Data berhasil diunggah ke MySQL")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Koneksi ke MySQL ditutup")
