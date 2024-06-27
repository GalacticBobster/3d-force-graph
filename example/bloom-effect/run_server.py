from flask import Flask, send_from_directory, abort, jsonify
from werkzeug.utils import safe_join
import webbrowser
import os
import time

# Define the port to serve on
PORT = 8000

# Path to the project directory
project_dir = '/home/ananyo/Desktop/Personal/3d-force-graph/example/bloom-effect'

# Create Flask app
app = Flask(__name__, static_url_path='', static_folder=project_dir)

# Route to serve index.html
@app.route('/')
def serve_index():
    return send_from_directory(project_dir, 'index.html')

# Route to serve files in datasets directory
@app.route('/datasets/<path:filename>')
def serve_datasets(filename):
    filepath = safe_join(project_dir, 'datasets', filename)
    try:
        return send_from_directory(os.path.dirname(filepath), os.path.basename(filepath))
    except FileNotFoundError:
        abort(404)

# Debug route to check file contents
@app.route('/debug/<path:filename>')
def debug_file(filename):
    try:
        with open(safe_join(project_dir, 'datasets', filename), 'r') as file:
            data = file.read()
        return jsonify({"content": data})
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    # Open the web browser after a short delay
    time.sleep(1)  # Wait for 1 second to ensure the server is ready
    webbrowser.open(f'http://localhost:{PORT}')

    # Run the Flask app
    app.run(port=PORT)

