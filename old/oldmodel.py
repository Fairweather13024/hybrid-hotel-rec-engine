import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

#loading dataset
hotel=pd.read_csv("hotel_reviews.csv")
hotel_new=hotel.rename(columns={'Rating_attribute':'ratin_att',
                              'Rating(Out of 10)':'Rating',
                              'Review_Text':'Review'})
hotel_pivot=hotel_new.pivot_table(index='Name',values='Rating')
model=NearestNeighbors(algorithm='brute')
model.fit(hotel_pivot.values)

#the similarity is not calculated using factors like the name of the hotel, location or features of the hotel or
# any other data about users and hotels
#It is calculated only on the basis of the rating (explicit or implicit) a user gives to a hotel

# function that will recommend hotel
def process_user_input(userInput):
    #getting the distance and indices
    query_index = hotel_pivot.index.get_loc(userInput)
    distances, indices = model.kneighbors(hotel_pivot.iloc[query_index, :].values.reshape(1, -1), n_neighbors=4)

    # Prepare results as a list of strings
    results = []
    for i in range(1, len(distances.flatten())):
        result_str = f'{i}: {hotel_pivot.index[indices.flatten()[i]]}, {hotel_pivot.Rating[indices.flatten()[i]]}'
        results.append(result_str)
    
    # Write results to a file
    # with open('nearest_neighbors.txt', 'w') as f:
    #     f.write('\n'.join(results))

    # Return the results
    return results







