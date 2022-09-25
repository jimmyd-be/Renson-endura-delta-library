"""File that contain all generic enums."""
from enum import Enum


class ExtendedEnum(Enum):
    """Special enum for creating list of it."""

    @classmethod
    def list(cls):
        """Get list of all values in the enum."""
        return list(map(lambda c: c.value, cls))


class Quality(ExtendedEnum):
    """Enum with all quality values."""

    GOOD = "good"
    POOR = "poor"
    BAD = "bad"


class ManualLevel(ExtendedEnum):
    """Enum with all level values for manual setup."""

    OFF = "Off"
    LEVEL1 = "Level1"
    LEVEL2 = "Level2"
    LEVEL3 = "Level3"
    LEVEL4 = "Level4"
    BREEZE = "Breeze"


class TimerLevel(ExtendedEnum):
    """Enum with all timer levels."""

    LEVEL1 = "Level1"
    LEVEL2 = "Level2"
    LEVEL3 = "Level3"
    LEVEL4 = "Level4"
    HOLIDAY = "Holiday"
    BREEZE = "Breeze"


class DataType(ExtendedEnum):
    """Enum with all data types the library can return."""

    NUMERIC = "numeric"
    STRING = "string"
    LEVEL = "level"
    QUALITY = "quality"
    BOOLEAN = "boolean"


class ServiceNames(ExtendedEnum):
    """All the service fields of the Renson ventilation unit."""

    SET_MANUAL_LEVEL_FIELD = "Manual level"
    TIME_AND_DATE_FIELD = "Date and time"
    TIMER_FIELD = "Ventilation timer"
    BREEZE_TEMPERATURE_FIELD = "Breeze activation temperature"
    BREEZE_ENABLE_FIELD = "Breeze enable"
    BREEZE_LEVEL_FIELD = "Breeze level"
    DAYTIME_FIELD = "Start daytime"
    NIGHTTIME_FIELD = "Start night-time"
    DAY_POLLUTION_FIELD = "Day pollution-triggered ventilation level"
    NIGHT_POLLUTION_FIELD = "Night pollution-triggered ventilation level"
    HUMIDITY_CONTROL_FIELD = "Trigger internal pollution alert on RH"
    AIR_QUALITY_CONTROL_FIELD = "Trigger internal pollution alert on IAQ"
    CO2_CONTROL_FIELD = "Trigger internal pollution alert on CO2"
    CO2_THRESHOLD_FIELD = "CO2 threshold"
    CO2_HYSTERESIS_FIELD = "CO2 hysteresis"
    FILTER_DAYS_FIELD = "Filter preset time"
