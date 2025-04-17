import os
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Ensure compatibility with PyCharm
import matplotlib.pyplot as plt
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud

# Ensure necessary NLTK components are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Define dataset path
file_path = os.path.join("C:\\Users\\sayhe\\OneDrive\\Desktop\\DAA,PS,MAP-project\\ai_resume_sorter\\data\\CleanedResumeData.csv")

# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Dataset not found at: {file_path}")

# Load cleaned dataset
df_cleaned = pd.read_csv(file_path)

# Combine all resumes into a single text
all_words = ' '.join(df_cleaned['Resume']).lower()

# Tokenize words
tokens = word_tokenize(all_words)

# Remove stopwords and non-alphabetic tokens
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

# Count word frequency
word_freq = Counter(filtered_tokens)

# Display top 20 words
print("Top 20 most common words in resumes:")
print(word_freq.most_common(20))

# Generate a WordCloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(' '.join(filtered_tokens))

# Show the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Common Words in Resumes", fontsize=14)
plt.show()

# Save the WordCloud as an image
wordcloud.to_file("wordcloud.png")
