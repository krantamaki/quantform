"""
TODO
"""
from typing import Optional
from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd


class DatabaseConnection(ABC):
  """
  TODO
  """

  @abstractmethod
  def __init__(self, database: str, user: Optional[str], password: Optional[str]) -> None:
    """
    TODO
    """
    pass
  

  @abstractmethod
  def __call__(self, query: str) -> None:
    """
    TODO
    For running generic queries
    """
    pass
  

  @staticmethod
  def read_sql(sql_path: Path) -> str:
    """
    TODO
    """
    pass
  

  @abstractmethod
  def insert_sql(self, schema: str, table: str, df: pd.DataFrame) -> None:
    """
    TODO
    """
    pass
  

  @abstractmethod
  def delete_sql(self, query: str) -> None:
    """
    TODO
    """
    pass
  

  @abstractmethod
  def select_sql(self, query: str) -> pd.DataFrame:
    """
    TODO
    """
    pass
