import unittest
from dolfin import *
from magnumfe import *
import numpy

class LlgTest(unittest.TestCase):

  def prepare_s_state(self):
    mesh  = DemagField.create_mesh((500.0/2.0, 125.0/2.0, 3.0/2.0), (100, 25, 1), d=3, scale=1e-9)
    VV    = VectorFunctionSpace(mesh, "CG", 1, 3)

    filename = "data/s-state.xml"
    try:
      with open(filename) as f: pass
      # File exists, read and return
      return Function(VV, filename)

    except IOError as e:
      # File does not exists, calculate s-state and return
      arg = "sqrt((3.141592*(x[0]/1e-6))*(3.141592*(x[0]/1e-6)))"
      m   = interpolate(Expression(("cos(%s)" % arg, "sin(%s)" % arg, "0.0")), VV)

      material = Material.py()
      material.alpha = 1.0

      llg = LLG2(mesh, material)

      for i in range(60):
        m = llg.step(m, 8e-12)

      f = File(filename)
      f << m

      return m

  def test_sp4(self):
    mesh  = DemagField.create_mesh((500.0/2.0, 125.0/2.0, 3.0/2.0), (100, 25, 1), d=3, scale=1e-9)
    VV    = VectorFunctionSpace(mesh, "CG", 1, 3)

    m = self.prepare_s_state()
    llg = LLG2(mesh, Material.py())
    field = Constant((-24.6e-3/Constants.mu0, +4.3e-3/Constants.mu0, 0.0))

    scalar_file = open("data/sp4.dat","w",0)
    dt = 5e-14
    T  = 1e-9

    t  = 0.0
    print "Total Steps: %d" % int(T / dt)
    for i in range(int(T / dt)):
      t = i * dt
      
      # write magnetization configuration (only each 20th step)
      if (i % 20 == 0):
        f = File("data/m_%d.pvd" % int(i/20))
        f << m

      # write scalar information
      volume = 187500e-27 
      m_x = assemble(m[0] / volume * dx)
      m_y = assemble(m[1] / volume * dx)
      m_z = assemble(m[2] / volume * dx)
      scalar_file.write("%.10f %f %f %f\n" % (t*1e9, m_x, m_y, m_z))

      # calculate next step
      m = llg.step(m, dt, h_ext = field)

    scalar_file.close()

if __name__ == '__main__':
    unittest.main()
