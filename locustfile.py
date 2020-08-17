import random
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(0, 0)

    @task
    def get_tests(self):
        self.client.get("/tests")
    
    @task
    def put_tests(self):
        self.client.post("/tests", {
						  "name": "load testing",
						  "description": "checking if a software can handle the expected load"
						})