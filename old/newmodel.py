import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from joblib import dump

# Loading dataset
hotel = pd.read_csv("hotel_reviews.csv")
hotel_new = hotel.rename(
    columns={
        "Rating_attribute": "ratin_att",
        "Rating(Out of 10)": "Rating",
        "Review_Text": "Review",
    }
)
hotel_pivot = hotel_new.pivot_table(index="Name", values="Rating")

# Saving hotel_pivot
hotel_pivot.to_excel("hotel_pivot.xlsx")

# Training the model
model = NearestNeighbors(algorithm="brute")
model.fit(hotel_pivot.values)

# Saving the trained model
dump(model, "hotel_model.joblib")
