import pandas as pd
from joblib import load

# Load the trained model using joblib
model = load("content_based_model.joblib")

# Load the scaler used during training
scaler = load("content_scaler.joblib")


def content_based_input_processor(user_input):
    # Load feature-engineered ratings data
    feature_engineered_ratings = pd.read_csv("feature_engineered_ratings.csv")

    # Find the Hotel_UUID corresponding to the given hotel name
    hotel_uuid = feature_engineered_ratings[
        feature_engineered_ratings["Name"] == user_input
    ]["Hotel_UUID"].iloc[0]

    # Load hotel_agg_data containing features
    hotel_agg_data = pd.read_csv("hotel_agg_data.csv")

    # Filter the hotel aggregation data for the hotel of interest using Hotel_UUID
    input_hotel_features = hotel_agg_data[
        hotel_agg_data["Hotel_UUID"] == hotel_uuid
    ].drop(
        columns=[
            "Name",
            "Hotel_UUID",
            "PCA_Component_1_std",
            "PCA_Component_2_std",
            "PCA_Component_3_std",
            "PCA_Component_4_std",
            "PCA_Component_5_std",
            "Rating_std",
            "compound_std",
            "neg_std",
            "neu_std",
            "pos_std",
            "City",
            "Neighborhood",
        ]
    )

    # Scale the input features
    input_features_scaled = scaler.transform(input_hotel_features)

    # Perform inference using the loaded model
    distances, neighbor_indices = model.kneighbors(
        input_features_scaled, n_neighbors=10
    )

    # Get top recommendations
    top_recommendations_indices = neighbor_indices[0]  
    top_recommendations = hotel_agg_data.iloc[top_recommendations_indices]
    # print(top_recommendations.head(1))
    print(distances)
    # Prepare results as a list of dictionaries
    results = []
    for i, row in top_recommendations.iterrows():
        print(i)
        # Fetch additional information from feature_engineered_ratings using Hotel_UUID
        additional_info = feature_engineered_ratings[
            feature_engineered_ratings["Hotel_UUID"] == row["Hotel_UUID"]
        ].iloc[0]
        result_dict = {
            "Hotel_UUID": row["Hotel_UUID"],
            "hotel_name": row["Name"],
            "rating": row["Rating_mean"],
            "neighborhood": additional_info["Neighborhood"],
            "city": additional_info["City"],
        }
        results.append(result_dict)


    # Sort results based on distance
    results = sorted(results, key=lambda x: x["rating"], reverse=True)

    # Return the results
    return results


# user_input = "Hotel The Pearl"
# output = content_based_input_processor(user_input)
# print(output)
