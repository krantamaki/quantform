"""@package quantform
@author Kasper Rantamäki
Setup script for the QuantForm platform

The setup script does a couple of things needed before running the main file. It 
compiles the C++ libraries, runs tests and if everything is successful, it adds the 
quantform into the Python site-packages directory so that it can be imported as a library.
"""
import os
from site import getsitepackages
from shutil import rmtree, copytree, copyfile
from pathlib import Path


def find_site_packages() -> Path:
  """
  TODO
  """
  site_packages_dirs = getsitepackages()

  for dir in site_packages_dirs:
    if dir.endswith("site-packages"):
      return Path(dir)
    

def add_quantform_to_dir(dir: Path) -> None:
  """
  TODO
  """
  qf_dirs = ["broker_api",
             "cpplib",
             "db",
             "pylib",
             "trading_strategy",
             "ui"]
  
  qf_files = ["config.yaml",
              "__init__.py"]
  
  src_path = Path(__file__).parent.resolve().as_posix()
  qf_path  = dir.as_posix() + "/quantform"

  # If old version of quantform exists in site-packages, remove it
  if os.path.isdir(qf_path):
    try:
      rmtree(qf_path)
    except OSError as e:
      raise RuntimeError(f"Couldn't delete the past version of quantform! ({e.strerror()})")

  # Add the new version to site-packages
  os.mkdir(qf_path)

  # Copy directories
  for qf_dir in qf_dirs:
    try:
      copytree(src_path + f"/{qf_dir}", qf_path + f"/{qf_dir}")
    except OSError as e:
      raise RuntimeError(f"Couldn't copy the module {qf_dir}! ({e.strerror()})")
    
  # Copy files
  for qf_file in qf_files:
    try:
      copyfile(src_path + f"/{qf_file}", qf_path + f"/{qf_file}")
    except OSError as e:
      raise RuntimeError(f"Couldn't copy the file {qf_file}! ({e.strerror()})")


def main(*args, **kwargs) -> int:
  
  # Compile C++ dependencies
  ...

  # Find the site-packages directory and add quantform there
  site_packages = find_site_packages()
  add_quantform_to_dir(site_packages)

  # Run tests
  ...

  return 0


if __name__ == "__main__":
  main()
