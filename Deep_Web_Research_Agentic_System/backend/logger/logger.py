# logger.py

import logging
import os
from datetime import datetime

class CustomLogger:
    def __init__(self, logger_name=__name__):
        # Generate timestamped log file name
        log_file = f"{datetime.now().strftime('%m_%d_%y_%H_%M_%S')}.log"

        # Create 'logs' directory
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, log_file)

        # Configure the logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

        # Prevent adding multiple handlers if this logger is reused
        if not self.logger.handlers:
            # File handler
            file_handler = logging.FileHandler(log_path)
            formatter = logging.Formatter(
                "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            # Optional: Add console handler too
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
