#include <iostream>
#include "../optic.hh"
#include "../geometry.hh"
using namespace std;

int main() {
  Ray inp;
  inp.start  = Vector3f(0, 0, 0);
  inp.direction = Vector3f(1, 1, 0).Normalized();
  inp.stopped = false;
  cout << "Input Ray: " << inp.start << " " << inp.direction << endl << endl;

  Collimator c;
  c.center = Vector3f(3, 0, 0);
  c.normal = Vector3f(1, 1, 0).Normalized();
  c.iR = 1;
  c.oR = 3;
  cout << "Collimator: " << c.center << " " << c.normal << " " << c.iR << " " << c.oR << endl;

  Ray out = c.transport(inp);
  cout << "Output Ray: " << out.start << " " << out.direction << " " << out.stopped << endl << endl;

  c.center = Vector3f(2, 0, 0);
  c.normal = Vector3f(1, 0, 0).Normalized();
  out = c.transport(inp);
  cout << "Collimator: " << c.center << " " << c.normal << " " << c.iR << " " << c.oR << endl;
  cout << "Output Ray: " << out.start << " " << out.direction << " " << out.stopped << endl;

}