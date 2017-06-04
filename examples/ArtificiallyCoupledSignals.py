"""Generate signals that contains a phase-amplitude coupling."""
import matplotlib.pyplot as plt
from tensorpac.utils import PacSignals

# Generate one signal containing PAC. By default, this signal present a
# coupling between a 2hz phase and a 100hz amplitude (2 <-> 100) :
sig, time = PacSignals(ndatasets=1)

# Now, we generate a longer and weaker 4 <-> 60 coupling using the chi
#  parameter. In addition, we increase the amount of noise :
sig2, time2 = PacSignals(fpha=4, famp=60, ndatasets=1, chi=.9, noise=3, tmax=3)

# Alternatively, you can generate multiple coupled signals :
sig3, time3 = PacSignals(fpha=10, famp=150, ndatasets=3, chi=0.5, noise=2)

# Finally, if you want to add variability across generated signals, use the
# dpha and damp parameters :
sig4, time4 = PacSignals(fpha=1, famp=50, ndatasets=3, dpha=30, damp=70, tmax=3)


def plot(time, sig, title):
    """Plotting function."""
    plt.plot(time, sig.T)
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')


fig = plt.figure()
plt.subplot(2, 2, 1)
plot(time, sig, 'Strong coupling between 2hz <-> 100hz')

plt.subplot(2, 2, 2)
plot(time2, sig2, 'Weak and noisy coupling between 4hz <-> 60hz')

plt.subplot(2, 2, 3)
plot(time3, sig3, '3 signals coupled between 10hz <-> 150hz')

plt.subplot(2, 2, 4)
plot(time4, sig4, '3 signals coupled, with variability between 1hz <-> 50hz')

plt.show()