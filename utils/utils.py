import random


class Utils:
    def __init__(self):
        pass

    def rand_hex(self):
        pass
    def _chkarg(a):
        if isinstance(a, int): # clamp to range 0--255
            if a < 0:
                a = 0
            elif a > 255:
                a = 255
            elif isinstance(a, float): # clamp to range 0.0--1.0 and convert to integer 0--255
                if a < 0.0:
                    a = 0
                elif a > 1.0:
                    a = 255
                else:
                    a = int(round(a*255))
                else:
                    raise ValueError('Arguments must be integers or floats.')
                    return a