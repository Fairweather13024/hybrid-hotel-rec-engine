import pandas as pd
import joblib
import numpy as np


# Load the pre-trained KNN model
knn_model = joblib.load("collaborative_filtering_model.joblib")
def collaborative_filtering_inference(user_uuid, user_data, hotel_data):
    # Find the user in the user data
    user = user_data[user_data["UUID"] == user_uuid]
    print("user", user)
    # Extract aspect keyword ratings of the user
    user_ratings = user[["cleanliness", "location", "service", "amenities", "budget", "value"]].values
    print("user_ratings", user_ratings)
    # Get the top 10 similar users
    distance, neighbor_indices = knn_model.kneighbors(user_ratings, n_neighbors=10)
    print("neighbor_indices",neighbor_indices)
    # Initialize a set to store unique hotel UUIDs
    unique_hotels = set()
    similar_user_uuids = []


    # Iterate over the indices in neighbor_indices
    for neighbor_index in neighbor_indices[0]:
        # Get the UUID of the similar user at the current index
        neighbor_uuid = user_data.iloc[neighbor_index]["UUID"]
        # Append the UUID to the list
        similar_user_uuids.append(neighbor_uuid)

    # Iterate over the similar user UUIDs
    for _uuid in similar_user_uuids:
        # Get the favorites array of the neighbor user
        neighbor_favorites = user_data[user_data["UUID"] == _uuid]["favorites"].iloc[0]

        # Add unique hotel UUIDs to the set
        unique_hotels.update(neighbor_favorites)
    
    # Filter out hotels already in user's favorites
    user_favorites = set(user.iloc[0]["favorites"])
    unique_hotels -= user_favorites
    print("unique_hotels",unique_hotels)
    # Initialize a list to store hotel objects
    recommended_hotels = []

    # Iterate over unique hotel UUIDs
    for hotel_uuid in unique_hotels:

        # Find hotel info in hotel data
        hotel_info = hotel_data[hotel_data["Hotel_UUID"] == hotel_uuid].iloc[0]

        # Create hotel object
        hotel_obj = {
            "Hotel_UUID": hotel_info["Hotel_UUID"],
            "hotel_name": hotel_info["Name"],
            "rating": hotel_info["Rating_mean"],
            "neighborhood": hotel_info["Neighborhood"],
            "city": hotel_info["City"],
        }

        # Add hotel object to recommended hotels list
        recommended_hotels.append(hotel_obj)

    # Sort recommended hotels by rating
    recommended_hotels = sorted(recommended_hotels, key=lambda x: x["rating"], reverse=True)

    return recommended_hotels


# user_uuid = "1e6d0088-13a2-4536-b4e6-4dbbe2e09c8b"
# user_data = pd.read_json("user_data.json")
# hotel_data = pd.read_csv("hotel_agg_data.csv")
# result = collaborative_filtering_inference(user_uuid, user_data, hotel_data)
# print(result)
