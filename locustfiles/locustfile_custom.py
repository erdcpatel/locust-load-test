import random
import time
from locust import HttpUser, task, between
import gevent
from locust import events
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP, MasterRunner, LocalRunner

def checker(environment):
    while not environment.runner.state in [STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP]:
        time.sleep(1)
        if environment.runner.stats.total.fail_ratio > 0.2:
            print(f"fail ratio was {environment.runner.stats.total.fail_ratio}, quitting")
            environment.runner.quit()
            return


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    # dont run this on workers, we only care about the aggregated numbers
    if isinstance(environment.runner, MasterRunner) or isinstance(environment.runner, LocalRunner):
        gevent.spawn(checker, environment)

from locust import HttpUser, events, task


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--my-argument", type=str, env_var="LOCUST_MY_ARGUMENT", default="", help="It's working")
    # Choices will validate command line input and show a dropdown in the web UI
    parser.add_argument("--env", choices=["dev", "staging", "prod"], default="dev", help="Environment")
    # Set `include_in_web_ui` to False if you want to hide from the web UI
    parser.add_argument("--my-ui-invisible-argument", include_in_web_ui=False, default="I am invisible")
    # Set `is_secret` to True if you want the text input to be password masked in the web UI
    parser.add_argument("--my-ui-password-argument", is_secret=True, default="I am a secret")
    # Use a boolean default value if you want the input to be a checkmark
    parser.add_argument("--my-ui-boolean-argument", default=True)
    # Set `is_required` to mark a form field as required
    parser.add_argument("--my-ui-required-argument", is_required=True, default="I am required")


@events.test_start.add_listener
def _(environment, **kw):
    print(f"Custom argument supplied: {environment.parsed_options.my_argument}")


class WebsiteUser(HttpUser):
    @task
    def my_task(self):
        print(f"my_argument={self.environment.parsed_options.my_argument}")
        print(f"my_ui_invisible_argument={self.environment.parsed_options.my_ui_invisible_argument}")
        print(f"env={self.environment.parsed_options.env}")
        print(f"my_ui_boolean_argument={self.environment.parsed_options.my_ui_boolean_argument}")

from flask import request

@web_ui.app.route("/my_custom_route")
def my_custom_route():
    return "your IP is: %s" % request.remote_addr

class QuickstartCustomUser(HttpUser):
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
