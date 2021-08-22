import aiohttp
import logging

from datetime import datetime
from rensonVentilationLib.fieldEnum import FieldEnum

_LOGGER = logging.getLogger(__name__)


class RensonData:
    data_url = "http://[host]/JSON/ModifiedItems?wsn=150324488709"

    all_data_cache = None
    last_cache_refresh = None

    async def __get_all_data(self, host: str):

        if self.last_cache_refresh is None or self.last_cache_refresh + datetime.timedelta(0, 60) > datetime.now():
            async with aiohttp.ClientSession() as session:
                async with session.get(self.data_url.replace("[host]", host)) as response:

                    if response.status == 200:
                        self.all_data_cache = await response.json()
                        self.last_cache_refresh = datetime.now()
                        return self.all_data_cache
                    else:
                        _LOGGER.error(f"Error communicating with API: {response.status}")

    def __get_field_value(self, all_data, fieldname):
        """Search for the field in the Reson JSON and return the value of it."""
        for data in all_data["ModifiedItems"]:
            if data["Name"] == fieldname:
                return data["Value"]

    def get_data(self, host: str, field: FieldEnum) -> object:
        all_data = self.get_all_data(host)
        return self.get_field_value(all_data, field.name)
