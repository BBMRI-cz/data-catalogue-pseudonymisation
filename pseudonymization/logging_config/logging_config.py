import os
import logging
import sys

class LoggingConfig:
    _logger : logging.Logger | None = None
    _run_id = None

    @classmethod
    def initialize(cls, run_id, log_dir):
        cls._run_id = run_id
        os.makedirs(log_dir, exist_ok=True)
        log_filename = os.path.join(log_dir, f"{run_id}.log")

        logger = logging.getLogger(f"run.{run_id}")
        logger.setLevel(logging.INFO)

        if not logger.handlers:  
            # file logging
            file_handler = logging.FileHandler(log_filename)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            # stdout logging
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        cls._logger = logger
        return logger

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._logger is None:
            raise RuntimeError("Logger not initialized. Call LoggingConfig.initialize(run_id) first.")
        return cls._logger
