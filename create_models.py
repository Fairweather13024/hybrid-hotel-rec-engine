from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
from sklearn.neighbors import NearestNeighbors
import joblib
import pandas as pd

# Load feature-engineered user data and feature-engineered review data
user_data = pd.read_json("user_data.json")
hotel_agg = pd.read_csv("hotel_agg_data.csv")


def content_based_model( hotel_agg, test_size=0.2, random_state=42):
    # Select relevant columns from hotel_reviews
    features = [
        'Rating_mean', 'PCA_Component_1_mean', 'PCA_Component_2_mean',
        'PCA_Component_3_mean', 'PCA_Component_4_mean', 'PCA_Component_5_mean',
        'neg_mean', 'neu_mean', 'pos_mean', 'compound_mean'
    ]

    # Normalize features
    scaler = StandardScaler()
    hotel_agg[features] = scaler.fit_transform(hotel_agg[features])
    
    # Train-test split
    X_train, X_test = train_test_split(hotel_agg[features] , test_size=test_size, random_state=random_state)

    # Train a KNN model
    model = NearestNeighbors(n_neighbors=25, metric="euclidean") #25 because sqrt 550 entries which prevents overfittng and underfitting
    model.fit(X_train)
    joblib.dump(model, "content_based_model.joblib")
    joblib.dump(scaler, "content_scaler.joblib")
    print("Content based model created and saved as content_based_model.joblib")

def create_collaborative_filtering_model(user_data, test_size=0.2, random_state=42):
    # Keep only the aspect keyword ratings columns
    aspect_keyword_ratings = ["cleanliness", "location", "service", "amenities", "budget", "value"]
    user_data = user_data[["UUID"] + aspect_keyword_ratings]

    # Train-test split
    X_train, X_test = train_test_split(user_data[aspect_keyword_ratings], test_size=test_size, random_state=random_state)

    # Train the Nearest Neighbors model
    knn_model = NearestNeighbors(metric="cosine", algorithm="brute")
    knn_model.fit(X_train)

    # Save the model
    joblib.dump(knn_model, "collaborative_filtering_model.joblib")
    print("Collaborative filtering model created and saved as collaborative_filtering_model.joblib")



# Train and save the models
content_based_model( hotel_agg)
create_collaborative_filtering_model(
    user_data
)
