from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import json
from content_based_inference import content_based_input_processor
from collaborative_filtering import collaborative_filtering_inference
import pandas as pd
import numpy as np

user_data = pd.read_json("user_data.json")
hotel_data = pd.read_csv("hotel_agg_data.csv")


def replace_nan_with_empty(obj):
    if isinstance(obj, dict):
        return {k: replace_nan_with_empty(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_nan_with_empty(item) for item in obj]
    elif isinstance(obj, float) and np.isnan(obj):
        return ""  # Replace NaN with empty string
    else:
        return obj

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        parsed_data = json.loads(post_data)
        print("Parsed data: ", parsed_data)
        
        # Extract hotelName and userUUID from the parsed data
        hotelName = parsed_data.get("hotelName", "")
        userUUID = parsed_data.get("userUUID", "")
        
        print("Hotel name: ", hotelName)
        print("User UUID: ", userUUID)
        
        content_based_results= content_based_input_processor(hotelName)
        collaborative_filtering_results = collaborative_filtering_inference(userUUID, user_data, hotel_data)

        results = {
            "content_based_results": content_based_results,
            "collaborative_filtering_results": collaborative_filtering_results
        }
        results = replace_nan_with_empty(results)
        print("Results: ", results)

        # Send the results back as JSON
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(results).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

def run_server(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
