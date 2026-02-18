import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def train_model():
    data = {
        "text": [
            "pay registration fee",
            "earn money fast",
            "government job notification",
            "company official interview"
        ],
        "label": [1, 1, 0, 0]
    }

    df = pd.DataFrame(data)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["text"])
    y = df["label"]

    model = LogisticRegression()
    model.fit(X, y)

    pickle.dump(model, open("job_model.pkl", "wb"))
    pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

    print("✅ ML Model Trained Successfully")
    return model, vectorizer
