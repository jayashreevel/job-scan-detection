import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def train_model():
    # Sample training data (simple + lightweight for Render)
    data = {
        "text": [
            "work from home earn money fast",
            "pay registration fee to join",
            "limited vacancies apply immediately",
            "software developer full time job",
            "company website official career page",
            "interview scheduled through HR email"
        ],
        "label": [1, 1, 1, 0, 0, 0]  # 1 = Fake, 0 = Real
    }

    df = pd.DataFrame(data)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["text"])
    y = df["label"]

    model = LogisticRegression()
    model.fit(X, y)

    # Save model files
    pickle.dump(model, open("job_model.pkl", "wb"))
    pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

    print("✅ ML Model Trained Successfully")

    return model, vectorizer
