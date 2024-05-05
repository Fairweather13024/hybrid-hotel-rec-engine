import pandas as pd
import numpy as np
from joblib import load

# Load the trained model using joblib
model = load("hotel_model.joblib")

# Load hotel_pivot from Excel
hotel_pivot = pd.read_excel("hotel_pivot.xlsx", index_col="Name")

def process_user_input(userInput):
    # Reshape user input
    query_data = hotel_pivot.loc[userInput].values.reshape(1, -1)

    # Find nearest neighbors
    distances, indices = model.kneighbors(query_data)

    # Prepare results as a list of strings
    results = []
    for i in range(len(indices[0])):
        index = indices[0][i]
        result_dict = {
            "rank": i + 1,
            "hotel_name": hotel_pivot.index[index],
            "rating": hotel_pivot.iloc[index, 0],
            "distance": distances[0][i],
        }
        results.append(result_dict)

    # Return the results
    return results


# Example usage
user_input = "Hotel The Pearl"
output = process_user_input(user_input)
print(output)
