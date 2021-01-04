#include <iostream>
#include "../optic.hh"
#include "../geometry.hh"
#include <time.h>
using namespace std;

int main() {
  Ray inp;
  inp.start  = Vector3f(0, 0, 0);
  inp.direction = Vector3f(0, 0, 1).Normalized();
  inp.stopped = false;
  cout << "Input Ray: " << inp.start << " " << inp.direction << endl << endl;

  long int seed = time(NULL);
  FlatMirror mr = FlatMirror();
  mr.center = Vector3f(0, 0, 1.5);
  mr.normal = Vector3f(1, 0, -1).Normalized();
  mr.halfSize = Vector3f(0.05, 0.05, 0.5);
  mr.dA1 = -0.1;  mr.dA2 = 0.1;
  // mr.trans1 = -0.1; mr.trans2 = 0.1;
  // mr.dA1 = 0;  mr.dA2 = 0;
  mr.trans1 = 0; mr.trans2 = 0;
  mr.orientation = xplus;
  mr.verbose = 2;

  Ray out = mr.transport(inp);
  cout << "Output Ray: " << out.start << " " << out.direction << " " << out.stopped << endl;
}