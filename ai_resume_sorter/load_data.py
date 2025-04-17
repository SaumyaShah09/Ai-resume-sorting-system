import pandas as pd

# Load the dataset
df = pd.read_csv("data/UpdatedResumeDataSet.csv")

# Display basic info
print(df.info())

# Display the first few rows
print(df.head())
