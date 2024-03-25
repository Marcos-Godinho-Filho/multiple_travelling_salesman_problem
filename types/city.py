from dataclasses import dataclass


@dataclass
class City:
    id: int
    x: int
    y: int
    
    
    def __lt__(self, other):
        return self.id < other.id


    def __eq__(self, other):
        return self.id == other.id