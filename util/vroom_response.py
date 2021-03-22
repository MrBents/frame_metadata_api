import json
import os
import pickle
from config import *

class VroomResponse():
    def __init__(self, payload):
        self.payload = payload
        with open(os.path.join(base_path, "cache/coords_to_address_cache.pickle"), "rb") as f:
            self.coords_to_address_cache = pickle.load(f)
    
    def usingAddresses(self):
        return self.recursiveReplace(self.payload)
    
    def getAddress(self, coords):
        try:
            return self.coords_to_address_cache[','.join(str(loc) for loc in coords)]
        except:
            return 'UNKNOWN'
    
    # Recursively replaces coords with addresses.
    # In order to do this efficiently, it uses coords_to_address_cache which is populated
    # whenever an address is added to the main cache in VroomPayloadBuilder.
    def recursiveReplace(self, ledger):
        
        for key, value in ledger.items():
            if type(value) == list and len(value) == 2 and type(value[0]) == float:
                ledger[key] = self.getAddress(value)
            elif type(value) == dict:
                ledger[key] = self.recursiveReplace(value)
            elif type(value) == list and len(value) > 0 and type(value[0]) == dict:
                for i, subdict in enumerate(value):
                    ledger[key][i] = self.recursiveReplace(subdict)
        return ledger

    def getResponseWithCoords(self):
        pass


    