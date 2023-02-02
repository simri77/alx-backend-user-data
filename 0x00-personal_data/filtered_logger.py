#!/usr/bin/env python3
"""
Module filtered_logger
"""
import re
from typing import List
import logging
from os import environ
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Reterive the log message obfuscated
    Parameters
    ----------
    fields: list
        a list of strings representing all fields to obfuscate
    redaction: str
        a string representing by what the field will be obfuscated
    message: str
        a string representing the log line
    separator: str
        a string representing by which character is separating
        all fields in the log line (message)
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """Reterive logger object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Reterive a connector to the database
    """
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    user = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    database = environ.get("PERSONAL_DATA_DB_NAME")
    connection = mysql.connector.connection.MySQLConnection(host=host,
                                                            database=database,
                                                            user=user,
                                                            password=password)
    return connection


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format a string that lists out the attributes
        that the output should contain

        parameters
        ----------
        record: logging.LogRecord
            LogRecord objects that have all the information related
            to the event being logged
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
