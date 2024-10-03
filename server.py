from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

@app.route('/run-python-script', methods=['POST'])
def run_python_script():
    data = request.json
    location = data.get('location')
    if not location:
        return jsonify({'error': 'Location is required'}), 400

    # Run the Python script with the location argument
    process = subprocess.Popen(['python', 'gogetjobs.py', location], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return jsonify({'error': stderr.decode()}), 500

    # Read the jobs.json file
    try:
        with open('jobs.json', 'r') as json_file:
            jobs = json.load(json_file)
    except FileNotFoundError:
        return jsonify({'error': 'jobs.json not found'}), 500

    return jsonify(jobs)

if __name__ == '__main__':
    app.run(debug=True)
