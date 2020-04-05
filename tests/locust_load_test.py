from locust import HttpLocust, TaskSet, task, between

from tests.all_tests import get_auth_header


class BookstoreLocustTasks(TaskSet):
    # @task
    # def token_test(self):
    #     self.client.post("/token", dict(username="test", password="test"))

    # @task
    # def test_get_users(self):
    #     auth_header = {'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0Iiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNTg2NDMyMzU4fQ.dK4TPVgzmuHWNHprCr-d3RtRGNRBDrw1DCXC7ySFgws"}
    #     self.client.get("/v1/users", headers=auth_header)

    # @task
    # def test_post_users(self):
    #     user = {
    #         "name": "user1",
    #         "password": "pass1",
    #         "role": "admin",
    #         "mail": "a@b.com"
    #     }
    #     auth_header = {'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0Iiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNTg2NDMyMzU4fQ.dK4TPVgzmuHWNHprCr-d3RtRGNRBDrw1DCXC7ySFgws"}
    #     self.client.post("/v1/users", json=user, headers=auth_header)

    @task
    def test_get_awesome_data(self):
        self.client.get("/awesome")


class BookstoreLoadTest(HttpLocust):
    task_set = BookstoreLocustTasks
    # wait_time = between(5, 15)
    wait_time = between(0.0000001, 0.0000005)  # ile czasu bedzie czekal pomiedzy poszczegolnymi requestami
    # host = "http://localhost:8000"
    host = "http://165.22.69.128:8000"
    # host = "http://67.207.76.123"
