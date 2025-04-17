import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK resources (run once)
nltk.download("stopwords")
nltk.download("wordnet")

# Load dataset
df = pd.read_csv("data/UpdatedResumeDataSet.csv")

# Initialize tools
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    """Preprocess text: remove special characters, stopwords, and apply lemmatization."""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove numbers & special characters
    text = text.split()  # Tokenize (split into words)
    text = [word for word in text if word not in stop_words]  # Remove stopwords
    text = [lemmatizer.lemmatize(word) for word in text]  # Lemmatization
    return " ".join(text)  # Join words back

# Apply cleaning function
df["Cleaned_Resume"] = df["Resume"].apply(clean_text)

# Save cleaned data
df.to_csv("data/CleanedResumeData.csv", index=False)

print("Data cleaning complete! Saved as 'CleanedResumeData.csv'")
