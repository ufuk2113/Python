# (Model - KI-Logik)
import pandas as pd
import numpy as np
import random
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# NLTK-Download sicherstellen
nltk.download("punkt")


class ChatbotModel:
    """Verarbeitet die Trainingsdaten und trainiert das Machine Learning Modell."""

    def __init__(self, filepath):
        self.filepath = filepath
        self.label_encoder = LabelEncoder()
        self.stemmer = PorterStemmer()
        self.ignore_words = ["?", ".", "!"]
        self.words = []
        self.patterns = []
        self.responses = []
        self.labels = []
        self.model = DecisionTreeClassifier()
        self.process_data()
        self.train()

    def process_data(self):
        """Lädt die CSV-Datei und verarbeitet die Daten für das Training."""
        df = pd.read_csv(self.filepath)

        # Tags in numerische Werte umwandeln
        df["tag"] = self.label_encoder.fit_transform(df["tag"])

        self.patterns = df["patterns"].values.tolist()
        self.labels = df["tag"].values.tolist()
        self.responses = list(zip(self.labels, df["responses"].values.tolist()))

        # Vokabular aufbauen
        for sentence in df["patterns"].values.tolist():
            self.add_to_vocabulary(sentence)

        for sentence in df["responses"].values.tolist():
            self.add_to_vocabulary(sentence)

    def add_to_vocabulary(self, sentence):
        """Tokenisiert und stemmt Wörter aus einem Satz und fügt sie zum Vokabular hinzu."""
        tokens = self.tokenize(sentence)
        stemmed_words = [
            self.stem(word) for word in tokens if word not in self.ignore_words
        ]
        self.words.extend(stemmed_words)

    def tokenize(self, sentence):
        """Zerteilt einen Satz in Tokens."""
        return nltk.word_tokenize(sentence)

    def stem(self, word):
        """Reduziert Wörter auf ihre Wurzel."""
        return self.stemmer.stem(word.lower())

    def bag_of_words(self, sentence):
        """Erstellt eine Bag-of-Words-Darstellung eines Satzes."""
        sentence_tokens = self.tokenize(sentence)
        sentence_words = [self.stem(word) for word in sentence_tokens]
        bag = np.zeros(len(self.words), dtype=np.float32)
        for i, word in enumerate(self.words):
            if word in sentence_words:
                bag[i] += 1
        return bag

    def train(self):
        """Trainiert das Decision-Tree-Modell."""
        bow_patterns = [self.bag_of_words(pattern) for pattern in self.patterns]
        self.model.fit(bow_patterns, self.labels)

    def predict(self, sentence):
        """Gibt die vorhergesagte Klasse für einen Satz zurück."""
        bow_sentence = [self.bag_of_words(sentence)]
        return self.model.predict(bow_sentence)[0]
