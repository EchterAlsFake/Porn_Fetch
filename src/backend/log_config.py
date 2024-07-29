import logging


def setup_logging():
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Avoid adding handlers multiple times
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)  # Set the default logging level

        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('log.log')

        c_handler.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.DEBUG)

        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        return logger
