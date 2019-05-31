from brian import *
# Neuron model parameters
Vr = -70 * mV
Vt = -55 * mV
taum = 10 * ms # was 10, 12.35 interesting TMM modifications 20140424
taupsp = 0.325 * ms
weight = 4.86 * mV
# Neuron model
eqs = Equations('''
dV/dt=(-(V-Vr)+x)*(1./taum) : volt
dx/dt=(-x+y)*(1./taupsp) : volt
dy/dt=-y*(1./taupsp)+25.27*mV/ms+\
    (39.24*mV/ms**0.5)*xi : volt
''')
# Neuron groups.  Modified to be larger TMM
P = NeuronGroup(N=5000, model=eqs,
    threshold=Vt, reset=Vr, refractory=1 * ms)
Pinput = PulsePacket(t=50 * ms, n=51, sigma=1 * ms)
# The network structure.  Modified to be larger TMM
Pgp = [ P.subgroup(100) for i in range(50)]
C = Connection(P, P, 'y')
# modified to be larger TMM
for i in range(49):
    C.connect_full(Pgp[i], Pgp[i + 1], weight)
Cinput = Connection(Pinput, Pgp[0], 'y')
Cinput.connect_full(weight=weight)
# Record the spikes
Mgp = [SpikeMonitor(p) for p in Pgp]
Minput = SpikeMonitor(Pinput)
monitors = [Minput] + Mgp
# Setup the network, and run it
P.V = Vr + rand(len(P)) * (Vt - Vr)
run(100 * ms)
# Plot result
raster_plot(showgrouplines=True, *monitors)
show()
