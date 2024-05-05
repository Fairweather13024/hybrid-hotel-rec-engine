import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import uuid
import itertools
from sklearn.decomposition import PCA

# Download NLTK resources
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("vader_lexicon")

# Load the data
data = pd.read_csv(
    "hotel_reviews.csv"
)

# Text preprocessing
stop_words = set(stopwords.words("english"))


def preprocess_text(text):
    if pd.isna(text):  # Check for missing values
        return ""
    # Tokenize the text
    tokens = word_tokenize(str(text).lower())  # Convert to string and lowercase
    # Remove stopwords and punctuation
    filtered_tokens = [
        token for token in tokens if token.isalnum() and token not in stop_words
    ]
    return " ".join(filtered_tokens)


# Preprocess the review text
data["Merged_Review"] = data["Review_Text"] + " " + data["Rating_attribute"]
data["Cleaned_Merged_Review"] = data["Merged_Review"].apply(preprocess_text)

# Separate 'Area' column into 'Neighborhood' and 'City'
data[["Neighborhood", "City"]] = data["Area"].str.split(",", n=1, expand=True)

# Process 'Review_Date' to be sortable
data["Sortable_Review_Date"] = pd.to_datetime(data["Review_Date"], format="%b-%y")

# Define aspect_keywords with synonyms
aspect_keywords = {
    "cleanliness": ["clean", "tidy", "hygienic", "spotless"],
    "location": ["location", "area", "neighborhood", "proximity"],
    "service": ["service", "staff", "reception", "hospitality"],
    "amenities": ["amenities", "facility", "services", "features"],
    "budget": ["budget", "affordable", "cheap", "economical"],
    "value": [
        "return on investment",
        "high-quality",
        "prestigious",
        "lucrative",
        "elite",
        "premium",
        "exclusive",
        "sophisticated",
        "exceptional",
    ],
}

# Generate a flat list of all synonyms
all_keywords = list(itertools.chain.from_iterable(aspect_keywords.values()))


# Function to extract aspect features
def extract_aspect_features(text):
    """
    Goes through the text and counts the number of keywords and their synonyms for each aspect.
    """
    features = {}
    for aspect, keywords in aspect_keywords.items():
        count = sum(text.lower().count(keyword) for keyword in keywords)
        features[f"{aspect}_count"] = count

        # Count synonyms
        for synonym in all_keywords:
            count_synonym = text.lower().count(synonym)
            features[f"{aspect}_{synonym}_count"] = count_synonym

    return features


# Apply aspect feature extraction to the cleaned merged review text
aspect_features = data["Cleaned_Merged_Review"].apply(extract_aspect_features)
aspect_features_df = pd.DataFrame(aspect_features.tolist())

# Apply PCA
pca = PCA(n_components=5)  # Choose the number of components to retain
aspect_features_pca = pca.fit_transform(aspect_features_df)

# Create DataFrame for PCA-transformed aspect features
aspect_features_pca_df = pd.DataFrame(
    aspect_features_pca,
    columns=[f"PCA_Component_{i+1}" for i in range(aspect_features_pca.shape[1])],
)

# Concatenate PCA-transformed aspect features with original data
data = pd.concat([data, aspect_features_pca_df], axis=1)

# Contextual analysis (Sentiment Analysis)
sid = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    sentiment = sid.polarity_scores(text)
    return sentiment


sentiment_scores = data["Cleaned_Merged_Review"].apply(analyze_sentiment)
sentiment_scores_df = pd.DataFrame(sentiment_scores.tolist())
data = pd.concat([data, sentiment_scores_df], axis=1)

# Rename 'Rating(Out of 10)' column to 'Rating'
data.rename(columns={"Rating(Out of 10)": "Rating"}, inplace=True)

# Create a dictionary to map unique hotel names to UUIDs
uuid_mapping = {name: uuid.uuid4() for name in data["Name"].unique()}

# Create a new column 'UUID' and map UUIDs based on hotel names
data["Hotel_UUID"] = data["Name"].map(uuid_mapping)
data['UUID'] = [uuid.uuid4() for _ in range(len(data))]

# Drop unnecessary columns and clean Merged_Review column
data.drop(
    columns=[
        "Index",
        "Area",
        "Review_Date",
        "Rating_attribute",
        "Review_Text",
        "Merged_Review",
        "Cleaned_Merged_Review",
    ],
    inplace=True,
)

# Save the updated dataframe to a new CSV file
data.to_csv("feature_engineered_ratings.csv", index=False)
