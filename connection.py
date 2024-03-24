from dataclasses import dataclass
from city import City


@dataclass
class Connection:
    origin: City
    destination: City
