from __future__ import annotations
from typing import Any, Callable
import warnings
from .base import base_lazy_property

class presence_required_property(base_lazy_property):
    
    def __init__(
            self, 
            get_property: Callable[[Any], Any] | None = None, 
            set_property: Callable[[Any, Any], None] | None = None, 
            delete_property: Callable[[Any], None] | None = None, 
            doc: str | None = None,
            raise_exception_when_missing: bool = True,
            default_value: Any = None,
            warning_message: str | None = None,
            error_message: str | None = None
        ) -> None:
        
        super().__init__(
            get_property, 
            set_property, 
            delete_property, 
            doc
        )
   
        self.raise_exception_when_missing = raise_exception_when_missing
        self.default_value = default_value
        self.warning_message = warning_message
        self.error_message = error_message
    
    def __get__(self, obj, objtype=None):
        
        # return property value if it is present
        if hasattr(obj, self.private_property_name):
            return getattr(obj, self.private_property_name)
        
        # raise exception when the property is missing
        if self.raise_exception_when_missing:
            if self.error_message is not None:
                raise AttributeError(f"{self.error_message}")
            else:
                raise AttributeError(f"property '{self.property_name}' is not present yet")

        # show a warning message instead of raising an expection
        if self.warning_message is not None:
            warnings.warn(self.warning_message)
                
        # set default property value
        setattr(obj, self.private_property_name, self.default_value)
        
        return self.default_value
