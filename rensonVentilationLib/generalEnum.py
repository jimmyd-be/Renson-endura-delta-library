from enum import Enum


class ManualLevel(Enum):
    OFF = "Off"
    LEVEL1 = "Level1"
    LEVEL2 = "Level2"
    LEVEL3 = "Level3"
    LEVEL4 = "Level4"


class TimerLevel(Enum):
    LEVEL1 = "Level1"
    LEVEL2 = "Level2"
    LEVEL3 = "Level3"
    LEVEL4 = "Level4"
    HOLIDAY = "Holiday"
    BREEZE = "Breeze"


class DataType(Enum):
    NUMERIC = "numeric"
    STRING = "string"
    LEVEL = "level"
    QUALITY = "quality"
    BOOLEAN = "boolean"
