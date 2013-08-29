"""Defines logging system specifically for lemon."""
__author__ = 'ankhmorporkian'
import logging


class LemonLogger():
    """Logging class for lemon."""
    def __init__(self, logger_name='lemon_main'):
        logging.basicConfig(level=logging.INFO)
        self.__logger = logging.getLogger(logger_name)

    def error(self, msg, *args, **kwargs):
        """
        Logs an error. Use for properly handled exceptions.
        :param msg: Error information.
        """
        self.__logger.error(msg)

    def warning(self, msg, *args, **kwargs):
        """
        Logs a warning.
        :param msg: Warning information. String.
        """
        self.__logger.warning(msg)

    def critical(self, msg, *args, **kwargs):
        """
        Log a serious error, one that may or may not be recoverable.
        :param msg: Critical error information.
        """
        self.__logger.critical(msg)

    def info(self, msg, *args, **kwargs):
        """
        Log an informational message.
        :param msg: Information to be logged.
        """
        self.__logger.info(msg)