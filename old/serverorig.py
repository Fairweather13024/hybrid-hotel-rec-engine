from http.server import BaseHTTPRequestHandler, HTTPServer,SimpleHTTPRequestHandler
import urllib.parse 
from old.oldmodel import process_user_input

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        # Extract the length of the request body
        content_length = int(self.headers['Content-Length'])
        
        # Parse the request body and extract the user input
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)
        userInput = parsed_data['userInput'][0]

        # Call the process_user_input function with user input
        results = process_user_input(userInput)
        
        # Convert results list to a single string
        results_string = '\n'.join(results)

        # Send the response back to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Write results to the response
        response_body=results_string
        return response_body

def run_server(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()