import threading
import time
import requests

class HealthChecker(threading.Thread):
    def __init__(self, servers, balancer, interval=10):
        super().__init__()
        self.servers = servers
        self.balancer = balancer
        self.interval = interval
        self.daemon = True # Ensures thread exits with main program

    def run(self):
        while True:
            for server in self.servers:
                try:
                    r = requests.get(f"http://{server}/health", timeout=2)
                    self.balancer.update_health(server, r.status_code == 200)
                except:
                    self.balancer.update_health(server, False)
            time.sleep(self.interval)
