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

    def test_energy_unit_cube(self):
      energy = self.energy_cube()
      self.assertTrue(abs(energy - 1.0/6.0) < 0.01)

    def test_energy_scaled_big_cube(self):
      energy = self.energy_cube(2)
      self.assertTrue(abs(energy - 8.0/6.0) < 0.08)

    def test_energy_scaled_small_cube(self):
      energy = self.energy_cube(0.5)
      self.assertTrue(abs(energy - 1.0/48.0) < 0.001)

    def energy_cube(self, scale=1.0):
      mesh = DemagField.create_mesh((0.5, 0.5, 0.5), (10, 10, 10), d = 3, scale=scale)
      VS = FunctionSpace(mesh, "Lagrange", 2)
      VV = VectorFunctionSpace(mesh, "Lagrange", 1)

      m = interpolate(Constant((0.0, 0.0, 1.0)), VV)
      demag = DemagField(mesh, order = 2)

      u = demag.calculate(m)

      M = 0.5 * inner(m, grad(u)) * dx
      return assemble(M)
    
    def test_energy_sphere(self):
      mesh = DemagField.create_mesh("mesh/sphere.msh", d=5, n=(10,10,10), margin=0.2)
      f = File("sphere.pvd")
      f << mesh.with_shell

      VV = VectorFunctionSpace(mesh, "CG", 1)

      # calculate demag potential
      m = interpolate(Constant((0.0, 0.0, 1.0)), VV)
      demag = DemagField(mesh, order = 2)
      u = demag.calculate(m)

      # calculate demag energy
      M = 0.5 * inner(m, grad(u)) * dx
      energy = assemble(M)

      self.assertTrue(abs(energy - pi/36.0) < 0.01)

if __name__ == '__main__':
    unittest.main()
