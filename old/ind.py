from http.server import SimpleHTTPRequestHandler,HTTPServer
import json

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = json.loads(post_data)
        # userInput = parsed_data['userInput'][0]
        results="process_user_input(userInput)"
        results_string = '\n'.join(results)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(results_string.encode())

def run_server(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8000):
    print("Server is running")
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()