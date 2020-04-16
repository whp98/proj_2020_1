import h5py
import numpy as np


f=h5py.File('foo.hdf5','w')
temperature=np.random.random(1024)
f['/a']=temperature
f.name
print(f.keys())
print(f['a'])
f.close