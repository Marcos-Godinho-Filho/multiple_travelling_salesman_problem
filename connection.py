from dataclasses import dataclass
from city import City


@dataclass
class Connection:
    origin: City
    destination: City
    
    
    def __lt__(self, other):
        return self.origin < other.origin

