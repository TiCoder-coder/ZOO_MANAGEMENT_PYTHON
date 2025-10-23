from enum import Enum

class CustomEnum(Enum):
    @property
    def description(self):
        pass

# Dinh nghia class Gender de khoi tao cac thuoc tinh "Male" va "Female"
class Gender(CustomEnum):
    Male = "Male"
    Female = "Female"

# Dinh nghia class HealthStatus de tao cac thuoc tinh "Healthy", "Sick" va "Quarantined"
class HealthStatus(CustomEnum):
    Healthy = "Healthy"
    Sick = "Sick"
    Quarantined = "Quarantined"

# Dinh nghia class TypeFood de tao cac thuoc tinh "Meat", "Plant", "Fish" va "Insect"
class TypeFood(CustomEnum):
    Meat = "Meat"
    Plant = "Plant"
    Fish = "Fish"
    Insect = "Insect"

# Dinh nghia class Climate de tao cac thuoc tinh "Tropical", "Desert" "Aquatic" va "Temperate" 
class Climate(CustomEnum):
    Tropical = "Tropical"
    Desert = "Desert"
    Aquatic = "Aquatic"
    Temperate = "Temperate"

# Dinh nghia class Role de tao cac thuoc tinh "Staff" va "Manager"
class Role(CustomEnum):
    Staff = "Staff"
    Manager = "Manager"
