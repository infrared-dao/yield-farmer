import logging
import os
from datetime import datetime

def setup_logging(script_name):
    log_dir = os.path.join(os.path.dirname(__file__), "../logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = f"{log_dir}/{script_name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(script_name)