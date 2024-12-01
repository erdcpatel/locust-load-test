import logging
from locust import LoadTestShape, events

# Configure logger
logger = logging.getLogger("BreakTestShape")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class BreakTestShape(LoadTestShape):
    """
    Custom load shape for a break test.
    Increases the number of users over time until failures are observed,
    then reduces the user count or stops the test.
    """

    # Configuration parameters
    initial_users = 1000    # Initial number of users
    max_users = 20000       # Maximum users to scale up to
    step_size = 1000        # Number of users to add in each step
    step_duration = 20    # Duration (in seconds) for each step
    failure_threshold = 5 # Number of failures to trigger load reduction
    failure_stop_threshold = 10  # Number of failures to trigger load reduction
    total_run_time = 6000 #Max time to run test

    def __init__(self):
        super().__init__()
        self.current_users = self.initial_users
        self.run_time = 0
        self.failure_count = 0
        self.total_requests = 0

        # Track request results via the `request` event
        @events.request.add_listener
        def on_request(request_type, name, response_time, response_length, exception, **kwargs):
            self.total_requests += 1
            if exception is not None:
                self.failure_count += 1

    def tick(self):
        self.run_time = round(self.get_run_time())

        # Log details about the current test state
        failure_rate = (self.failure_count / self.total_requests * 100) if self.total_requests > 0 else 0
        logger.info(
            f"Run Time: {self.run_time}s | "
            f"Users: {self.current_users} | "
            f"Failures: {self.failure_count} | "
            f"Total Requests: {self.total_requests} | "
            f"Failure Rate: {failure_rate:.2f}%"
        )

        # # Stop the test if we reach the max user limit or a severe failure threshold
        # if self.run_time >= self.total_run_time or failure_rate >= self.failure_stop_threshold:
        #     logger.warning("Stopping test due to reaching failure threshold or max user limit.")
        #     return None

        # Increment users in steps over time
        if self.run_time % self.step_duration == 0:
            self.current_users += self.step_size
            logger.info(f"Increasing users to {self.current_users}.")

        # Reduce load if failures exceed the threshold
        if failure_rate >= self.failure_threshold:
            self.current_users = max(self.initial_users, self.current_users - self.step_size)
            logger.warning(
                f"Failure threshold exceeded. Reducing users to {self.current_users}."
            )
            self.failure_count = 0  # Reset failure count after load reduction

        return self.current_users, self.current_users