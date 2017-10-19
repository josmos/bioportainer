import logging


class CustomFormatter(logging.Formatter):
    """Custom formatter, overrides funcName with value of name_override if it exists"""
    def format(self, record):
        if hasattr(record, 'name_override'):
            record.funcName = record.name_override
        return super(CustomFormatter, self).format(record)


def setup_logger(logger_name, log_file, level=logging.INFO):
    """
    Creates a logger instance
    :param logger_name: name of logger instance
    :param log_file: log file name (created in working directory)
    :param level: Logging level
    :return: logger instance
    """
    logger = logging.getLogger(logger_name)
    file_handler = logging.FileHandler(log_file, mode='w')
    formatter = CustomFormatter("%(asctime)s %(funcName)s %(levelname)s:  "
                                " %(message)s", "%Y-%m-%d %H:%M:%S")
    stream_handler = logging.StreamHandler()
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
