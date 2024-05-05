# Hotel Recommendation System

This repository contains code for a hotel recommendation system. Follow the steps below to set up and run the system.

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

