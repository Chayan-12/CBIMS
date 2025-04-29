from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 2)  # Simulate user wait time between tasks

    @task
    def my_task(self):
        self.client.get("/")  # Make a GET request to the root URL


    @task
    def detect_anomaly(self):
        # Define test data (you can expand this for various test cases)
        threat_level = random.randint(50, 100)
        description = "Potential malware detected" if threat_level > 60 else "Normal operation"

        # Send a POST request to the /detect endpoint
        headers = {'Content-Type': 'application/json'}
        payload = {
            "threat_level": threat_level,
            "description": description
        }
        self.client.post("/detect", data=json.dumps(payload), headers=headers)

