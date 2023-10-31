"""Main class of the Renson ventilation library."""
import json
import logging
from datetime import datetime
import re

import requests

from renson_endura_delta.field_enum import FILTER_PRESET_FIELD, FieldEnum, FIRMWARE_VERSION, FIRMWARE_VERSION_FIELD
from renson_endura_delta.general_enum import (Level, Quality,
                                              ServiceNames, DataType, Level)

_LOGGER = logging.getLogger(__name__)


class ValueData:
    """Class for getting Renson data."""

    def __init__(self, value):
        """Construct the class."""
        self.Value = value


class RensonVentilation:
    """Main class to get data and post data to the Renson unit."""

    data_url = "http://[host]/JSON/ModifiedItems?wsn=150324488709"
    service_url = "http://[host]/JSON/Vars/[field]?index0=0&index1=0&index2=0"
    firmware_server_url = "http://www.renson-app.com/endura_delta/firmware/check.php"
    firmware_dowload_url = "http://www.renson-app.com/endura_delta/firmware/files/"

    host = None

    def __init__(self, host: str):
        """Initialize Renson Ventilation class by giving the host name or ip address."""
        self.host = host

    def connect(self) -> bool:
        try:
            response = requests.get(self.data_url.replace("[host]", self.host))

            return response.status_code == 200
        except Exception:
            return False

    def get_all_data(self):
        response = requests.get(self.data_url.replace("[host]", self.host))

        if response.status_code == 200:
            return response.json()
        else:
            _LOGGER.error(f"Error communicating with API: {response.status_code}")
            return ''

    def get_field_value(self, all_data, fieldname: str) -> str:
        """Search for the field in the Reson JSON and return the value of it."""
        for data in all_data["ModifiedItems"]:
            if data["Name"] == fieldname == FIRMWARE_VERSION_FIELD.name:
                return data["Value"].split()[-1]
            elif data["Name"] == fieldname:
                return data["Value"]
        return ''

    def parse_value(self, value, data_type):
        """Parse value to correct type"""
        if data_type == DataType.NUMERIC:
            return self.parse_numeric(value)
        elif data_type == DataType.STRING:
            return value
        elif data_type == DataType.LEVEL:
            return self.parse_data_level(value).value
        elif data_type == DataType.BOOLEAN:
            return self.parse_boolean(value)
        elif data_type == DataType.QUALITY:
            return self.parse_quality(value).value

    def __get_service_url(self, field: ServiceNames):
        """Make the full url of the Renson API and return it."""
        return self.service_url.replace("[host]", self.host).replace(
            "[field]", field.value.replace(" ", "%20")
        )
    
    def __get_base_url(self, path: str):
        """Make the base url of the Renson API and return it."""
        return "http://" + self.host + path
        

    def parse_numeric(self, value: str) -> float:
        """Get the value of the field and convert it to a numeric type."""
        return round(float(value))

    def parse_data_level(self, value: str) -> Level:
        """Get the value of the field and convert it to a Level type."""
        return Level[value.split()[-1].upper()]

    def parse_boolean(self, value: str) -> bool:
        """Get the value of the field and convert it to a boolean type."""
        return bool(int(value))

    def parse_quality(self, value: str) -> Quality:
        """Get the value of the field and convert it to a Quality type."""
        value = round(float(value))
        if value < 950:
            return Quality.GOOD
        elif value < 1500:
            return Quality.POOR
        else:
            return Quality.BAD

    def set_manual_level(self, level: Level):
        """Set the manual level of the Renson unit. When set to 'Off' the unit will go back to auto program."""
        data = ValueData(level.value)

        response = requests.post(
            self.__get_service_url(ServiceNames.SET_MANUAL_LEVEL_FIELD), data=json.dumps(data.__dict__)
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

    def restart_device(self):
        """Restart device"""
        response = requests.post(
            self.__get_base_url("/Reset")
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

    def sync_time(self):
        """Sync time of the Renson unit to current date and time."""
        response = requests.get(self.__get_service_url(ServiceNames.TIME_AND_DATE_FIELD))

        if response.status_code == 200:
            json_result = response.json()
            device_time = datetime.strptime(
                json_result["Value"], "%d %b %Y %H:%M"
            )
            current_time = datetime.now()

            if current_time != device_time:
                data = ValueData(current_time.strftime("%d %b %Y %H:%M").lower())
                requests.post(
                    self.__get_service_url(ServiceNames.TIME_AND_DATE_FIELD), data=json.dumps(data.__dict__)
                )
        else:
            _LOGGER.error("Ventilation unit did not return 200")

    def set_timer_level(self, level: Level, time: int):
        """Set a level for a specific time (in minutes)."""

        if level == Level.OFF:
            raise Exception("Off is not a valid type for setting manual level")

        data = ValueData(str(time) + " min " + level.value)
        response = requests.post(self.__get_service_url(ServiceNames.TIMER_FIELD), data=json.dumps(data.__dict__))

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

    def set_breeze(self, level: Level, temperature: int, activated: bool):
        """Activate/deactivate breeze feature and give breeze parameters to the function."""

        if level == Level.HOLIDAY or level == Level.OFF or level == Level.BREEZE:
            raise Exception("Holiday, Off, Breeze are not a valid types for setting breeze level")

        data = ValueData(level)
        response = requests.post(
            self.__get_service_url(ServiceNames.BREEZE_LEVEL_FIELD), data=json.dumps(data.__dict__)
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(temperature))
        response = requests.post(
            self.__get_service_url(ServiceNames.BREEZE_TEMPERATURE_FIELD), data=json.dumps(data.__dict__)
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(int(activated)))
        response = requests.post(
            self.__get_service_url(ServiceNames.BREEZE_ENABLE_FIELD), data=json.dumps(data.__dict__)
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

    def set_time(self, day: str, night: str):
        """Set day and night time for the device."""
        data = ValueData(day)
        response = requests.post(self.__get_service_url(ServiceNames.DAYTIME_FIELD), data=json.dumps(data.__dict__))

        if response.status_code != 200:
            _LOGGER.error("Start daytime cannot be set")

        data = ValueData(night)
        response = requests.post(self.__get_service_url(ServiceNames.NIGTHTIME_FIELD), data=json.dumps(data.__dict__))

        if response.status_code != 200:
            _LOGGER.error("Start nighttime cannot be set")

    def set_pollution(self, day: Level, night: Level, humidity_control: bool,
                      airquality_control: bool,
                      co2_control: bool, co2_threshold: bool, co2_hysteresis: bool):
        """Enable/disable special auto features of the Renson unit."""

        if day == Level.HOLIDAY or day == Level.OFF or day == Level.BREEZE:
            raise Exception("Holiday, Off, Breeze are not a valid types for setting day level")

        if night == Level.HOLIDAY or night == Level.OFF or night == Level.BREEZE:
            raise Exception("Holiday, Off, Breeze are not a valid types for setting night level")

        data = ValueData(day.value)
        response = requests.post(
            self.__get_service_url(ServiceNames.DAY_POLLUTION_FIELD), data=json.dumps(data.__dict__)
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(night.value)
        response = requests.post(
            self.__get_service_url(ServiceNames.NIGHT_POLLUTION_FIELD), data=json.dumps(data.__dict__)
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(int(humidity_control)))
        response = requests.post(
            self.__get_service_url(ServiceNames.HUMIDITY_CONTROL_FIELD), data=json.dumps(data.__dict__)
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(int(airquality_control)))
        response = requests.post(
            self.__get_service_url(ServiceNames.AIR_QUALITY_CONTROL_FIELD), data=json.dumps(data.__dict__)
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(int(co2_control)))
        response = requests.post(
            self.__get_service_url(ServiceNames.CO2_CONTROL_FIELD), data=json.dumps(data.__dict__)
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(int(co2_threshold)))
        response = requests.post(
            self.__get_service_url(ServiceNames.CO2_THRESHOLD_FIELD), data=json.dumps(data.__dict__)
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(int(co2_hysteresis)))
        response = requests.post(
            self.__get_service_url(ServiceNames.CO2_HYSTERESIS_FIELD), data=json.dumps(data.__dict__)
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

    def set_filter_days(self, days: int):
        """Set the filter days."""
        data = ValueData(str(int(days)))
        response = requests.post(
            self.__get_service_url(ServiceNames.FILTER_DAYS_FIELD), data=json.dumps(data.__dict__)
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

    def set_remaining_filter_days(self, days: int):
        """Set the remaining filter days."""
        data = ValueData(str(int(days)))
        response = requests.post(
            self.__get_service_url(ServiceNames.FILTER_REMAIN_FIELD), data=json.dumps(data.__dict__)
        )

        if response.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

    def is_firmware_up_to_date(self, current_version) -> bool:
        """Check if the Renson firmware is up to date."""
        # version = self.get_field_value(FIRMWARE_VERSION).split()[-1]
        version = current_version.split()[-1]
        json_string = '{"a":"check", "name":"D_' + version + '.fuf"}'

        response_server = requests.post(self.firmware_server_url, data=json_string)
        if response_server.status_code == 200:
            return bool((response_server.json())["latest"])

        return False

    def get_latest_firmware_version(self) -> str:
        """Get the latest Renson firmware version."""
        json_string = '{"a":"check", "name":"D_0.fuf"}'

        response_server = requests.post(self.firmware_server_url, data=json_string)

        if response_server.status_code == 200:
            return re.sub(r"D_(.*)\.fuf", r"\1", response_server.json()["url"])

        return ""
    
    def reset_filter(self):
        """Reset filter timer"""
        data = self.get_all_data()
        filter_preset = self.parse_numeric(self.get_field_value(data, FILTER_PRESET_FIELD.name))
        self.set_remaining_filter_days(filter_preset)
    
    