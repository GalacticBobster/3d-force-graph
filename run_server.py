import http.server
import socketserver
import webbrowser
import os
import time

# Define the port to serve on
PORT = 8000

# Change the directory to the path where your HTML file is located
os.chdir('/home/ananyo/Desktop/Personal/3d-force-graph/example/ananyo_test1')

# Set up the HTTP server
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

# Open the web browser after a short delay
time.sleep(1)  # Wait for 1 second to ensure the server is ready
webbrowser.open(f'http://localhost:{PORT}')

print(f"Serving at port {PORT}")
httpd.serve_forever()

