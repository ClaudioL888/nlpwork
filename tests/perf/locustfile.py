from locust import HttpUser, task, between


class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def analyze_text(self):
        self.client.post(
            "/api/analyze_text",
            headers={"x-api-key": "demo-key"},
            json={"text": "I love distributed systems"},
        )

    @task(2)
    def filter_text(self):
        self.client.post(
            "/api/filter",
            headers={"x-api-key": "demo-key"},
            json={"text": "I hate everything"},
        )

    @task(1)
    def search_event(self):
        self.client.post(
            "/api/search",
            headers={"x-api-key": "demo-key"},
            json={"keyword": "earthquake"},
        )
