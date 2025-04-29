from sklearn.ensemble import IsolationForest
import numpy as np

# Function to detect anomalies
def detect_anomalies(threat_level, description):
    # Example of how you might process the data
    data = np.array([[threat_level]])  # Wrapping the input data in a 2D array for scikit-learn

    model = IsolationForest(contamination=0.1)  # Set contamination rate (anomaly rate)
    model.fit(data)

    score = model.decision_function(data)[0]
    anomaly = model.predict(data)[0]

    # Return result: anomaly (1 for normal, -1 for anomaly), score
    return {'anomaly': anomaly, 'score': score}
