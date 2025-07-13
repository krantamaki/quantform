"""@package scheduler.Task
@author Kasper Rantamäki
Generic task class to be used with the Scheduler class

An object for specifying a task that should be run and when it should be run
"""
from typing import Literal, Optional, List
from pathlib import Path
from copy import copy


class Task:
  """
  TODO
  """

  def __init__(task_name: str, 
               script_path: Path, 
               # If run frequency is intraday then runtime is not used and can be None
               runtime: Optional[str], 
               # New run frequencies can be added as needed
               run_freq: Literal["Once", "1min", "1h", "Day", "Bank Day", "Month End"],
               prerequisite_tasks: List[str],
               max_duration: int,  # Seconds
               parallelization: Literal["Worker", "Pool"],
               pool_size: Optional[int],
               *args,
               **kwargs) -> None:
    """
    TODO
    """
    pass
  

  def __call__(self, datetime: str) -> None:
    """
    TODO
    """
    pass
  

  @property
  def task_name(self) -> str:
    return copy(self.__task_name)
  

  @property
  def script_path(self) -> Path:
    return copy(self.__script_path)
  

  @property
  def runtime(self) -> Optional[str]:
    return copy(self.__runtime)
  

  @property
  def run_freq(self) -> str:
    return copy(self.__run_freq)
  

  @property
  def prerequisite_tasks(self) -> List[str]:
    return copy(self.__prerequisite_tasks)


  @property
  def max_duration(self) -> int:
    return self.__max_duration
  

  @property
  def parallelization(self) -> Literal["Worker", "Pool"]:
    return self.__parallelization
  

  @property
  def pool_size(self) -> Optional[int]:
    return self.__pool_size

