import unittest
from dolfin import *
from magnumfe import *
import numpy

#mesh           = DemagField.create_mesh((50.0/2.0, 50.0/2.0, 3.0/2.0), (10, 10, 1), d=3)
#mesh           = DemagField.create_mesh((500.0/2.0, 125.0/2.0, 3.0/2.0), (100, 25, 1), d=4)
mesh           = DemagField.create_mesh((500.0/2.0, 125.0/2.0, 3.0/2.0), (10, 10, 1), d=2)
VV             = VectorFunctionSpace(mesh, "CG", 1, 3)

material       = Material.py()
material.alpha = 1.0

arg            = "sqrt((3.141592*(x[0]/1e1))*(3.141592*(x[0]/1e1)))"
m_expr         = Expression(("cos(%s)" % arg, "sin(%s)" % arg, "0.0"))
dt             = 1e-12

class LlgTest4(unittest.TestCase):

  def test_llg4(self):
    llg = LLG4(mesh, material, scale=1e-9, demag_order=2)
    m   = llg.interpolate(m_expr)
    dm  = llg.calculate_dm(m, dt)

    #m2  = llg.step(m, dt)
    #f  = File("data4/dm_b.pvd")
    #f << dm

if __name__ == '__main__':
    unittest.main()
