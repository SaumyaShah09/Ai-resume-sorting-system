import streamlit as st
import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB

# Load TF-IDF vectorizer and category labels
with open("tfidf_vectorizer.pkl", "rb") as f:
    tfidf_vectorizer = pickle.load(f)

with open("resume_features.pkl", "rb") as f:
    resume_features = pickle.load(f)

with open("resume_labels.pkl", "rb") as f:
    resume_labels = pickle.load(f)

# Train Naive Bayes classifier
nb_model = MultinomialNB()
nb_model.fit(resume_features, resume_labels)

# Function to clean and vectorize new resumes
def vectorize_resume(text):
    return tfidf_vectorizer.transform([text])

st.title("🔍 AI Resume Sorter")
st.subheader("Upload multiple resumes and find the best match for your job role")

# Admin input for job role
job_role = st.text_input("💼 Enter the job role you're hiring for:")

# Upload multiple resumes
uploaded_files = st.file_uploader("📁 Upload resumes (.txt)", type=["txt"], accept_multiple_files=True)

if job_role and uploaded_files:
    job_vector = vectorize_resume(job_role)  # Treat job role as query

    scores = []
    resume_texts = []
    resume_names = []
    bayes_predictions = []
    bayes_probabilities = []

    for uploaded_file in uploaded_files:
        text = uploaded_file.read().decode("utf-8")
        resume_vector = vectorize_resume(text)

        # Cosine similarity
        similarity = cosine_similarity(resume_vector, job_vector)[0][0]
        scores.append(similarity)

        # Naive Bayes prediction
        predicted_class = nb_model.predict(resume_vector)[0]
        predicted_proba = nb_model.predict_proba(resume_vector).max()

        bayes_predictions.append(predicted_class)
        bayes_probabilities.append(predicted_proba)

        resume_texts.append(text)
        resume_names.append(uploaded_file.name)

    # Get top match based on similarity
    sorted_indices = np.argsort(scores)[::-1]

    st.success("🎯 Top Matching Resumes")
    for idx in sorted_indices[:3]:
        st.markdown(f"**{resume_names[idx]}** - Similarity Score: {scores[idx]:.2f}")
        st.markdown(f"🔑 Predicted Category (Bayesian): `{bayes_predictions[idx]}` with Confidence: `{bayes_probabilities[idx]:.2f}`")

        with st.expander("📄 View Resume Content"):
            st.write(resume_texts[idx])
else:
    st.info("👆 Enter a job role and upload resume files to proceed.")
