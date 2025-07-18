"""@package db
@author Kasper Rantamäki
Module for database connections

The module implements a DatabaseConnection abstract base class and a SQLiteConnection class which provides useful
methods for database operators using the 'sqlite3' Python library.
"""


__all__ = ["DatabaseConnection", "SQLiteConnection"]


from .DatabaseConnection import DatabaseConnection
from .SQLiteConnection import SQLiteConnection
