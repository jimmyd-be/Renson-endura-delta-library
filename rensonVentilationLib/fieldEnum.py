import enum

from rensonVentilationLib.generalEnum import DataType


class FieldEnum(enum.Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, name, field_type):
        self.name = name
        self.type = field_type

    CO2_FIELD = "CO2", DataType.QUALITY
    AIR_QUALITY_FIELD = "IAQ", DataType.QUALITY
    CURRENT_LEVEL_FIELD = "Current ventilation level", DataType.LEVEL
    CURRENT_AIRFLOW_EXTRACT_FIELD = "Current ETA airflow", DataType.NUMERIC
    CURRENT_AIRFLOW_INGOING_FIELD = "Current SUP airflow", DataType.NUMERIC
    OUTDOOR_TEMP_FIELD = "T21", DataType.NUMERIC
    INDOOR_TEMP_FIELD = "T11", DataType.NUMERIC
    FILTER_REMAIN_FIELD = "Filter remaining time", DataType.NUMERIC
    HUMIDITY_FIELD = "RH11", DataType.NUMERIC
    FROST_PROTECTION_FIELD = "Frost protection active", DataType.BOOLEAN
    MANUAL_LEVEL_FIELD = "Manual level", DataType.STRING
    TIME_AND_DATE_FIELD = "Date and time", DataType.STRING
    BREEZE_TEMPERATURE_FIELD = "Breeze activation temperature", DataType.NUMERIC
    BREEZE_ENABLE_FIELD = "Breeze enable", DataType.BOOLEAN
    BREEZE_LEVEL_FIELD = "Breeze level", DataType.STRING
    DAYTIME_FIELD = "Start daytime", DataType.STRING
    NIGHTTIME_FIELD = "Start night-time", DataType.STRING
    DAY_POLLUTION_FIELD = "Day pollution-triggered ventilation level", DataType.STRING
    NIGHT_POLLUTION_FIELD = "Night pollution-triggered ventilation level", DataType.STRING
    HUMIDITY_CONTROL_FIELD = "Trigger internal pollution alert on RH", DataType.BOOLEAN
    AIR_QUALITY_CONTROL_FIELD = "Trigger internal pollution alert on IAQ", DataType.BOOLEAN
    CO2_CONTROL_FIELD = "Trigger internal pollution alert on CO2", DataType.BOOLEAN
    CO2_THRESHOLD_FIELD = "CO2 threshold", DataType.NUMERIC
    CO2_HYSTERESIS_FIELD = "CO2 hysteresis", DataType.NUMERIC
    BREEZE_MET_FIELD = "Breeze conditions met", DataType.BOOLEAN
    PREHEATER_FIELD = "Preheater enabled", DataType.BOOLEAN
    BYPASS_TEMPERATURE_FIELD = "Bypass activation temperature", DataType.NUMERIC
    BYPASS_LEVEL_FIELD = "Bypass level", DataType.STRING
    FILTER_PRESET_FIELD = "Filter preset time", DataType.NUMERIC
