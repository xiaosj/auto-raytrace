#ifndef VECTOR_HH
#define VECTOR_HH

#include <math.h>
#include <iostream>
#include <sstream>
#include <string>
#include <cassert>

const double epsilon = 4.37114e-05;

// 3D vector
template <class T>
class Vector3 {
public:
  T x; T y; T z;

  // ---- Constructors ----
  Vector3() {
    x = 0.0; y = 0.0; z = 0.0;
  }
  Vector3(T nx, T ny, T nz) {
    x = nx; y = ny; z = nz;
  }
  Vector3(const Vector3<T>& v) {
    x = v.x; y = v.y; z = v.z;
  }
  template <class FromT>
  Vector3(const Vector3<FromT>& v): x(static_cast<T>(v.x)), y(static_cast<T>(v.y)), z(static_cast<T>(v.z)) {}

  // ---- Access Operators ----
  Vector3<T> operator=(const Vector3<T>& v) {
    x = v.x; y = v.y; z = v.z;
    return *this;
  }

  template <class FromT>
  Vector3<T> operator=(const Vector3<FromT>& v) {
    x = static_cast<T>(v.x); y = static_cast<T>(v.y); z = static_cast<T>(v.z);
    return *this;
  }

  T & operator[](int i) {
    assert(i >= 0 && i <= 2);
    if(i == 0)
      return x;
    else if(i == 1)
      return y;
    else if(i == 2)
      return z;
  }

  const T & operator[](int i) const {
    assert(i >= 0 && i <= 2);
    if(i == 0)
      return x;
    else if(i == 1)
      return y;
    else if(i == 2)
      return z;
  }

  // ---- Arithmetic operators ----
  Vector3<T> operator+(const Vector3<T>& v) const {
    return Vector3<T>(x + v.x, y + v.y, z + v.z);
  }
  Vector3<T> operator-(const Vector3<T>& v) const {
    return Vector3<T>(x - v.x, y - v.y, z - v.z);
  }
  Vector3<T> operator-() const {
    return Vector3<T>(-x, -y, -z);
  }
  Vector3<T> operator*(T v) const {
    return Vector3<T>(x * v, y * v, z * v);
  }
  Vector3<T> operator/(T v) const {
    assert(v != 0.0);
    return Vector3<T>(x / v, y / v, z / v);
  }

  Vector3<T>& operator+=(const Vector3<T>& v) {
    x += v.x; y += v.y; z += v.z;
    return *this;
  }
  Vector3<T>& operator-=(const Vector3<T>& v) {
    x -= v.x; y -= v.y; z -= v.z;
    return *this;
  }
  Vector3<T>& operator*=(T v) {
    x *= v; y *= v; z *= v;
    return *this;
  }
  Vector3<T>& operator/=(T v) {
    assert(v != 0.0);
    x /= v; y /= v; z /= v;
    return *this;
  }

  T dot(const Vector3<T>& v) const {
    return x * v.x + y * v.y + z * v.z;
  }
  Vector3<T> cross(const Vector3<T>& v) const {
    return Vector3<T>(y * v.z - z * v.y, z * v.x - x * v.z, x * v.y - y * v.x);
  }
  T length() const {
    return (T) sqrt(x * x + y * y + z * z);
  }
  void normalize() {
    T s = length();
    assert(s > 0);
    x /= s; y /= s; z /= s;
  }
  Vector3<T> Normalized() const {
    T s = length();
    assert(s > 0);
    return Vector3<T>(x / s, y / s, z / s);
  }

  // ---- Rotation ----
  Vector3<T> Rx(T angle) const {
    T cosA = cos(angle);
    T sinA = sin(angle);
    T nx = x;
    T ny = cosA * y - sinA * z;
    T nz = sinA * y + cosA * z;
    return Vector3<T>(nx, ny, nz);
  }
  Vector3<T> Ry(T angle) const {
    T cosA = cos(angle);
    T sinA = sin(angle);
    T nx = cosA * x + sinA * z;
    T ny = y;
    T nz =-sinA * x + cosA * z;
    return Vector3<T>(nx, ny, nz);
  }
  Vector3<T> Rz(T angle) const {
    T cosA = cos(angle);
    T sinA = sin(angle);
    T nx = cosA * x - sinA * y;
    T ny = sinA * y + cosA * x;
    T nz = z;
    return Vector3<T>(nx, ny, nz);
  }

  Vector3<T> Reflect(const Vector3<T>& norm) const {
  // "norm" is the normal of the reflection surface
    Vector3<T> in = Normalized();
    Vector3<T> n = norm.Normalized();
    T fac = 2.0 * in.dot(n);
    return in - n * fac;
  }

  // ---- Compare and Conversion ----
  bool operator==(const Vector3<T>& v) const {
    return abs(x - v.x) < epsilon && abs(y - v.y) < epsilon && abs(z - v.z) < epsilon;
  }
  bool operator!=(const Vector3<T>& v) const {
    return !(*this == v);
  }
  operator T* () {
    return (T*) this;
  }
  operator const T* () const {
    return (const T*) this;
  }

  // ---- Ooutput ----
  friend std::ostream& operator<<(std::ostream& stream, const Vector3<T> v) {
    stream << "[" << v.x << ", " << v.y << ", " << v.z << "]";
    return stream;
  }
  // std:string toString() const {
  //   std::ostringstream oss;
  //   oss << *this;
  //   return oss.str();
  // }
};

typedef Vector3<float>  Vector3f;
typedef Vector3<double> Vector3d;

#endif