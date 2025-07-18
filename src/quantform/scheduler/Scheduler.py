"""@package scheduler.Scheduler
@author Kasper Rantamäki
Generic scheduler class to be used with the Task class

An object that is constantly checking time and runs tasks as specified in the Task class
"""
from typing import List
from copy import copy
from datetime import datetime
from queue import PriorityQueue  # Used to schedule stuff

from .Task import Task


class Scheduler:
  """
  TODO
  """

  def __init__(self, tasks: List[Task], max_processes: int) -> None:
    """
    TODO
    """
    pass
  

  def __call__(self, task_name: str) -> None:
    """
    TODO
    """
    pass
  

  @property
  def tasks(self) -> List[Task]:
    return copy(self.__tasks)
  

  @property
  def max_processes(self) -> int:
    return self.__max_processes
  

  @property
  def available_processes(self) -> int:
    return self.__available_processes
  

  @property
  def running_tasks(self) -> List[str]:
    pass


  def __main_loop(self) -> None:
    """
    TODO
    """
    pass
  
