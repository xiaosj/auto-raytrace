#include <iostream>
#include "../vector.hh"
#include "../geometry.hh"
using namespace std;

int main() {
  Vector3f v1(1, 2, 3);
  Vector3f v2(0.1, 0.2, 0.3);
  cout << v1 << " + " << v2 << " = " << v1 + v2 << endl;
  cout << v1 << " - " << v2 << " = " << v1 - v2 << endl;
  cout << v1 << " . " << v2 << " = " << v1.dot(v2) << endl;
  cout << v1 << " x " << v2 << " = " << v1.cross(v2) << endl;
 
  float r = 0.5;
  cout << v1 << " * " << r << " = " << v1 * r << endl;
  cout << v1 << " / " << r << " = " << v1 / r << endl;

  float angle = deg2rad(90);
  cout << v2 << " rotate 90-deg X = " << v2.Rx(angle) << endl;
  cout << v2 << " rotate 90-deg Y = " << v2.Ry(angle) << endl;
  cout << v2 << " rotate 90-deg Z = " << v2.Rz(angle) << endl;
  cout << v1 << " x " << v2.Rx(angle) << " = " << v1.cross(v2.Rx(angle)) << endl;
  
  Vector3f v2_old = v2;
  v2.normalize();
  cout << "Normalized " << v2_old << " = " << v2 << endl;

  Vector3f v3(1, -1, 0);
  Vector3f v4(0, 2, 0);
  Vector3f v5 = v3.Reflect(v4);
  cout << v3 << " reflect from " << v4 << " = " << v5 << endl;
}