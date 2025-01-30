import numpy as np


class Vector(np.ndarray):
    def __new__(cls, data):

        obj = np.asarray(data)

        # remove all dimensions of size 1
        # shape (1,3,1) -> (3,)
        obj = obj.squeeze()
        
        if obj.ndim != 1:
            raise ValueError(f"A Vector must be a 1D array, got {obj.ndim}D.")            

        return obj.view(cls)
