from fastapi import FastAPI
from config_loader import ConfigLoader
from logger import Logger
from request_handler import create_router
from health_checker import HealthChecker
from load_balancer import LoadBalancer

# 1. Init logger
logger = Logger()

# 2. Load config from etcd
loader = ConfigLoader(etcd_host="etcd")  # Use 'etcd' service in Docker
global_config = loader.load_global_config()
servers = loader.load_server_config()

# 3. Initialize balancer
lb = LoadBalancer(servers)
checker = HealthChecker(servers, lb)
checker.start()

# 4. Build FastAPI app
app = FastAPI()
router = create_router(lb, global_config, logger)
app.include_router(router)
