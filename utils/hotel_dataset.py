import pandas as pd

# Read the hotel reviews data
hotel_reviews = pd.read_csv("feature_engineered_ratings.csv")

# Group by Hotel_UUID and calculate average and standard deviation for each column
hotel_agg = hotel_reviews.groupby("Hotel_UUID").agg(
    {
        "Name": "first",
        "Rating": ["mean", "std"],
        "PCA_Component_1": ["mean", "std"],
        "PCA_Component_2": ["mean", "std"],
        "PCA_Component_3": ["mean", "std"],
        "PCA_Component_4": ["mean", "std"],
        "PCA_Component_5": ["mean", "std"],
        "neg": ["mean", "std"],
        "neu": ["mean", "std"],
        "pos": ["mean", "std"],
        "compound": ["mean", "std"],
        "Neighborhood": "first",  # Include Neighborhood column
        "City": "first"  # Include City column
    }
)

# Flatten the multi-index columns
hotel_agg.columns = ["_".join(col).strip() for col in hotel_agg.columns.values]

# Rename the columns for clarity
hotel_agg.columns = [
    "Name", 
    "Rating_mean",
    "Rating_std",
    "PCA_Component_1_mean",
    "PCA_Component_1_std",
    "PCA_Component_2_mean",
    "PCA_Component_2_std",
    "PCA_Component_3_mean",
    "PCA_Component_3_std",
    "PCA_Component_4_mean",
    "PCA_Component_4_std",
    "PCA_Component_5_mean",
    "PCA_Component_5_std",
    "neg_mean",
    "neg_std",
    "neu_mean",
    "neu_std",
    "pos_mean",
    "pos_std",
    "compound_mean",
    "compound_std",
    "Neighborhood",
    "City"
]

print(len(hotel_agg.columns))
print(hotel_agg.columns)

# Reset index to make Hotel_UUID a regular column
hotel_agg.reset_index(inplace=True)

# Save the aggregated data to a new CSV file
hotel_agg.to_csv("hotel_agg_data.csv", index=False)

print("Aggregated hotel data saved successfully.")
