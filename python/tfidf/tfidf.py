import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv('detiknews_prepro.csv')

# Membuat TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Menerapkan TF-IDF pada teks
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Isi Berita'])

# Mengonversi matriks TF-IDF menjadi DataFrame
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

print("Tabel Hasil TF-IDF:")
print(tfidf_df)

# Menghitung nilai TF-IDF total untuk setiap kata
sum_tfidf = tfidf_df.sum()

# Mengurutkan nilai TF-IDF dari yang tertinggi
top_words = sum_tfidf.sort_values(ascending=False).head(10)

# Mencetak kata-kata teratas
print("Top 10 Kata berdasarkan TF-IDF:")
print(top_words)