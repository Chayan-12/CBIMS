from flask import Flask, request, jsonify
from anomaly_detector import detect_anomalies  # Assuming you have a detect_anomalies function in anomaly_detector.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

# MongoDB Atlas Connection
try:
    client = MongoClient(
        "mongodb+srv://admin:admin123@cyber-cluster.ibyinjz.mongodb.net/?retryWrites=true&w=majority",
        tls=True,
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=5000
    )
    client.admin.command('ping')
    print("✅ MongoDB connected successfully")
except ConnectionFailure as e:
    print(f"❌ MongoDB connection error: {e}")

# Access the database and collection
db = client['anomalies_db']  # Database name
collection = db['anomalies']  # Collection to store anomalies

@app.route('/detect', methods=['POST'])
def detect():
    # Get the data from the POST request
    data = request.get_json()

    # Assume data has 'threat_level' and 'description'
    threat_level = data.get('threat_level')
    description = data.get('description')

    # Call the anomaly detection function
    result = detect_anomalies(threat_level, description)

    # Store the result in MongoDB
    anomaly_data = {
        'threat_level': threat_level,
        'description': description,
        'anomaly': result['anomaly'],
        'score': result['score']
    }

    # Insert the anomaly data into the collection
    collection.insert_one(anomaly_data)

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
