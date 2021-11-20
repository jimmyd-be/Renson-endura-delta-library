"""Enum of all the possible fields that can be read."""
from renson_endura_delta.general_enum import DataType


class FieldEnum:
    """Enum of all the possible fields that can be read."""

    name: str = None
    field_type: DataType = None

    def __init__(self, name: str, field_type: DataType):
        """Create enum with values name and field type."""
        self.name = name
        self.field_type = field_type


FIRMWARE_VERSION = FieldEnum("Firmware version", DataType.STRING)
CO2_QUALITY_FIELD = FieldEnum("CO2", DataType.QUALITY)
AIR_QUALITY_FIELD = FieldEnum("IAQ", DataType.QUALITY)
CO2_FIELD = FieldEnum("CO2", DataType.NUMERIC)
AIR_FIELD = FieldEnum("IAQ", DataType.NUMERIC)
CURRENT_LEVEL_FIELD = FieldEnum("Current ventilation level", DataType.LEVEL)
CURRENT_AIRFLOW_EXTRACT_FIELD = FieldEnum("Current ETA airflow", DataType.NUMERIC)
CURRENT_AIRFLOW_INGOING_FIELD = FieldEnum("Current SUP airflow", DataType.NUMERIC)
OUTDOOR_TEMP_FIELD = FieldEnum("T21", DataType.NUMERIC)
INDOOR_TEMP_FIELD = FieldEnum("T11", DataType.NUMERIC)
FILTER_REMAIN_FIELD = FieldEnum("Filter remaining time", DataType.NUMERIC)
HUMIDITY_FIELD = FieldEnum("RH11", DataType.NUMERIC)
FROST_PROTECTION_FIELD = FieldEnum("Frost protection active", DataType.BOOLEAN)
MANUAL_LEVEL_FIELD = FieldEnum("Manual level", DataType.STRING)
TIME_AND_DATE_FIELD = FieldEnum("Date and time", DataType.STRING)
BREEZE_TEMPERATURE_FIELD = FieldEnum("Breeze activation temperature", DataType.NUMERIC)
BREEZE_ENABLE_FIELD = FieldEnum("Breeze enable", DataType.BOOLEAN)
BREEZE_LEVEL_FIELD = FieldEnum("Breeze level", DataType.STRING)
DAYTIME_FIELD = FieldEnum("Start daytime", DataType.STRING)
NIGHTTIME_FIELD = FieldEnum("Start night-time", DataType.STRING)
DAY_POLLUTION_FIELD = FieldEnum("Day pollution-triggered ventilation level", DataType.STRING)
NIGHT_POLLUTION_FIELD = FieldEnum("Night pollution-triggered ventilation level", DataType.STRING)
HUMIDITY_CONTROL_FIELD = FieldEnum("Trigger internal pollution alert on RH", DataType.BOOLEAN)
AIR_QUALITY_CONTROL_FIELD = FieldEnum("Trigger internal pollution alert on IAQ", DataType.BOOLEAN)
CO2_CONTROL_FIELD = FieldEnum("Trigger internal pollution alert on CO2", DataType.BOOLEAN)
CO2_THRESHOLD_FIELD = FieldEnum("CO2 threshold", DataType.NUMERIC)
CO2_HYSTERESIS_FIELD = FieldEnum("CO2 hysteresis", DataType.NUMERIC)
BREEZE_MET_FIELD = FieldEnum("Breeze conditions met", DataType.BOOLEAN)
PREHEATER_FIELD = FieldEnum("Preheater enabled", DataType.BOOLEAN)
BYPASS_TEMPERATURE_FIELD = FieldEnum("Bypass activation temperature", DataType.NUMERIC)
BYPASS_LEVEL_FIELD = FieldEnum("Bypass level", DataType.STRING)
FILTER_PRESET_FIELD = FieldEnum("Filter preset time", DataType.NUMERIC)
