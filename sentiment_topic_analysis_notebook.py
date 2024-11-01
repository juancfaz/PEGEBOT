# -*- coding: utf-8 -*-
"""sentiment_topic_analysis_notebook.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HlB0Fqq7woW2x08gv5H-JSaaW89xoI3k

1. Cargar el Archivo Preprocesado
"""

import json

# Cargar las segmentaciones
with open('/content/segmentaciones.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# sentences = data['puntos']  Selecciona las oraciones segmentadas con spaCy
senteces_points = data['puntos']
sentences_commas = data['comas']
sentences_spacy = data['spacy']

from transformers import pipeline

# Crear el pipeline de análisis de sentimientos
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Aplicar el análisis de sentimientos a cada oración
sentiments = [{"sentence": sentence, "sentiment": sentiment_analyzer(sentence)[0]} for sentence in senteces_points]

sentiments[:5]

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Convertir el texto a vectores TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(senteces_points)

# Aplicar K-means para agrupar en 5 temas (ajusta según lo que quieras)
kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
clusters = kmeans.labels_

classified_sentences = [{"sentence": sentence, "cluster": int(cluster)} for sentence, cluster in zip(senteces_points, clusters)]

classified_sentences[:5]

analysis_results = [
    {"sentence": sentiment["sentence"],
     "sentiment": sentiment["sentiment"],
     "topic_cluster": cluster["cluster"]}
    for sentiment, cluster in zip(sentiments, classified_sentences)
]

# Guardar los resultados en un archivo JSON
output_file = '/content/analysis_results.json'
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(analysis_results, json_file, ensure_ascii=False, indent=4)

print(f'Resultados del análisis exportados a {output_file}')

