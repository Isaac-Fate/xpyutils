import unittest
import random
from xpyutils import lazy_property

class BasePerson:
    
    def __init__(self, name: str) -> None:
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name

class LazyPropertyTestCase(unittest.TestCase):
    
    def test_lazy_property(self):
        
        class Person(BasePerson):
            
            def __init__(self, name: str) -> None:
                super().__init__(name)
                
            @lazy_property
            def lucky_number(self) -> int:
                return random.randint(0, 100)
            
            @lucky_number.setter
            def lucky_number(self, new_number: int):
                self._lucky_number = new_number
        
        p = Person("Isaac")
        self.assertEqual(p.name, "Isaac")
        
        random.seed(42)
        self.assertEqual(p.lucky_number, 81)
        
        p.lucky_number = 100
        self.assertEqual(p.lucky_number, 100)

    def test_get_presence_required_lazy_property(self):
        
        class Person(BasePerson):
            
            def __init__(self, name: str) -> None:
                super().__init__(name)
                
            @lazy_property.require_presence()
            def lucky_number(self) -> int:
                return random.randint(0, 100)
        
        p = Person("Isaac")
        self.assertEqual(p.name, "Isaac")
        
        try:
            p.lucky_number
        except Exception as e:
            self.assertEqual(
                str(e), 
                "property 'lucky_number' is not present yet"
            )

    def test_cannot_set_presence_required_lazy_property(self):
        
        class Person(BasePerson):
            
            def __init__(self, name: str) -> None:
                super().__init__(name)
                
            @lazy_property.require_presence()
            def name(self) -> str:
                return self._name
        
        p = Person('Isaac')
        self.assertEqual(p.name, 'Isaac')
        
        try:
            p.name = 'Albert'
        except Exception as e:
            self.assertEqual(
                str(e), 
                "setting 'name' is not allowed"
            )

    def test_can_set_presence_required_lazy_property(self):
        
        class Person(BasePerson):
            
            def __init__(self, name: str) -> None:
                super().__init__(name)
                
            @lazy_property.require_presence()
            def name(self) -> str:
                return self._name
            
            @name.setter
            def name(self, new_name: str) -> None:
                self._name = new_name
        
        p = Person('Isaac')
        self.assertEqual(p.name, 'Isaac')
      
        p.name = 'Albert'
        self.assertEqual(p.name, 'Albert')
        self.assertDictEqual(
            p.__dict__,
            dict(
                _name='Albert'
            )
        )
    
    def test_get_presence_required_lazy_property_with_warning(self):
        
        class Person(BasePerson):
            
            def __init__(self, name: str) -> None:
                super().__init__(name)
            
            @lazy_property.with_default_value_when_missing(
                default_value=-1,
                warning_message='the lucky number is not present yet'
            )
            def lucky_number(self) -> int:
                return random.randint(0, 100)
        
        p = Person('Isaac')
        self.assertEqual(p.name, 'Isaac')
        
        self.assertEqual(p.lucky_number, -1)
        
        self.assertEqual(
            p.__dict__,
            dict(
                _name='Isaac',
                _lucky_number=-1
            )
        )

if __name__ == '__main__':
    unittest.main()