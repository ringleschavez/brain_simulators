#
# source: https://nbviewer.thevirtualbrain.org/url/docs.thevirtualbrain.org/tutorials/tutorial_s1_region_simulation.ipynb
#

# from tvb.simulator.lab import *
# import tvb.simulator as tvb_simulator
import numpy
import matplotlib.pyplot as plt

import tvb.simulator.models as tvb_simulator_models
import tvb.datatypes.connectivity as tvb_datatypes_connectivity
import tvb.simulator.coupling as tvb_simulator_coupling
import tvb.simulator.integrators as tvb_simulator_integrators
import tvb.simulator.monitors as tvb_simulator_monitors
import tvb.simulator.simulator as tvb_simulator_simulator

#
# Model
#
g2d_oscillator = tvb_simulator_models.Generic2dOscillator()

#
# Connectivity
#
'''
the following message could be thrown
- WARNING - tvb.basic.readers - File 'hemispheres' not found in ZIP.
'''
white_matter = tvb_datatypes_connectivity.Connectivity.from_file()
white_matter.speed = numpy.array([4.0])

#
# Coupling
#
white_matter_coupling = tvb_simulator_coupling.Linear(a=numpy.array([0.0154]))


#
# Integrator
#
'''
HeunDeterministic is used with an integration step size of 2**-6
because powers of 2 are nice.
IMPORTANT: Using a step size that is small enough for the integration
to be numerically stable,
   ideally the number chosen should also be machine representable ()
'''

heunint = tvb_simulator_integrators.HeunDeterministic(dt=2**-6)

#
# Monitors
#
# Initialise some Monitors with period in physical time
mon_raw = tvb_simulator_monitors.Raw()
mon_tavg = tvb_simulator_monitors.TemporalAverage(period=2**-2)

# Bundle them
what_to_watch = (mon_raw, mon_tavg)

#
# Simulator
#
# Initialise a Simulator -- Model, Connectivity, Integrator, and Monitors.
sim = tvb_simulator_simulator.Simulator(
                                    model=g2d_oscillator,
                                    connectivity=white_matter,
                                    coupling=white_matter_coupling,
                                    integrator=heunint,
                                    monitors=what_to_watch
                                )

sim.configure()


#
# Simulation
#
# Perform the simulation
raw_data = []
raw_time = []
tavg_data = []
tavg_time = []

for raw, tavg in sim(simulation_length=2**10):
    if raw is not None:
        raw_time.append(raw[0])
        raw_data.append(raw[1])

    if tavg is not None:
        tavg_time.append(tavg[0])
        tavg_data.append(tavg[1])

# Make the lists numpy.arrays for easier use.
RAW = numpy.array(raw_data)
TAVG = numpy.array(tavg_data)

plt.plot(raw_time, RAW[:, 0, :, 0])
plt.title('RAW - State Variable 0')
plt.savefig('raw_state_variable_0.png')

plt.plot(tavg_time, TAVG[:, 0, :, 0])
plt.title('Temporal Average')
plt.savefig('temporal_average.png')
