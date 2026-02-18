from flask import Flask, request, render_template
import sqlite3, os, pickle

from analyzer import check_keywords, domain_age_check
from search import google_search
from ml_model import train_model

app = Flask(__name__)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("reports.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title TEXT,
    job_description TEXT,
    job_url TEXT,
    result TEXT,
    risk_score INTEGER
)
""")
conn.commit()

# ---------------- MODEL ----------------
MODEL_PATH = "job_model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

if not os.path.exists(MODEL_PATH):
    model, vectorizer = train_model()
else:
    model = pickle.load(open(MODEL_PATH, "rb"))
    vectorizer = pickle.load(open(VECTORIZER_PATH, "rb"))

def ml_prediction(text):
    vec = vectorizer.transform([text])
    return model.predict_proba(vec)[0][1]

# ---------------- HOME ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    reason = ""
    links = []

    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        url = request.form["job_url"]

        text = f"{title} {desc} {url}"

        keyword_score, _ = check_keywords(text)
        domain_risk = domain_age_check(url)
        ml_prob = ml_prediction(text)

        if ml_prob > 0.75 or keyword_score > 7:
            result = "❌ FAKE JOB"
            reason = f"High scam probability ({int(ml_prob*100)}%)"
        elif domain_risk:
            result = "⚠ HIGH RISK JOB"
            reason = "Suspicious domain detected"
        else:
            result = "✅ SAFE JOB"
            reason = "No scam indicators found"

        links = google_search(text)

        cursor.execute(
            "INSERT INTO reports (job_title, job_description, job_url, result, risk_score) VALUES (?, ?, ?, ?, ?)",
            (title, desc, url, result, keyword_score)
        )
        conn.commit()

    return render_template("index.html", result=result, reason=reason, links=links)

# ---------------- REPORTS ----------------
@app.route("/reports")
def reports():
    cursor.execute("SELECT * FROM reports ORDER BY id DESC")
    data = cursor.fetchall()
    return render_template("reports.html", reports=data)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
