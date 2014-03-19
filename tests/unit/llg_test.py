import unittest
from dolfin import *
from magnumfe import *
import os

mesh     = DemagField.create_mesh((50.0/2.0, 50.0/2.0, 3.0/2.0), (50, 50, 1), d=3)
volume   = 50.0 * 50.0 * 3.0
VV       = VectorFunctionSpace(mesh, "CG", 1, 3)
arg      = "sqrt((3.141592*(x[0]/1e1))*(3.141592*(x[0]/1e1)))"
m_expr   = Expression(("cos(%s)" % arg, "sin(%s)" % arg, "0.0"))
material = Material.py()
ref_file = os.path.dirname(os.path.realpath(__file__)) + "/ref/llg_dm.xml"

class LlgTest(unittest.TestCase):

  def test_llg(self):
    llg = LLG(mesh, material, scale=1e-9, demag_order=2)
    m   = llg.interpolate(m_expr)
    dm  = llg.calculate_dm(m, 1e-12)

    #f = File(ref_file)
    #f << dm

    ref = Function(VV, ref_file)

    error = assemble(inner(ref - dm, ref - dm) / inner(ref, ref) * dx) / volume
    self.assertTrue(error < 0.3)

  def test_llg2(self):
    llg = LLG2(mesh, material, scale=1e-9, demag_order=2)
    m   = llg.interpolate(m_expr)
    dm  = llg.calculate_dm(m, 1e-12)

    ref = Function(VV, ref_file)

    error = assemble(inner(ref - dm, ref - dm) / inner(ref, ref) * dx) / volume
    self.assertTrue(error < 0.3)

  # TODO currently broken (segfault probably caused by cbc.block)
  def test_llg4(self):
    llg = LLG4(mesh, material, scale=1e-9, demag_order=1)
    m   = llg.interpolate(m_expr)
    dm  = llg.calculate_dm(m, 1e-12)

    ref = Function(VV, ref_file)

    f = File("ref/dm.pvd")
    f << dm

    error = assemble(inner(ref - dm, ref - dm) / inner(ref, ref) * dx(mesh)) / volume
    print error
    self.assertTrue(error < 0.3)

if __name__ == '__main__':
    unittest.main()
