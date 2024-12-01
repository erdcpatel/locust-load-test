import random
from locust import HttpUser, task, between

class MarketDataUser(HttpUser):
    wait_time = between(5, 10)

    @task
    def get_tests(self):
        self.client.get("/tests")

    @task
    def get_test4(self):
        self.client.get("/tests1")

    @task
    def get_test5(self):
        self.client.get("/tests3")
