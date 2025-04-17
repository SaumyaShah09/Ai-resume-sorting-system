import os
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the processed resume data
file_path = os.path.join("data", "processed_resume_data.csv")
df = pd.read_csv(file_path)

# TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
tfidf_matrix = tfidf_vectorizer.fit_transform(df["Cleaned_Resume"])

# Save features and labels using pickle
with open("resume_features.pkl", "wb") as f:
    pickle.dump(tfidf_matrix, f)

with open("resume_labels.pkl", "wb") as f:
    pickle.dump(df["Category"], f)

# Save the TF-IDF Vectorizer
with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(tfidf_vectorizer, f)

print("TF-IDF Feature Extraction Completed!")
