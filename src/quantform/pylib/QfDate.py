"""@package quantform.pylib.QfDate
@author Kasper Rantamäki
Module for QuantForm date class
"""
from __future__ import annotations
from typing import Literal, Callable
from math import ceil
import QuantLib as ql


__all__ = ["QfDate", "comparable"]


# Map from the name of the calendar to the ql.Calendar object
_calendar_map = {
  "Eurex":     ql.Germany(ql.Germany.Eurex),
  "Frankfurt": ql.Germany(ql.Germany.FrankfurtStockExchange),
  "Xetra":     ql.Germany(ql.Germany.Xetra),
  "London":    ql.UnitedKingdom(ql.UnitedKingdom.Exchange),
  "NYSE":      ql.UnitedStates(ql.UnitedStates.NYSE)
}


# Map from the convention name to the function for calculating the time delta
_convention_map = {
  "30/360": lambda end, start: (360 * (end.year - start.year) + 30 * (end.month - start.month) + (end.day - start.day)) / 360,
  "ACT/365": lambda end, start: start.days_until(end) / 365,
  "ACT/360": lambda end, start: start.days_until(end) / 360,
  "Business/252": lambda end, start: start.prod_days_until(end) / 252
}


# Map from the convention name to the number of days in the year
_day_count_map = {
  "30/360": 360,
  "ACT/365": 365,
  "ACT/360": 360,
  "Business/252": 252
}


def comparable(func: Callable[[QfDate, QfDate], any]) -> Callable:
  """Decorator that asserts that two QfDate instances are comparable i.e. share the calendar and day count convention
  
  @param func  The function to be decorated
  @return      The decorated function
  """
  
  def wrapper(this: QfDate, that: QfDate) -> None:
    assert this.convention == that.convention, f"The conventions must match! ({this.convention} != {that.convention})"
    assert this.calendar  == that.calendar, f"The calendars must match! ({this.calendar} != {that.calendar})"
    
    return func(this, that)
  
  return wrapper
     


