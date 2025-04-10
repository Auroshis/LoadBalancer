import threading
import hashlib

class LoadBalancer:
    def __init__(self, servers):
        self.lock = threading.Lock()
        self.servers = servers
        self.healthy = {s: True for s in servers}
        self.index = 0  # For Round Robin

    def get_server_round_robin(self):
        with self.lock:
            healthy_servers = [s for s in self.servers if self.healthy[s]]
            if not healthy_servers:
                raise Exception("No healthy servers available")
            server = healthy_servers[self.index % len(healthy_servers)]
            self.index += 1
            return server

    def get_server_by_hash(self, client_id):
        healthy_servers = [s for s in self.servers if self.healthy[s]]
        if not healthy_servers:
            raise Exception("No healthy servers available")
        key = int(hashlib.md5(client_id.encode()).hexdigest(), 16)
        return healthy_servers[key % len(healthy_servers)]

    def update_health(self, server, is_healthy):
        with self.lock:
            self.healthy[server] = is_healthy
