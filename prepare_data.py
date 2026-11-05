
import os
import zipfile
import urllib.request
import pandas as pd

# Create the data folder
os.makedirs("data", exist_ok=True)

# Download the SMS Spam Collection dataset
url = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
zip_path = "data/sms_spam_collection.zip"

print("Downloading dataset...")
urllib.request.urlretrieve(url, zip_path)

# Extract the dataset
with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall("data")

# Read and clean the messages
file_path = "data/SMSSpamCollection"
df = pd.read_csv(
    file_path,
    sep="\t",
    header=None,
    names=["label", "message"],
    encoding="utf-8"
)

df["label"] = df["label"].str.strip().str.lower()
df["message"] = df["message"].astype(str).str.strip()

df = df.dropna()
df = df[df["label"].isin(["ham", "spam"])]
df = df[df["message"] != ""]

# Save the cleaned dataset
output_path = "data/cleaned_messages.csv"
df.to_csv(output_path, index=False)

print("\nDataset prepared successfully!")
print("Dataset shape:", df.shape)
print("\nLabel counts:")
print(df["label"].value_counts())
print("\nSaved to:", output_path)
