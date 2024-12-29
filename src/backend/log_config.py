import logging
android = True

def setup_logging():
    # Check if running on Android, either from platform or a flag
    if android:
        # Return a dummy logger that ignores all logs
        logger = logging.getLogger("dummy")
        logger.addHandler(logging.NullHandler())  # Null handler ignores all logs
        return logger

    # Create a custom logger for desktop
    logger = logging.getLogger(__name__)

    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

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
