#ifndef OPTIC_HH
#define OPTIC_HH

#include "vector.hh"
#include "geometry.hh"
#include <random>
using namespace std;

enum opticType {
  opticSource,
  opticCollimator,
  opticFlatMirror
};


enum mirrorOrientation { xplus, xminus, yplus, yminus };


class Optic {
  public:
    Optic()  {}
    virtual ~Optic()  {}
    virtual Ray transport(Ray inp)  {}
    opticType type;
};


class Collimator : public Optic {
  public:
    Vector3f center;
    Vector3f normal;
    float iR, oR;   // inner radius, outer radius

    Collimator() { type = opticCollimator; }

    Ray transport(Ray inp) {
      Ray out;
      out.direction = inp.direction;

      Vector3f w = center - inp.start;
      float s = normal.dot(w) / normal.dot(inp.direction);
      out.start = inp.start + inp.direction * s;

      Vector3f d = out.start - center;
      float dist = d.length();
      if(dist > iR && dist < oR)
        out.stopped = true;
      else
        out.stopped = false;
      
      return out;
    }
};


class FlatMirror : public Optic {
  private:
    default_random_engine generator;
    uniform_real_distribution<float> rand_dA;
    uniform_real_distribution<float> rand_trans;
    Vector3f normal;
    float halfLength, halfWidth, thickness;
    float A;

  public:
    Vector3f center;
    Vector3f nominalIn;   // the nominal incident vector
    Vector3f nominalOut;  // the nominal output vector
    float dA1, dA2;       // - rotation range, + rotation range
    float trans1, trans2; // - translation range, + translation range
    int orientation;      // +1,-1 = +X,-X; +2,-2 = +Y,-Y
    bool surfaceOnly;
    int verbose;          // output debug information if > 1

    FlatMirror(float length, float width, float thickness,
               Vector3f center, // mirror center
               Vector3f nominalIn, // norminal incident vector
               mirrorOrientation orientation,  // mirror orientation
               float incidentA, float dA_1, float dA_2, // incident angle (rad), rotation angle
               float trans_1, float trans_2, // transition range
               long int random_seed,
               bool surface_only) {
      type = opticFlatMirror;
      halfLength = length * 0.5;
      halfWidth = width * 0.5;
      this->thickness = thickness;
      this->center = center;
      this->nominalIn = nominalIn;
      this->orientation = orientation;
      A = incidentA;  dA1 = dA_1;  dA2 = dA_2;
      trans1 = trans_1; trans2 = trans_2;
      generator.seed(random_seed);
      rand_dA = uniform_real_distribution<float>(dA1, dA2);
      rand_trans = uniform_real_distribution<float>(trans1, trans2);
      surfaceOnly = surface_only;

      // calculate the normal vector

      // calculate the nominal output surface

    }

    Ray transport(Ray inp) {
      // generate a random mirror angle by rotating the normal, and
      // generate a random mirror plane by shifting the center point
      float dA = rand_dA(generator);
      float trans = rand_trans(generator);
      Vector3f n; // new normal 
      Vector3f c = center;  // new center point, copy the current center first
      switch (orientation) {
        case xplus:
          n = normal.Ry(dA);
          c.x += trans;
          break;
        case xminus:
          n = normal.Ry(-dA);
          c.x -= trans;
          break;
        case yplus:
          n = normal.Rx(dA);
          c.y += trans;
          break;
        case yminus:
          n = normal.Rx(-dA);
          c.y -= trans;
          break;
      }

      // calculate the hitting point of the ray to the mirror surface (infinite plane)
      Vector3f w = c - inp.start;
      float s = n.dot(w) / n.dot(inp.direction);
      Vector3f hit = inp.start + inp.direction * s;

      if(verbose > 1) {
        cout << "New mirror normal = " << n << ", dA = " << dA << endl;
        cout << "New mirror center = " << c << ", trans = " << trans << endl;
        cout << "Hit point = " << hit << endl;
      }

      float xmin, ymin, xmax, ymax, zmin, zmax;
      if(orientation == xplus || orientation == xminus) {
        Vector3f delta = n.Ry(-M_PI * 0.5) * halfSize.z;
        xmin = c.x - delta.x;
        xmax = c.x + delta.x;
        ymin = c.y - halfSize.y;
        ymax = c.y + halfSize.y;
        zmin = c.z - delta.z;
        zmax = c.z + delta.z;
        if(verbose > 1) {
          cout << "Delta: " << delta << endl; }
      }
      if(verbose > 1) {
        cout << "X Range: " << xmin << ", " << xmax << endl;
        cout << "Y Range: " << ymin << ", " << ymax << endl;
        cout << "Z Range: " << zmin << ", " << zmax << endl << endl;
      }

      Ray out;
      // chek if the hitting point is in the valid mirror surface
      if(hit.x >= xmin && hit.x <= xmax &&
         hit.y >= ymin && hit.y <= ymax &&
         hit.z >= zmin && hit.z <= zmax) {
        // hitting the valid mirror surface
        if(verbose > 1)  cout << "Hit mirror surface" << endl;
        out.start = hit;
        out.direction = inp.direction.Reflect(n);
        out.stopped = false;
      }
      else { // not hitting the valid mirror surface
        if(surfaceOnly) {
          // for surface only transport, the ray will go through
          out.start = hit;
          out.direction = inp.direction;
          out.stopped = false;
        }
        else { // check if the ray will be blocked by the mirror body

        }
      }
      return out;
    }
};

#endif