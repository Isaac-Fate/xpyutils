# Extra Python Utilities

🛠️ Ongoing project of extra Python utilities including implementation of lazy property, 
collections of common regular expressions, ...

## Lazy Property

A simple use of `lazy_property`:

```python
from xpyutils import lazy_property

import random
random.seed(42)

class Person:
    
    def __init__(self, name: str) -> None:
        self._name = name
    
    @property
    def name(self) -> str:
        """Name of the person.
        """
        return self._name
    
    @lazy_property
    def lucky_number(self) -> int:
        """Lucky number.
        """
        return random.randint(0, 100)
    
    @lazy_property.require_presence()
    def age(self) -> int:
        """Age.
        """
        return random.randint(20, 30)
    
person = Person('Isaac')

print(person.lucky_number) # 81
print(person.lucky_number) # it is still 81

try: 
    person.age
except Exception as e:
    print(e) # property 'age' is not present yet
```