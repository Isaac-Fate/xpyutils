from __future__ import annotations
from typing import Type

class Singleton(object):
    
    # one and only instance
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        
        # create a new instance if it is None
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        
        # otherwise return the one and only instance
        return cls._instance
    
def singleton(cls: Type) -> Type:
    """A decorator that makes the class to decorate a singleton.

    Parameters
    ----------
        cls (Type): Class to decorate.

    Returns
    -------
        Type: Singleton class.
    """
    
    # set the class attribute _instance as None
    setattr(cls, '_instance', None)

    # the magic __new__ method of 
    # the class to decorate should be 
    # replaced with that of the Singleton class
    cls.__new__ = Singleton.__new__
    
    return cls