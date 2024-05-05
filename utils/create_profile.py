import pandas as pd
import numpy as np
import json
import uuid
import random

# Load the hotel dataset
hotel_data = pd.read_csv(
    "feature_engineered_ratings.csv"
)  # Replace "hotel_data.csv" with the path to your hotel dataset

# List of phrases related to traveling
travel_phrases = [
    "Avid traveler who loves exploring new destinations and experiencing different cultures.",
    "Passionate about adventure and discovering hidden gems during travels.",
    "Enthusiastic globetrotter seeking new adventures and cultural experiences.",
    "Dedicated traveler with a thirst for exploration and a love for discovering unique destinations.",
    "Adventurous spirit always seeking new horizons and embracing the unknown.",
    "Wanderlust-driven traveler with a passion for uncovering the beauty of the world.",
    "Curious explorer eager to embark on new journeys and immerse in diverse cultures.",
    "Travel enthusiast with an insatiable desire to roam the globe and create unforgettable memories.",
    "Inquisitive traveler constantly seeking out off-the-beaten-path experiences and local delights.",
    "Global nomad on a perpetual quest for adventure, discovery, and authentic travel experiences.",
]

aspect_keywords = ["cleanliness", "location", "service", "amenities", "budget", "value"]

# Function to generate random ratings for aspect keywords
def generate_ratings():
    return {aspect: random.randint(1, 10) for aspect in aspect_keywords}

# Function to create dummy user profiles
def create_user_profiles(num_profiles):
    profiles = []
    for i in range(num_profiles):
        profile = {}
        profile["UUID"] = str(uuid.uuid4())  # Generate UUID for the profile
        profile["bio"] = random.choice(travel_phrases)
        profile.update(generate_ratings())  # Add aspect ratings to the profile
        profiles.append(profile)
    return profiles

# Function to find unique UUIDs for each hotel and create favorites list and ratings list
def create_user_data(profiles, hotel_data):
    for profile in profiles:
        num_favorites = random.randint(
            5, 10
        )  # Randomly select number of favorites between 5 and 10
        profile["favorites"] = random.sample(
            hotel_data["Hotel_UUID"].tolist(), num_favorites
        )  # Select random hotels as favorites

        num_ratings = random.randint(
            5, 10
        )  # Randomly select number of ratings between 5 and 10
        profile["ratings"] = random.sample(
            hotel_data["Hotel_UUID"].tolist(), num_ratings
        )  # Select random UUIDs from the dataset as ratings
    return profiles


# Create dummy user profiles
num_profiles = 100
user_profiles = create_user_profiles(num_profiles)

# Create user data (favorites and ratings)
user_data = create_user_data(user_profiles, hotel_data)

# Output user data as JSON
with open("user_data.json", "w") as outfile:
    json.dump(user_data, outfile, indent=4)

print("User data has been saved to 'user_data.json'.")
