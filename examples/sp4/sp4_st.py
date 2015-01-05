"""
MuMag Standard Problem #4 computed with the shell-transform method for
the demagnetization-field computation.
"""

# Copyright (C) 2011-2015 Claas Abert
#
# This file is part of magnum.fe. 
#
# magnum.fe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# magnum.fe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with magnum.fe. If not, see <http://www.gnu.org/licenses/>.
# 
# Last modified by Claas Abert, 2015-01-05

from dolfin import *
from magnumfe import *

#######################################
#### GENERATE MESH WITH SHELL
#######################################

mesh, sample_size = DemagField.create_mesh((500.0/2.0, 125.0/2.0, 3.0/2.0), (100, 25, 1), d=4)

#######################################
#### RELAX SYSTEM TO S-STATE
#######################################

# define start magnetization
arg     = "sqrt((3.141592*(x[0]/1e3))*(3.141592*(x[0]/1e3)))"
m_start = Expression(("cos(%s)" % arg, "sin(%s)" % arg, "0.0"))

state   = State(mesh, material = Material.py(), scale = 1e-9, m = m_start)
llg     = LLGAlougesProject([ExchangeField(), DemagField("ST", sample_size, 2)])

state.material.alpha = 1.0
for i in range(200): llg.step(state, 2e-11)

#######################################
#### SIMULATE SWITCHING
#######################################

state.material.alpha = 0.02

llg = LLGAlougesProject([
    ExternalField((-24.6e-3/Constants.mu0, +4.3e-3/Constants.mu0, 0.0)),
    ExchangeField(),
    DemagField("ST", sample_size, 2)
])

logfile = open("sp4_st.dat", "w", 0)
dt, T = 2e-13, 1e-9

for i in range(int(T / dt)):
  #if (i % 10 == 0):
  #  f = File("data/m_%d.pvd" % int(i/10))
  #  f << state.m

  # write scalar information
  logfile.write("%.10f %f %f %f\n" % ((state.t*1e9,) + state.m.average()))

  # calculate next step
  state.step(llg, dt)

logfile.close()
