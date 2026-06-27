# entity/PhotoVisibility.py
from enum import Enum, unique

@unique
class PhotoVisibility(Enum):
    PUBLIC = 1
    PRIVATE = 0