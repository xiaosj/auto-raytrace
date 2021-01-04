#ifndef GEOMETRY_HH
#define GEOMETRY_HH

#include <vector>
using namespace std;

float deg2rad(float deg) {
  return deg / 180.0 * M_PI;
};

float rad2deg(float rad) {
  return rad / M_PI * 180.0;
};

struct Ray {
  Vector3f start;  // start point
  Vector3f direction;  // normlized direction vector
  bool stopped;  // whether the ray is stopped
};

vector<Vector3f> Trace;
// vector<vector<int> > obj(N);
// for(int i =0; i< obj.size(); i++)//动态二维数组为5行6列，值全为0 
//     { 
//         obj[i].resize(M); 
//     }

#endif