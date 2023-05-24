from __future__ import annotations
from typing import Any, Callable
from functools import partial
from .base import base_lazy_property
from .presence_required import presence_required_property

class lazy_property(base_lazy_property):
    """Lazy property.
    By decorating a class method with `lazy_property`,
    the user can turn into that method into a managed property.
    The property will be initialized only when it is accessed.
    
    Examples
    --------
    ```python
    import random
    random.seed(42)
    
    class Person:
        def __init__(self, name: str) -> None:
            self._name = name
        
        @lazy_property
        def lucky_number(self) -> int:
            return random.randint(0, 100)
    
    p = Person('Isaac')
    print(p.__dict__) # {'_name': 'Isaac'}
    
    print(p.lucky_number) # 81
    print(p.__dict__) # {'_name': 'Isaac', '_lucky_number': 81}
    
    print(p.lucky_number) # 81
    ```
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
    
    @classmethod
    def require_presence(
            cls, 
            error_message: str | None = None
        ) -> partial[presence_required_property]:
        """The property is required to be present when accessed.
        Otherwise, an exception will be raised.

        Parameters
        ----------
            error_message (str | None, optional): Custom error message to display. 
            Defaults to None.

        Returns
        -------
            partial[presence_required_property]: Partially initialized 
            presence required property.
        """
        
        return partial(
            presence_required_property,
            error_message=error_message
        )
    
    @classmethod
    def with_default_value_when_missing(
            cls, 
            default_value: Any,
            warning_message: str | None = None
        ) -> partial[presence_required_property]:
        """If the property is missing when accessed,
        then the default value will be returned,
        and a warning message will be shown.

        Parameters
        ----------
            default_value (Any): Default property value to return.  
            warning_message (str | None, optional): Warning message to display. 
            Defaults to None.

        Returns
        -------
            partial[presence_required_property]: Partially initialized 
            presence required property.
        """
        
        return partial(
            presence_required_property,
            raise_exception_when_missing=False,
            default_value=default_value,
            warning_message=warning_message
        )
        