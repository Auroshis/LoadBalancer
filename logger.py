import logging
import json
from datetime import datetime
from threading import Lock

class Logger:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance._setup()
            return cls._instance
    
    def _setup(self):
        self.logger = logging.getLogger("LoadBalancerLogger")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_request(self, method, protocol, endpoint, headers, data, trace_id):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "trace_id": trace_id,
            "method": method,
            "protocol": protocol,
            "endpoint": endpoint,
            "headers": headers,
            "data": data,
        }
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))