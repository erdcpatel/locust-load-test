from locust import HttpUser, LoadTestShape, TaskSet, constant, task


class UserTasks(TaskSet):
    @task
    def get_root(self):
        self.client.get("/")

    @task
    def get_tests(self):
        self.client.get("/tests")


class WebsiteUserA(HttpUser):
    wait_time = constant(0.5)
    tasks = [UserTasks]


class WebsiteUserB(HttpUser):
    wait_time = constant(0.5)
    tasks = [UserTasks]


class StagesShapeWithCustomUsers(LoadTestShape):
    """
    A simply load test shape class that has different user and spawn_rate at
    different stages.

    Keyword arguments:

        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage

        stop_at_end -- Can be set to stop once all stages have run.
    """

    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 10, "user_classes": [WebsiteUserA]},
        {"duration": 100, "users": 50, "spawn_rate": 10, "user_classes": [WebsiteUserB]},
        {"duration": 180, "users": 100, "spawn_rate": 10, "user_classes": [WebsiteUserA]},
        {"duration": 220, "users": 30, "spawn_rate": 10},
        {"duration": 230, "users": 10, "spawn_rate": 10},
        {"duration": 240, "users": 1, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                # Not the smartest solution, TODO: find something better
                try:
                    tick_data = (stage["users"], stage["spawn_rate"], stage["user_classes"])
                except KeyError:
                    tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None