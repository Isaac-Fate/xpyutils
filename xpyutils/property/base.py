from __future__ import annotations
from typing import Any, Callable

class base_lazy_property(property):
    """Base class of lazy property.
    By decorating a class method with `lazy_property`,
    the user can turn into that method into a managed property.
    The property will be initialized only when it is accessed.
    """
    
    def __init__(
            self, 
            get_property: Callable[[Any], Any] | None = None, 
            set_property: Callable[[Any, Any], None] | None = None, 
            delete_property: Callable[[Any], None] | None = None, 
            doc: str | None = None
        ) -> None:
        """Create a lazy property.

        Parameters
        ----------
            get_property (Callable[[Any], Any] | None, optional): Method to get the property. 
                Defaults to None.
            set_property (Callable[[Any, Any], None] | None, optional):Method to set the property. 
                Defaults to None.
            delete_property (Callable[[Any], None] | None, optional): Method to delete the property. 
                Defaults to None.
            doc (str | None, optional): Docstring of the property. Defaults to None.
        """
        
        super().__init__(
            get_property, 
            set_property, 
            delete_property, 
            doc
        )

    def __set_name__(self, owner, name):

        # property name
        self.property_name = name

        # priavate name is by convention with '_' prefix
        self.private_property_name = f"_{name}"

    def __get__(self, obj, objtype=None):

        # return property value if it is present
        if hasattr(obj, self.private_property_name):
            return getattr(obj, self.private_property_name)

        # calculate property value now
        property_value = self.fget(obj)
        
        # store the property
        setattr(obj, self.private_property_name, property_value)
        
        return property_value
    
    def __set__(self, obj, value):
        
        if self.fset is None:
            raise AttributeError(f"setting '{self.property_name}' is not allowed")
        
        self.fset(obj, value)
