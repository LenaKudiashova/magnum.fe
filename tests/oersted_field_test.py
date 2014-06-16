import unittest
from dolfin import *
from magnumfe import *
import os

set_log_active(False)

mesh, sample_size = DemagField.create_mesh((0.5, 0.5, 0.5), (10, 10, 10), d=4)
ref_file = os.path.dirname(os.path.realpath(__file__)) + "/ref/oersted.xml"

class OerstedFieldTestFK(unittest.TestCase):

  def test_field_fk(self):
    oersted_field = OerstedField("FK")
    state = State(mesh, j = Constant((0.0, 0.0, 1.0)))

    components = oersted_field.calculate_field(state)
    field = project(as_vector(components), state.VectorFunctionSpace())

    ref   = Function(state.VectorFunctionSpace(), ref_file)
    error = assemble(inner(ref - field, ref - field) / inner(ref, ref) * state.dx('magnetic'))

    self.assertTrue(error < 0.01)

  def test_field_st(self):
    oersted_field = OerstedField("ST", sample_size, 2)
    state = State(mesh, j = Constant((0.0, 0.0, 1.0)))

    components = oersted_field.calculate_field(state)
    field = project(as_vector(components), state.VectorFunctionSpace())

    ref   = Function(state.VectorFunctionSpace(), ref_file)
    error = assemble(inner(ref - field, ref - field) / inner(ref, ref) * state.dx('magnetic'))

    self.assertTrue(error < 0.01)

if __name__ == '__main__':
    unittest.main()
