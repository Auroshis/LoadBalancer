import etcd3

class ConfigLoader:
    def __init__(self, etcd_host="localhost", port=2379):
        self.etcd = etcd3.client(host=etcd_host, port=port)

    def load_global_config(self):
        cfg = {}
        for key in ["request_timeout", "retries", "health_check_timeout"]:
            val, _ = self.etcd.get(f"/config/global/{key}")
            if val:
                cfg[key] = val.decode()
        return cfg

    def load_server_config(self):
        servers = []
        for val, meta in self.etcd.get_prefix("/config/servers/"):
            servers.append(val.decode())
        return servers
