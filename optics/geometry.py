"""
Geometry functions
@author: xiaosj
"""

import numpy as np

def rot2D(Angle):
  """ 2D rotation matrix
  """
  cosA = np.cos(Angle)
  sinA = np.sin(Angle)
  return np.array([[cosA, -sinA], [sinA, cosA]], dtype=np.float32)


def Rx(Angle):
  """ Rotation matrix along X-axis
  """
  cosA = np.cos(Angle)
  sinA = np.sin(Angle)
  return np.array([[1.,   0.,     0.],
                   [0., cosA, -sinA],
                   [0., sinA,  cosA]], dtype=np.float32)


def Ry(Angle):
  """ Rotation matrix along Y-axis
  """
  cosA = np.cos(Angle)
  sinA = np.sin(Angle)
  return np.array([[ cosA, 0., sinA],
                   [   0., 1.,   0.],
                   [-sinA, 0., cosA]], dtype=np.float32)


def Rz(Angle):
  """ Rotation matrix along Z-axis
  """
  cosA = np.cos(Angle)
  sinA = np.sin(Angle)
  return np.array([[cosA, -sinA, 0.],
                   [sinA,  cosA, 0.],
                   [  0.,    0., 1.]], dtype=np.float32)


def VectorNormalize(vec):
  """ Normalize vector (3,) or vector list (N,3).
      This fuction will overwrite values in vec
  """
  if(len(vec.shape) == 1):   # single vector
    vec /= np.sqrt(vec.dot(vec))
  elif(len(vec.shape) == 2): # list of vectors
    vec /= np.linalg.norm(vec, axis=1)[:, np.newaxis]
  else:
    raise Exception('Wrong input: vector (3,) or vector list (N,3) only')
  return vec


def Reflection(incident, norm, normalized=True):
  """ Calculate the reflection vector with unit length
      "incident" and "norm" must be vector (3,) or vector list (N,3)
      Assume normalized inputs. If not, set "normalized" to False.
  """
  if(incident.shape != norm.shape):
    raise Exception('Wrong input: incident {:} and norm {:} must be in a same shape'.format(incident.shape, norm.shape))

  if(not normalized):
    VectorNormalize(incident)
    VectorNormalize(norm)
  
  if(len(incident.shape) == 1):   # single vector
    return incident - 2. * incident.dot(norm) * norm
  elif(len(incident.shape) == 2): # list of vectors
    d = 2. * np.einsum('ij, ij->i', incident, norm)
    return incident - d[:,np.newaxis] * norm
  else:
    raise Exception('Wrong input: vector (3,) or vector list (N,3) only')


class Plane2D():
  def __init__(self, point, norm):
    self.p = point
    self.n = norm

