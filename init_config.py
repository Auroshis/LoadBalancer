import etcd3

etcd = etcd3.client(host="etcd", port=2379)

# Set global configs
etcd.put("/config/global/request_timeout", "7")
etcd.put("/config/global/retries", "3")
etcd.put("/config/global/health_check_timeout", "3")

# Set server configs
etcd.put("/config/servers/server1", "host.docker.internal:3000")
etcd.put("/config/servers/server2", "host.docker.internal:3001")

print("Initial etcd config populated.")
