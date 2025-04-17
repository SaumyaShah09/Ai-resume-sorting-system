import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# Load saved model and vectorizer
with open("resume_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

with open("tfidf_vectorizer.pkl", "rb") as f:
    tfidf_vectorizer = pickle.load(f)

# --- Clean the resume like you did before ---
def clean_resume(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\@w+|\#','', text)
    text = re.sub(r'[^A-Za-z\s]', '', text)
    text = text.lower()
    return text

# --- Example usage ---
def predict_resume_category(resume_text):
    cleaned = clean_resume(resume_text)
    vectorized = tfidf_vectorizer.transform([cleaned])
    prediction = model.predict(vectorized)
    category = le.inverse_transform(prediction)[0]
    return category

# --- Test it ---
if __name__ == "__main__":
    test_resume = """Experienced Python developer with skills in Django, Flask, REST APIs, and SQL databases."""
    result = predict_resume_category(test_resume)
    print("Predicted Category:", result)
