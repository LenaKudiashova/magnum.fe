#include "MetricMatrixCube.h"
#include <dolfin.h>
#include <iostream>

namespace magnumfe {

  // returns the biggest of three double values
  double MetricMatrixCube::max3(double a, double b, double c)
  {
    double result = a;
    if (result < b) result = b;
    if (result < c) result = c;
    return result;
  }

  // returns the biggest of three double values
  double MetricMatrixCube::min3(double a, double b, double c)
  {
    double result = a;
    if (result > b) result = b;
    if (result > c) result = c;
    return result;
  }


  // alias Power for mathematica C export
  double MetricMatrixCube::Power(double x, int y)
  {
    if (y < 0) return 1.0 / Power(x, -y);

    double result = 1.0;
    for (int i=0; i<y; ++i) {
      result *= x;
    }
    return result;
    //return std::pow(x, y);
  }

  void MetricMatrixCube::eval(dolfin::Array<double>& values, const dolfin::Array<double>& pos) const
  {
    // constats
    const double D = min3(size[0], size[1], size[2]);// * 0.5;

    //TODO check
    const int ix = (1+coord)%3;
    const int iy = (2+coord)%3;
    const int iz = (0+coord)%3;

    // point mirror position if z is negative
    const double x = (pos[iz] > 0.0) ? pos[ix] : -pos[ix];
    const double y = (pos[iz] > 0.0) ? pos[iy] : -pos[iy];
    const double z = (pos[iz] > 0.0) ? pos[iz] : -pos[iz];

    const double Lx = size[ix];
    const double Ly = size[iy];
    const double Lz = size[iz];

    double &xx = values[ix + 3*ix];
    double &xy = values[ix + 3*iy];
    double &xz = values[ix + 3*iz];
    double &yx = values[iy + 3*ix];
    double &yy = values[iy + 3*iy];
    double &yz = values[iy + 3*iz];
    double &zx = values[iz + 3*ix];
    double &zy = values[iz + 3*iy];
    double &zz = values[iz + 3*iz];

    // custom 
    const double X = Lz - Lx;
    const double Y = Lz - Ly;
    const double Z = max3(X, Y, 0.0);

    const double P = std::sqrt(
        Power(x - x*(Z-X) / (z-X), 2) +
        Power(y - y*(Z-Y) / (z-Y), 2) +
        Power(z - Z, 2));

    const double A = std::sqrt( P*(D+Lz-z) / (z-Z) );
    const double B = std::sqrt( D*P        / (z-Z) );

    xx      = (B*(Lx - Lz + z)*(Lz - Z)*(-(A*Lx) + (-A + B)*(-Lz + Z))*(-(A*Ly) + (-A + B)*(-Lz + Z))*(P/(z - Z) + (Power(x,2)*Power((-2*A + 3*B)*(-Lz + z)*(-Lz + Z) + Lx*(2*A*Lz - B*Lz - 2*A*z + B*Z) + 2*D*(A*Lx - (-A + B)*(-Lz + Z)),2))/(D*Power(Lx - Lz + z,4)*Power(Lz - Z,2))))/ (2.*Power(A,3)*(Ly - Lz + z)*Power(A*Lx - (-A + B)*(-Lz + Z),2));
    xy = yx = (B*x*y*(-((-2*A + 3*B)*(-Lz + z)*(-Lz + Z)) + Lx*(-2*A*Lz + B*Lz + 2*A*z - B*Z) + 2*D*(-(A*Lx) + (-A + B)*(-Lz + Z)))* (-((-2*A + 3*B)*(-Lz + z)*(-Lz + Z)) + Ly*(-2*A*Lz + B*Lz + 2*A*z - B*Z) + 2*D*(-(A*Ly) + (-A + B)*(-Lz + Z))))/(2.*Power(A,3)*D*Power(Lx - Lz + z,2)*Power(Ly - Lz + z,2)*(Lz - Z));
    xz = zx = (x*(-(A*Ly) + (-A + B)*(-Lz + Z))*((-2*A + 3*B)*(-Lz + z)*(-Lz + Z) + Lx*(2*A*Lz - B*Lz - 2*A*z + B*Z) + 2*D*(A*Lx - (-A + B)*(-Lz + Z))))/(A*B*Power(Lx - Lz + z,2)*(Ly - Lz + z)*(-Lz + Z));
    yy      = (B*(Ly - Lz + z)*(Lz - Z)*(-(A*Lx) + (-A + B)*(-Lz + Z))*(-(A*Ly) + (-A + B)*(-Lz + Z))*(P/(z - Z) + (Power(y,2)*Power((-2*A + 3*B)*(-Lz + z)*(-Lz + Z) + Ly*(2*A*Lz - B*Lz - 2*A*z + B*Z) + 2*D*(A*Ly - (-A + B)*(-Lz + Z)),2))/(D*Power(Ly - Lz + z,4)*Power(Lz - Z,2))))/ (2.*Power(A,3)*(Lx - Lz + z)*Power(A*Ly - (-A + B)*(-Lz + Z),2));
    yz = zy = (y*(-(A*Lx) + (-A + B)*(-Lz + Z))*((-2*A + 3*B)*(-Lz + z)*(-Lz + Z) + Ly*(2*A*Lz - B*Lz - 2*A*z + B*Z) + 2*D*(A*Ly - (-A + B)*(-Lz + Z))))/(A*B*(Lx - Lz + z)*Power(Ly - Lz + z,2)*(-Lz + Z));
    zz      = (2*(D + Lz - z)*(-(A*Lx) + (-A + B)*(-Lz + Z))*(-(A*Ly) + (-A + B)*(-Lz + Z)))/(A*B*(Lx - Lz + z)*(Ly - Lz + z)*(Lz - Z));
  }

};
