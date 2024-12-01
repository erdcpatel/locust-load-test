import random
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(5, 10)

    @task
    def get_tests(self):
        self.client.get("/tests")

    @task
    def get_test2(self):
        self.client.get("/tests1")

    @task
    def get_test3(self):
        self.client.get("/tests2")
