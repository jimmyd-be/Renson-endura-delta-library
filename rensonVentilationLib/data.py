import requests
import logging

from datetime import datetime
from rensonVentilationLib.fieldEnum import FieldEnum
from rensonVentilationLib.generalEnum import Quality, ManualLevel

_LOGGER = logging.getLogger(__name__)


class RensonData:
    data_url = "http://[host]/JSON/ModifiedItems?wsn=150324488709"

    all_data_cache = None
    last_cache_refresh = None
    host = None

    def __init__(self, host: str):
        self.host = host

    def __get_all_data(self):
        if self.last_cache_refresh is None or self.last_cache_refresh + datetime.timedelta(0, 60) > datetime.now():
            response = requests.get(self.data_url.replace("[host]", self.host))

            if response.status_code == 200:
                self.all_data_cache = response.json()
                self.last_cache_refresh = datetime.now()
                return self.all_data_cache
            else:
                _LOGGER.error(f"Error communicating with API: {response.status_code}")

    def __get_field_value(self, all_data, fieldname: str) -> str:
        """Search for the field in the Reson JSON and return the value of it."""
        for data in all_data["ModifiedItems"]:
            if data["Name"] == fieldname:
                return data["Value"]

    def get_data_numeric(self, field: FieldEnum) -> float:
        all_data = self.__get_all_data()
        return round(float(self.__get_field_value(all_data, field.name)))

    def get_data_string(self, field: FieldEnum) -> str:
        all_data = self.__get_all_data()
        return self.__get_field_value(all_data, field.name)

    def get_data_level(self, field: FieldEnum) -> ManualLevel:
        all_data = self.__get_all_data()
        return ManualLevel[self.__get_field_value(all_data, field.name).split()[-1].upper()]

    def get_data_boolean(self, field: FieldEnum) -> bool:
        all_data = self.__get_all_data()
        return bool(int(self.__get_field_value(all_data, field.name)))

    def get_data_quality(self, field: FieldEnum) -> Quality:
        all_data = self.__get_all_data()
        value = round(float(self.__get_field_value(all_data, field.name)))
        if value < 950:
            return Quality.GOOD
        elif value < 1500:
            return Quality.POOR
        else:
            return Quality.BAD
