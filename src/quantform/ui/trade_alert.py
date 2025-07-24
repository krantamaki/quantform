"""@package quantform.ui.trade_alert
@author Kasper Rantamäki
Module that provides some utility functions for playing a sound each time a trade is completed
"""
import os
import sys
from pathlib import Path


def trade_alert(sound_effect_path: Path) -> None
  """Simple function for playing a given sound effect
  
  @param sound_effect_path  The path to the sound effect file
  @raises RuntimeError      Raised if the operating system is not Linux
  @return                   None
  """
  
  if sys.platform != 'linux':
    raise RuntimeError(f"Trade alert is currently only available for Linux! (platform = {sys.platform})")

  os.system("mpg123 " + sound_effect_path.as_posix())
  