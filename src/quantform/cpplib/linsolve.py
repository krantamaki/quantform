"""@package quantform.cpplib.linsolve
@author Kasper Rantamäki
Submodule with basic linear solver implementation
"""
from typing import List, Literal
from pathlib import Path
from scipy.sparse import csr_matrix
import ctypes
import numpy as np


clinsolve = ctypes.cdll.LoadLibrary(Path(__file__).parent.resolve() / "clinsolve.so")


def linsolve(system_matrix: csr_matrix[float], rhs_vector: np.ndarray[float], solver: Literal['CG', 'CGNR', 'TCGNR', 'IRLS'] = 'CGNR') -> np.ndarray[float]:
  """
  TODO
  """
  assert solver.upper() in ['CG', 'CGNR', 'TCGNR', 'IRLS'], f"Invalid solver specified! ('{solver}' not in ['CG', 'CGNR', 'TCGNR', 'IRLS'])"
  
  # Convert the Python lists into C arrays
  value_arr  = (ctypes.c_double * len(system_matrix.data))(*list(system_matrix.data))
  colInd_arr = (ctypes.c_int * len(system_matrix.indices))(*list(system_matrix.indices))
  rowPtr_arr = (ctypes.c_int * len(system_matrix.indptr))(*list(system_matrix.indptr))
  rhs_arr    = (ctypes.c_double * len(rhs_vector))(*list(rhs_vector))
  x0_arr     = (ctypes.c_double * system_matrix.shape[1])(*([0.0] * system_matrix.shape[1]))

  # Set the return type for the linsolve function
  # clinsolve.linsolve.restype = np.ctypeslib.ndpointer(dtype=ctypes.c_double, shape=(system_matrix.shape[1],))
  
  # Solve the problem
  clinsolve.linsolve(system_matrix.shape[0], system_matrix.shape[1], len(system_matrix.data), value_arr, rowPtr_arr, colInd_arr, rhs_arr, x0_arr, bytes(solver, "utf-8"))
  
  return x0_arr[0:system_matrix.shape[1]]