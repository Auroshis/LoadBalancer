from http.server import BaseHTTPRequestHandler, HTTPServer
from balancer import LoadBalancer
from health_checker import HealthChecker

SERVERS = ["localhost:8001", "localhost:8002", "localhost:8003"]

balancer = LoadBalancer(SERVERS)
checker = HealthChecker(SERVERS, balancer)
checker.start()

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            target = balancer.get_server_round_robin()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Forwarding to: {target}".encode())
        except Exception as e:
            self.send_response(503)
            self.end_headers()
            self.wfile.write(f"Error: {e}".encode())

def run():
    server = HTTPServer(('0.0.0.0', 8080), ProxyHandler)
    print("Load Balancer running on port 8080")
    server.serve_forever()

if __name__ == "__main__":
    run()
