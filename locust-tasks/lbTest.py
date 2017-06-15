from locust import HttpLocust, TaskSet, task
import os

class LBTaskSet(TaskSet):

    min_wait = 2000
    max_wait = 2000

    def on_start(self):
        self.client.verify = False
        # self.client.headers[] = ""

    # We are specifying full urls below to test 3 different endpoints at once.
    # This effectively ignores locust's "--host" parameter and the TARGET_HOST
    # env var in the k8s definitions
    @task(1)
    def get_No_SSL(self):
        self.client.verify = False
        response = self.client.post(os.environ['NOSSLURL'], {"ssl":"nosslno"})
        print "Response status code:", response.status_code
        print "Response content:", response.content

    @task(1)
    def get_Sidecar(self):
        self.client.verify = False
        response = self.client.post(os.environ['SIDECARURL'], {"ssl":"sidecar"})
        print "Response status code:", response.status_code
        print "Response content:", response.content

    @task(1)
    def get_Https_LB(self):
        self.client.verify = False
        response = self.client.post(os.environ['HTTPSLBURL'], {"ssl":"httpslb"})
        print "Response status code:", response.status_code
        print "Response content:", response.content

class MetricsLocust(HttpLocust):
    task_set = LBTaskSet
