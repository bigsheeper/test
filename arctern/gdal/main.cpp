#include <iostream>
#include <ogr_api.h>
#include <ogrsf_frmts.h>

int main() {
  OGRGeometry *geo;
  OGRGeometryFactory::createFromWkt("Polygon ((0 1, 0 2, 1 1, 0 1))", nullptr, &geo);
  auto x1 = geo->toPoint()->getX();
  auto y1 = geo->toPoint()->getY();
  int size = geo->WkbSize();
  std::vector<char> wkb(size);
  geo->exportToWkb(OGRwkbByteOrder::wkbNDR, (uint8_t*)wkb.data());

  std::string str(wkb.begin(), wkb.end());

  OGRGeometry* geo2;
  OGRGeometryFactory::createFromWkb(str.data(), nullptr, &geo2);
  auto x2 = geo2->toPoint()->getX();
  auto y2 = geo2->toPoint()->getY();

  auto wkb_cstr = str.data();


  auto res = geo->Equals(geo2);

  return 0;
}