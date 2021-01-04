"""
Geometry functions
@author: xiaosj
"""

import numpy as np

def rot2D(A):
    cosA = np.cos(A)
    sinA = np.sin(A)
    return np.array([[cosA, -sinA], [sinA, cosA]], dtype=np.float32)


class Vector3:
    """Class of 3D vectors.

    Args:
        x, y, z: coordinates of the vector.
    
    Properties:
        digits: The number of digits to be printed.
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self._digits = 2

    def length(self):
        """Return the length of the vector"""
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalized(self):
        """Return the normalized vector"""
        l = self.length()
        if l > 0:
            return Vector3(self.x / l, self.y / l, self.z / l)
        else:
            raise ValueError(f'The length of the vector must be greater than zero to be normalized: {self.x}, {self.y}, {self.z}')

    def norm(self):
        """Normalize the vector itself, no return value"""
        l = self.length()
        if l > 0:
            self.x /= l
            self.y /= l
            self.z /= l
        else:
            raise ValueError(f'The length of the vector must be greater than zero to be normalized: {self.x}, {self.y}, {self.z}')

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar):
        if scalar != 0:
            return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
        else:
            raise ValueError(f'The input scalar ({scalar}) must not be zero.')

    def dot(self, other):
        """Dot product"""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        """Cross product"""
        return Vector3(self.y * other.z - self.z * other.y,
                       self.z * other.x - self.x * other.z,
                       self.x * other.y - self.y * other.x)

    def Rx(self, angle):
        """Rotate the vector along the x-axis."""
        cosA = np.cos(angle)
        sinA = np.sin(angle)
        return Vector3(self.x,
                       cosA * self.y - sinA * self.z,
                       sinA * self.y + cosA * self.z)

    def Ry(self, angle):
        """Rotate the vector along the y-axis."""
        cosA = np.cos(angle)
        sinA = np.sin(angle)
        return Vector3(cosA * self.x + sinA * self.z,
                       self.y,
                       -sinA * self.x + cosA * self.z)
    
    def Rz(self, angle):
        """Rotate the vector along the z-axis."""
        cosA = np.cos(angle)
        sinA = np.sin(angle)
        return Vector3(cosA * self.x - sinA * self.y,
                       sinA * self.y + cosA * self.x,
                       self.z)

    def Reflect(self, norm):
        """Return a vector reflected from the surface whose normlize vector is 'norm'.
           No need to normlize the input vector and norm.
        """
        input = self.normalized()
        n = norm.normalized()
        fac = 2 * input.dot(n)
        return input - n * fac

    @property
    def digits(self):
        return self._digits

    @digits.setter
    def digits(self, value):
        if isinstance(value, int) and value >= 0:
            self._digits = value
        else:
            raise ValueError(f'The input ({value}) must be an integer greater than or equal to 0.')

    def __str__(self):
        return f'[{self.x:.{self._digits}f}, {self.y:.{self._digits}f}, {self.z:.{self._digits}f}]'


class Ray:
    """Class of ray.

    Args:
        start: start point.
        direction: direction of the vector (will be normalized automatically).
    
    Property:
        stopped (bool): whether the ray is stopped.
        digits: The number of digits to be printed.
    """
    def __init__(self, start: Vector3, direction: Vector3):
        self.start = start
        self.direction = direction
        self._stopped = False
        self._digits = 2
    
    @property
    def stopped(self):
        return self._stopped
    
    @stopped.setter
    def stopped(self, value):
        if isinstance(value, bool):
            self._stopped = value
        else:
            raise TypeError(f'value ({value}) must be a bool')

    @property
    def digits(self):
        return self._digits

    @digits.setter
    def digits(self, value):
        if isinstance(value, int) and value >= 0:
            self._digits = value
            self.start.digits = value
            self.direction.digits = value
        else:
            raise ValueError(f'The input ({value}) must be an integer greater than or equal to 0.')

    def __str__(self):
        return f'{{{self.start}, {self.direction}, {self.stopped}}}'
