# Hotel Recommendation System

This repository contains code for a hotel recommendation system. The system utilizes content-based filtering and collaborative filtering techniques on a hotel rating dataset to recommend hotels to users. Below are the steps to set up and run the system.

## Description

This project creates a hotel recommendation engine using content-based filtering and collaborative filtering techniques on a hotel rating dataset. It involves the following steps:

- **Feature Engineering**: Preprocessing the hotel ratings dataset to extract relevant features for recommendation.
- **User Profile Creation**: Generating user profiles from the hotel data to understand user preferences.
- **Model Training**: Training the recommendation models on train and test splits of the dataset.
- **Model Serialization**: Saving the trained models as joblib files for fast inference during recommendation.

## Installation

1. Create a virtual environment using `python -m venv venv`.
2. Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS and Linux:
      ```bash
      source venv/bin/activate
      ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Setup

1. Navigate to the `utils` folder.
2. Run the following scripts in order:
    - `python feature_engineering.py`
    - `python hotel_dataset.py`
    - `python create_profiles.py`
3. Copy the following files to the parent folder (outside `utils`):
    - `user_data.json`
    - `hotel_agg_data.csv`
    - `feature_engineered_ratings.csv`

## Model Creation and Server Startup

1. Navigate to the parent folder.
2. Run the following command to create model files:
    ```bash
    python create_models.py
    ```
3. Start the server:
    ```bash
    python server.py
    ```

## Usage

After starting the server, open `index.html` in a web browser to render the HTML and use the hotel recommendation system.

