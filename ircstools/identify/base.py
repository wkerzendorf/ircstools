from collections import namedtuple
import numpy as np
from astropy.io import fits

class IRCSType(object):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
    def __repr__(self):
        return "<{0} type={1}>".format(self.fname, self.type)

def identify(fname):
    """
    Parameters
    ----------
    """
    
    if fits.getval(fname, 'data-typ').lower() == 'flat':
        state = 'on' if fits.getval(fname, 'object').lower().endswith('_on') else 'off'
        return IRCSType(type='flat', fname=fname, state=state, lamp=None)
    else:
        return IRCSType(type='unknown', fname=fname)

class DataSet(object):
    
    def __init__(self, fname_list):
        self.all_data_set = map(identify, fname_list)

    @property
    def flat_on(self):
        return filter(lambda it: it.type == 'flat' and it.state == 'on', 
                        self.all_data_set)
    
    @property
    def flat_off(self):
        return filter(lambda it: it.type == 'flat' and it.state == 'off', 
                        self.all_data_set)

    @property
    def science_object(self):
        pass
    
def make_master_flat(data_set):
    combined_on = np.median([fits.getdata(item.fname) for item in data_set.flat_on], axis=0)
    combined_off = np.median([fits.getdata(item.fname) for item in data_set.flat_off], axis=0)
    master_flat = combined_on - combined_off
    return master_flat
        
        
### old make flat code ###
"""
from glob import glob

flat_on = []
flat_off = []
for fname in glob('*.fits'):
    if fits.getval(fname, 'object') == 'EC_K+(0.15)_OFF':
        flat_off.append(fname)
    elif fits.getval(fname, 'object') == 'EC_K+(0.15)_ON':
        flat_on.append(fname)
    else:
        print fname, 'no flat'
        continue
        

mask = np.ones_like(master_flat).astype(bool)
mask[1:510:4] = False

mask[:,:512] = mask[:,:512] & (master_flat[:,:512] > 1.0*1674)
mask[:,512:] = mask[:,512:] & (master_flat[:,512:] > 0.3*1674)


norm_master_flat = master_flat / np.median(master_flat[mask])
"""





