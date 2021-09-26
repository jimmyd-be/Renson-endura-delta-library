"""Main class of the Renson ventilation library."""
import datetime
import json
import logging
from datetime import datetime
from cachetools import cached, TTLCache


import requests

from rensonVentilationLib.fieldEnum import FieldEnum, FIRMWARE_VERSION, CO2_FIELD
from rensonVentilationLib.generalEnum import (ManualLevel, Quality,
                                              ServiceNames, TimerLevel, DataType)

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

    host = None

    def __init__(self, host: str):
        """Initialize Renson Ventilation class by giving the host name or ip address."""
        self.host = host

    def connect(self) -> bool:
        try:
            response = requests.get(self.data_url.replace("[host]", self.host))

            return response.status_code == 200
        except:
            return False

    @cached(cache=TTLCache(maxsize=1024, ttl=60))
    def __get_all_data(self):
        response = requests.get(self.data_url.replace("[host]", self.host))

        if response.status_code == 200:
            return response.json()
        else:
            _LOGGER.error(f"Error communicating with API: {response.status_code}")

    def __get_field_value(self, all_data, fieldname: str) -> str:
        """Search for the field in the Reson JSON and return the value of it."""
        for data in all_data["ModifiedItems"]:
            if data["Name"] == fieldname:
                return data["Value"]

    def __get_service_url(self, field: ServiceNames):
        """Make the full url of the Renson API and return it."""
        return self.service_url.replace("[host]", self.host).replace(
            "[field]", field.value.replace(" ", "%20")
        )

    def get_data_numeric(self, field: FieldEnum) -> float:
        """Get the value of the field and convert it to a numeric type."""

        if field.field_type is not DataType.NUMERIC:
            raise ValueError("Field is not of type numeric")

        all_data = self.__get_all_data()
        return round(float(self.__get_field_value(all_data, field.name)))

    def get_data_string(self, field: FieldEnum) -> str:
        """Get the raw value of the field and convert it to a string type."""
        all_data = self.__get_all_data()
        return self.__get_field_value(all_data, field.name)

    def get_data_level(self, field: FieldEnum) -> ManualLevel:
        """Get the value of the field and convert it to a ManualLevel type."""
        if field.field_type is not DataType.LEVEL:
            raise ValueError("Field is not of type level")

        all_data = self.__get_all_data()
        return ManualLevel[self.__get_field_value(all_data, field.name).split()[-1].upper()]

    def get_data_boolean(self, field: FieldEnum) -> bool:
        """Get the value of the field and convert it to a boolean type."""
        if field.field_type is not DataType.BOOLEAN:
            raise ValueError("Field is not of type boolean")

        all_data = self.__get_all_data()
        return bool(int(self.__get_field_value(all_data, field.name)))

    def get_data_quality(self, field: FieldEnum) -> Quality:
        """Get the value of the field and convert it to a Quality type."""
        if field.field_type is not DataType.QUALITY:
            raise ValueError("Field is not of type quality")

        all_data = self.__get_all_data()
        value = round(float(self.__get_field_value(all_data, field.name)))
        if value < 950:
            return Quality.GOOD
        elif value < 1500:
            return Quality.POOR
        else:
            return Quality.BAD

    def set_manual_level(self, level: ManualLevel):
        """Set the manual level of the Renson unit. When set to 'Off' the unit will go back to auto program."""
        data = ValueData(level.value)

        r = requests.post(
            self.__get_service_url(ServiceNames.SET_MANUAL_LEVEL_FIELD), data=json.dumps(data.__dict__)
        )

        if r.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

    def sync_time(self):
        """Sync time of the Renson unit to current date and time."""
        response = requests.get(self.__get_service_url(ServiceNames.TIME_AND_DATE_FIELD))

        if response.status_code == 200:
            json_result = response.json()
            device_time = datetime.datetime.strptime(
                json_result["Value"], "%d %b %Y %H:%M"
            )
            current_time = datetime.datetime.now()

            if current_time != device_time:
                data = ValueData(current_time.strftime("%d %b %Y %H:%M").lower())
                requests.post(
                    self.__get_service_url(ServiceNames.TIME_AND_DATE_FIELD), data=json.dumps(data.__dict__)
                )
        else:
            _LOGGER.error("Ventilation unit did not return 200")

    def set_timer_level(self, level: TimerLevel, time: int):
        """Set a level for a specific time (in minutes)."""
        data = ValueData(str(time) + " min " + level)
        r = requests.post(self.__get_service_url(ServiceNames.TIMER_FIELD), data=json.dumps(data.__dict__))

        if r.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

    def set_breeze(self, level: ManualLevel, temperature: int, activated: bool):
        """Activate/deactivate breeze feature and give breeze parameters to the function."""
        data = ValueData(level)
        r = requests.post(
            self.__get_service_url(ServiceNames.BREEZE_LEVEL_FIELD), data=json.dumps(data.__dict__)
        )

        if r.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(temperature))
        r = requests.post(
            self.__get_service_url(ServiceNames.BREEZE_TEMPERATURE_FIELD), data=json.dumps(data.__dict__)
        )

        if r.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(int(activated)))
        r = requests.post(
            self.__get_service_url(ServiceNames.BREEZE_ENABLE_FIELD), data=json.dumps(data.__dict__)
        )

        if r.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

    def set_time(self, day: str, night: str):
        """Set day and night time for the device."""
        data = ValueData(day)
        r = requests.post(self.__get_service_url(ServiceNames.DAYTIME_FIELD), data=json.dumps(data.__dict__))

        if r.status_code != 200:
            _LOGGER.error("Start daytime cannot be set")

        data = ValueData(night)
        r = requests.post(self.__get_service_url(ServiceNames.NIGTHTIME_FIELD), data=json.dumps(data.__dict__))

        if r.status_code != 200:
            _LOGGER.error("Start nighttime cannot be set")

    def set_pollution(self, day: ManualLevel, night: ManualLevel, humidity_control: bool,
                      airquality_control: bool,
                      co2_control: bool, co2_threshold: bool, co2_hysteresis: bool):
        """Enable/disable special auto features of the Renson unit."""
        data = ValueData(day.value)
        r = requests.post(
            self.__get_service_url(ServiceNames.DAY_POLLUTION_FIELD), data=json.dumps(data.__dict__)
        )

        if r.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(night.value)
        r = requests.post(
            self.__get_service_url(ServiceNames.NIGHT_POLLUTION_FIELD), data=json.dumps(data.__dict__)
        )

        if r.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(int(humidity_control)))
        r = requests.post(
            self.__get_service_url(ServiceNames.HUMIDITY_CONTROL_FIELD), data=json.dumps(data.__dict__)
        )

        if r.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(int(airquality_control)))
        r = requests.post(
            self.__get_service_url(ServiceNames.AIR_QUALITY_CONTROL_FIELD), data=json.dumps(data.__dict__)
        )

        if r.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(int(co2_control)))
        r = requests.post(
            self.__get_service_url(ServiceNames.CO2_CONTROL_FIELD), data=json.dumps(data.__dict__)
        )

        if r.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(int(co2_threshold)))
        r = requests.post(
            self.__get_service_url(ServiceNames.CO2_THRESHOLD_FIELD), data=json.dumps(data.__dict__)
        )

        if r.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

        data = ValueData(str(int(co2_hysteresis)))
        r = requests.post(
            self.__get_service_url(ServiceNames.CO2_HYSTERESIS_FIELD), data=json.dumps(data.__dict__)
        )

        if r.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

    def set_filter_days(self, days: int):
        """Set the filter days."""
        data = ValueData(str(int(days)))
        r = requests.post(
            self.__get_service_url(ServiceNames.FILTER_DAYS_FIELD), data=json.dumps(data.__dict__)
        )

        if r.status_code != 200:
            _LOGGER.error("Ventilation unit did not return 200")

    def is_firmware_up_to_date(self) -> bool:
        """Check if the Renson firmware is up to date."""
        version = self.get_data_string(FIRMWARE_VERSION).split()[-1]
        json_string = '{"a":"check", "name":"D_' + version + '.fuf"}'

        response_server = requests.post(self.firmware_server_url, data=json_string)
        if response_server.status_code == 200:
            return bool((response_server.json())["latest"])

        return False
