from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_caching import Cache
from flask_compress import Compress
import pandas as pd

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes
Compress(app)  # Enable GZIP compression for responses

# Configure caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Load the dataset
econ_data = pd.read_csv('Economid_data.csv', parse_dates=['Date'])
tech_data = pd.read_csv('technological_data.csv')

@app.route('/api/econ_data', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # Cache results for 60 seconds
def get_econ_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 100))

    # Filter the data based on the date range
    filtered_data = econ_data
    if start_date:
        filtered_data = filtered_data[filtered_data['Date'] >= start_date]
    if end_date:
        filtered_data = filtered_data[filtered_data['Date'] <= end_date]

    # Paginate data
    start = (page - 1) * limit
    end = start + limit
    paginated_data = filtered_data.iloc[start:end]

    # Select only required columns to reduce payload size
    response_data = paginated_data[['Date', 'GDP', 'Unemployment', 'Inflation', 'Price']]

    return jsonify(response_data.to_dict(orient='records'))

@app.route('/api/tech_data', methods=['GET'])
def get_tech_data():
    return jsonify(tech_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
