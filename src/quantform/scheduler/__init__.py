"""@package quantform.scheduler
@author Kasper Rantamäki
Basic scheduler for running and timing tasks

Very basic scheduler that can be used to time when e.g. a trading algorithm
is started or when a report is ran
"""


__all__ = ["Scheduler", "Task"]


from .Scheduler import Scheduler
from .Task import Task
