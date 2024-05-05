import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from summa import keywords as summa_keywords
import spacy.cli

# Download and install the spaCy English model
spacy.cli.download("en_core_web_sm")

# Load spaCy model for English
nlp = spacy.load("en_core_web_sm")

# Load user data from JSON file
user_data = pd.read_json("user_data.json")


# Function to perform topic modeling using Latent Dirichlet Allocation (LDA)
def perform_topic_modeling(text):
    # Tokenize and preprocess text using spaCy
    doc = nlp(text)
    tokens = [
        token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha
    ]
    processed_text = " ".join(tokens)

    # Convert text into a bag of words representation
    vectorizer = CountVectorizer(max_features=1000)  # Adjust max_features as needed
    X = vectorizer.fit_transform([processed_text])

    # Apply LDA
    lda = LatentDirichletAllocation(
        n_components=5, random_state=42
    )  # Adjust n_components as needed
    lda.fit(X)

    # Get top topics
    topics = lda.components_.argsort(axis=1)[:, ::-1]
    top_topics = topics[0][:3]  # Get top 3 topics
    return top_topics


# Function to perform keyword extraction using TextRank
def perform_keyword_extraction(text):
    # Use Summa's TextRank for keyword extraction
    keywords = summa_keywords.keywords(text).split("\n")
    return keywords[:5]  # Get top 5 keywords


# Apply topic modeling and keyword extraction to the 'bio' field
user_data["topics"] = user_data["bio"].apply(perform_topic_modeling)
user_data["keywords"] = user_data["bio"].apply(perform_keyword_extraction)

# Create a matrix factorization for user preferences
all_items = set(item for sublist in user_data["favorites"] for item in sublist)
for item in all_items:
    user_data[item] = user_data["favorites"].apply(lambda x: 1 if item in x else 0)

# Drop the 'favorites' column as it's no longer needed
user_data.drop(columns=["favorites"], inplace=True)

# Save the feature-engineered dataset
user_data.to_csv("user_data_with_topics_keywords_and_preferences.csv", index=False)