class QfDate:
  """QuantForm dateclass. Works as a wrapper for the QuantLib date object"""

  def __init__(self, year: int, month: int, day: int, calendar: Literal["Eurex", "Frankfurt", "Xetra", "London", "NYSE"] = "Frankfurt", 
               convention: Literal["30/360", "ACT/365", "ACT/360", "Business/252"] = "Business/252") -> None:
    """
    TODO
    """
    
    assert calendar in list(_calendar_map.keys()), f"Invalid calendar given! ({calendar} not in {list(_calendar_map.keys())})"
    assert convention in list(_convention_map.keys()), f"Invalid day count convention given! ({convention} not in {list(_convention_map.keys())})"
    
    self.__year            = year
    self.__month           = month
    self.__day             = day
    self.__calendar_name   = calendar
    self.__calendar        = _calendar_map[calendar]
    self.__convention_name = convention
    self.__convention      = _convention_map[convention]
    self.__ql_date         = ql.Date(day, month, year)
    self.__serial_number   = self.__ql_date.serialNumber()
    
    
  def __str__(self) -> str:
    return f"{self.__year}-{self.__month:02}-{self.__day:02}"
  
  
  def __repr__(self) -> str:
    return f"Date: {self}\nConvention: {self.__convention_name}\nCalendar: {self.__calendar_name}"


  def __hash__(self) -> str:
    return hash(repr(self))


  # Adding and subtracting return a new date object where the day has been changed by the given amount (under a given day count convention)
  def __add__(self, num: int) -> QfDate:
    """
    TODO
    """
    
    # The given parameter num is assumed to hold for the prevailing convention. Thus, for example under Business/252 convention if num
    # is 252 the calculated date should be a full year (365 days) in the future under normal day count convention.
    normalised_num = ceil(num * (365. / _day_count_map[self.__convention_name]))
    new_ql_date = ql.Date(self.__serial_number + normalised_num)
    
    return QfDate(new_ql_date.year(), new_ql_date.month(), new_ql_date.dayOfMonth(), calendar=self.__calendar_name, convention=self.__convention_name)
  
  
  def __sub__(self, num: int) -> QfDate:
    """
    TODO
    """
    return self + (-num)
  
  
  # Multiplication and division return a new date where the day has been changed by the amount 'num' * 'n_days_in_year' (under the given day count convention)
  # Multiplication goes forward in time and division backwards
  def __mul__(self, num: float) -> QfDate:
    """
    TODO
    """
    return self + num * _day_count_map[self.__convention_name]
  
  
  def __div__(self, num: float) -> QfDate:
    """
    TODO
    """
    return self - num * _day_count_map[self.__convention_name]
  
  
  @comparable
  def __eq__(self, other: QfDate) -> bool:
    return (self.year == other.year) and (self.month == other.month) and (self.day == other.day)
  
  
  @comparable
  def __gt__(self, other: QfDate) -> bool:
    return ((self.year == other.year) and (self.month == other.month) and (self.day > other.day)) or \
           ((self.year == other.year) and (self.month > other.month)) or \
           (self.year > other.year)
  
  
  @comparable
  def __lt__(self, other: QfDate) -> bool:
    return not (self >= other)
  
  
  @comparable
  def __ge__(self, other: QfDate) -> bool:
    return (self > other) or (self == other)
  
  
  @comparable
  def __le__(self, other: QfDate) -> bool:
    return (self < other) or (self == other)
  
  
  @property
  def year(self) -> int:
    return self.__year
  
  
  @property
  def month(self) -> int:
    return self.__month
  
  
  @property
  def day(self) -> int:
    return self.__day
  
  
  @property
  def calendar(self) -> str:
    return self.__calendar_name
  
  
  @property
  def convention(self) -> str:
    return self.__convention_name
  
  
  def date_shift(self, num: int) -> QfDate:
    """
    TODO
    """
    new_ql_date = ql.Date(self.__serial_number + num)
    return QfDate(new_ql_date.year(), new_ql_date.month(), new_ql_date.dayOfMonth(), calendar=self.__calendar_name, convention=self.__convention_name)
  
  
  @comparable
  def timedelta(self, other_date: QfDate) -> float:
    """
    TODO
    """
    
    if self > other_date:
      return -self.__convention(self, other_date)
    
    return self.__convention(other_date, self)
  
  
  @comparable
  def days_until(self, other_date: QfDate) -> int:
    """
    TODO
    """
    assert self <= other_date, f"The given date cannot be less than the instance date! ({self} < {other_date})"
    return other_date.__serial_number - self.__serial_number
  
  
  @comparable
  def days_since(self, other_date: QfDate) -> int:
    """
    TODO
    """
    assert self >= other_date, f"The given date cannot be greater than the instance date! ({self} < {other_date})"
    return other_date.days_until(self)
  
  
  @comparable
  def prod_days_until(self, other_date: QfDate) -> int:
    """
    inclusive from start but not end
    """
    assert self <= other_date, f"The given date cannot be less than the instance date! ({self} < {other_date})"
    
    prod_day_count = 0
    
    if self.is_prod_date():
      prod_day_count += 1
      
    date = self.next_prod_date()
    
    while date < other_date:
      prod_day_count += 1
      date = date.next_prod_date()
      
    return prod_day_count
  

  @comparable
  def prod_days_since(self, other_date: QfDate) -> int:
    """
    TODO
    """
    assert self >= other_date, f"The given date cannot be greater than the instance date! ({self} < {other_date})"
    return other_date.prod_days_until(self)
    

  def is_prod_date(self) -> bool:
    """
    TODO
    """
    return self.__calendar.isBusinessDay(self.__ql_date)
  
  
  def next_prod_date(self) -> QfDate:
    """
    TODO
    """
    next_date = self.date_shift(1)
    
    while not next_date.is_prod_date():
      next_date = next_date.date_shift(1)
      
    return next_date
  
  
  def prev_prod_date(self) -> QfDate:
    """
    TODO
    """
    prev_date = self.date_shift(-1)
    
    while not prev_date.is_prod_date():
      prev_date = prev_date.date_shift(-1)
      
    return prev_date
  
  
  def next_month_start(self) -> QfDate:
    """
    TODO
    """
    if self.month == 12:
      return QfDate(self.year + 1, 1, 1, calendar=self.__calendar_name, convention=self.__convention_name)
    
    return QfDate(self.year, self.month + 1, 1, calendar=self.__calendar_name, convention=self.__convention_name)
  
  
  def this_month_start(self) -> QfDate:
    """
    TODO
    """
    return QfDate(self.year, self.month, 1, calendar=self.__calendar_name, convention=self.__convention_name)
  
  
  def prev_month_start(self) -> QfDate:
    """
    TODO
    """
    if self.month == 1:
      return QfDate(self.year - 1, 12, 1, calendar=self.__calendar_name, convention=self.__convention_name)
    
    return QfDate(self.year, self.month - 1, 1, calendar=self.__calendar_name, convention=self.__convention_name)
  
  
  def next_year_start(self) -> QfDate:
    """
    TODO
    """
    return QfDate(self.year + 1, 1, 1, calendar=self.__calendar_name, convention=self.__convention_name)
  
  
  def this_year_start(self) -> QfDate:
    """
    TODO
    """
    return QfDate(self.year, 1, 1, calendar=self.__calendar_name, convention=self.__convention_name)
  
  
  def prev_year_start(self) -> QfDate:
    """
    TODO
    """
    return QfDate(self.year - 1, 1, 1, calendar=self.__calendar_name, convention=self.__convention_name)
  
  
  def next_month_end(self) -> QfDate:
    """
    TODO
    """
    return self.next_month_start().next_month_start() - 1
  
  
  def this_month_end(self) -> QfDate:
    """
    TODO
    """
    return self.next_month_start() - 1
  
  
  def prev_month_end(self) -> QfDate:
    """
    TODO
    """
    return self.this_month_start() - 1
  

  def next_year_end(self) -> QfDate:
    """
    TODO
    """
    return QfDate(self.year + 1, 12, 31, calendar=self.__calendar_name, convention=self.__convention_name)
  
  
  def this_year_end(self) -> QfDate:
    """
    TODO
    """
    return QfDate(self.year, 12, 31, calendar=self.__calendar_name, convention=self.__convention_name)
  
  
  def prev_year_end(self) -> QfDate:
    """
    TODO
    """
    return QfDate(self.year - 1, 12, 31, calendar=self.__calendar_name, convention=self.__convention_name)
  
