import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Initialize Lemmatizer
lemmatizer = WordNetLemmatizer()

def clean_resume(text):
    """Cleans resume text by removing special characters, numbers, and stopwords."""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters & numbers
    words = word_tokenize(text)  # Tokenize words
    words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords.words("english")]  # Lemmatization
    return " ".join(words)

# Load dataset
file_path = "C:\\Users\\sayhe\\OneDrive\\Desktop\\DAA,PS,MAP-project\\ai_resume_sorter\\data\\CleanedResumeData.csv"
df = pd.read_csv(file_path)

# Apply cleaning function
df["Cleaned_Resume"] = df["Resume"].apply(clean_resume)

# Save cleaned data
df.to_csv("processed_resume_data.csv", index=False)
print("✅ Preprocessing completed! Saved as 'processed_resume_data.csv'.")
