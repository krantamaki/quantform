"""@package scheduler.Task
@author Kasper Rantamäki
Generic task class to be used with the Scheduler class

An object for specifying a task that should be run and when it should be run
"""
from abc import ABC, abstractmethod
from typing import Literal, Optional, List
from pathlib import Path
from copy import copy

from quantform.pylib.date import QfDate


class Task(ABC):
  """
  TODO
  """

  @abstractmethod
  def __init__(self, *args, **kwargs) -> None:
    """
    TODO
    """
    pass


  @abstractmethod
  def __call__(self, global_time: str) -> None:
    """
    TODO
    """
    pass


  # Note that the dunder variables for the below properties need to be available in the instance
  @property
  def task_name(self) -> str:
    """
    TODO
    """
    return copy(self.__task_name)


  @property
  def script_path(self) -> Path:
    """
    TODO
    """
    return copy(self.__script_path)


  @property
  def runtime(self) -> Optional[str]:
    """
    TODO
    """
    return copy(self.__runtime)


  @property
  def run_freq(self) -> str:
    """
    TODO
    """
    return copy(self.__run_freq)


  @property
  def prerequisite_tasks(self) -> List[str]:
    """
    TODO
    """
    return copy(self.__prerequisite_tasks)


  @property
  def max_duration(self) -> int:
    """
    TODO
    """
    return self.__max_duration


  @property
  def threads_needed(self) -> Optional[int]:
    """
    TODO
    """
    return self.__threads_needed


