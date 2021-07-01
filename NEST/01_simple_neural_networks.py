
#
# source: https://nest-simulator.readthedocs.io/en/v3.0/tutorials/pynest_tutorial/part_1_neurons_and_simple_neural_networks.html
#

import matplotlib.pyplot as plt
import nest


# NodeCollection
print('creating...')
neuron = nest.Create("iaf_psc_alpha")
print('NodeCollection,neuron={}'.format(neuron))

# getting neuron's properties
print(neuron.get())

neuron.get("I_e")
neuron.get(["V_reset", "V_th"])

# setting values
neuron.set(I_e=375.0)
print(neuron.I_e)
neuron.set({"I_e": 366.6})
print(neuron.I_e)


neuron.I_e = 376.0
print(neuron.I_e)


# multimeter
# a device we can use to record the membrane voltage of a neuron over time
multimeter = nest.Create("multimeter")
multimeter.set(record_from=["V_m"])


# spike recorder
spikerecorder = nest.Create("spike_recorder")

# Connecting
nest.Connect(multimeter, neuron)
nest.Connect(neuron, spikerecorder)


# Simulation per se
print('simulating...')
nest.Simulate(1000.0)

# getting data by means of a multimeter data recorder
dmm = multimeter.get()
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]

# plotting
print('plotting...')
plt.plot(ts, Vms)
plt.title('multimeter events')
plt.savefig('01_01_multimeter_events.png')

# getting specific events
dSD = spikerecorder.get("events")
evs = dSD["senders"]
ts = dSD["times"]
plt.figure(2)
plt.plot(ts, evs, ".")
plt.savefig('01_02_events_senders_times.png')


# Second Neuron
neuron2 = nest.Create("iaf_psc_alpha")
neuron2.set({"I_e": 370.0})

nest.Connect(multimeter, neuron2)


print('simulating connected neurons')
nest.Simulate(1000.0)

plt.figure(3)
Vms1 = dmm["events"]["V_m"][::2] # start at index 0: till the end: each second entry
ts1 = dmm["events"]["times"][::2]
plt.plot(ts1, Vms1)
Vms2 = dmm["events"]["V_m"][1::2] # start at index 1: till the end: each second entry
ts2 = dmm["events"]["times"][1::2]
plt.plot(ts2, Vms2)
plt.savefig('01_03_connected_neurons')

