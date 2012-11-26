import unittest
from dolfin import *
from magnumfe import *
import numpy

class DemagFieldTest(unittest.TestCase):

    def test_create_mesh(self):
      mesh = DemagField.create_mesh((0.5, 0.5, 0.5), (11, 11, 11))
      self.assertEqual(mesh.size(0), 1331)
      self.assertEqual(mesh.with_shell.size(0), 1933)
      self.assertEqual(mesh.data['sample_size'], [0.5, 0.5, 0.5])

    def test_calculate_unit_cube(self):
      #mesh = DemagField.create_mesh("dolfin/sphere.msh", n = (11, 11, 11), margin = 0.1, d = 5)
      mesh = DemagField.create_mesh((0.5, 0.5, 0.5), (10, 10, 10), d = 3)
      #mesh = DemagField.create_mesh((0.5, 0.5, 0.5), (5, 5, 5), d = 2)
      VS = FunctionSpace(mesh, "Lagrange", 2)
      VV = VectorFunctionSpace(mesh, "Lagrange", 1)

      m = interpolate(Constant((0.0, 0.0, 1.0)), VV)
      demag = DemagField(mesh, order = 2)

      u = demag.calculate(m)
      u = demag.calculate(m)

      M = 0.5 * inner(m, grad(u)) * dx
      energy = assemble(M)
      print "Energy: %f" % energy

      self.assertTrue(abs(energy - 1.0/6.0) < 0.01)

if __name__ == '__main__':
    unittest.main()