 
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
from itertools import product

#$ fourier
def fourier(freq, components, tlims=[0,1]):
  """
  freq is a number
  components is a list of numbers
  """
  t = np.linspace(*tlims, num=1000)
  y = 0*t
  for n in components:
    y += 1.0/n * np.sin(2*np.pi*(freq*n)*t)
  return t, y
#$

#$ make_plots
def make_plots():
  freqs = [1,2,3,4,5]
  components = [1,3,5,7,9]
  for freq, num in product(freqs, range(1,6)):
    print(freq, num)
    
    t, y = fourier(freq, components[:num])
    
    fig = plt.figure(figsize=[3,2])
    plt.plot(t, y, c=[.3,.5,1], lw=2.5)
    plt.title("{} Hz, {} Component{}".format(
      freq, num, "" if num == 1 else "s"))
    plt.tight_layout()
    plt.savefig("../img/fouriers/{}_{}.pdf".format(
      freq, num))
    plt.close()
#$

if __name__ == "__main__":
  make_plots()
  