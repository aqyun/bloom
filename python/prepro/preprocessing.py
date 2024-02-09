import re

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Membaca data dari file CSV
df = pd.read_csv('detiknews.csv')

# Fungsi pembersihan teks
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'http\S+', '', text)
    return text

df['Isi Berita'] = df['Isi Berita'].apply(clean_text)
df['Isi Berita'] = df['Isi Berita'].apply(lambda x: x.lower())

# Tokenisasi teks
nltk.download('punkt')
def tokenize_text(text):
    tokens = word_tokenize(text)
    return tokens

df['Isi Berita'] = df['Isi Berita'].apply(tokenize_text)

# Penghapusan stop words
nltk.download('stopwords')
stop_words = set(stopwords.words('indonesian'))
def remove_stop_words(tokens):
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return filtered_tokens

df['Isi Berita'] = df['Isi Berita'].apply(remove_stop_words)

# Stemming teks
factory = StemmerFactory()
stemmer = factory.create_stemmer()
def stem_text(tokens):
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    return stemmed_tokens

df['Isi Berita'] = df['Isi Berita'].apply(stem_text)
df['Isi Berita'] = df['Isi Berita'].apply(lambda x: ' '.join(x))

print("Berita Awal:")
print(df['Isi Berita'][0])

print("\nHasil Pembersihan Teks (Clean Text):")
print(clean_text(df['Isi Berita'][0]))

print("\nHasil Case Folding Teks:")
print(df['Isi Berita'][0].lower())

print("\nHasil Tokenisasi Teks:")
print(tokenize_text(df['Isi Berita'][0]))

print("\nHasil Penghapusan Stop Words:")
print(remove_stop_words(tokenize_text(df['Isi Berita'][0])))

print("\nHasil Stemming:")
stemmed_text = stem_text(remove_stop_words(tokenize_text(df['Isi Berita'][0])))
print(stemmed_text)

df.to_csv('detiknews_prepro.csv', index=False)
