import datetime

import requests
import logging
import json

from rensonVentilationLib.generalEnum import ManualLevel, ServiceNames, TimerLevel

_LOGGER = logging.getLogger(__name__)
RENSON_API_URL = "http://[host]/JSON/Vars/[field]?index0=0&index1=0&index2=0"


class ValueData:
    """Class for getting Renson data."""

    def __init__(self, value):
        """Construct the class."""
        self.Value = value


def get_url(host: str, field: ServiceNames):
    """Make the full url of the Renson API and return it."""

    return RENSON_API_URL.replace("[host]", host).replace(
        "[field]", field.value.replace(" ", "%20")
    )


def set_manual_level(host: str, level: ManualLevel):
    data = ValueData(level.value)

    r = requests.post(
        get_url(host, ServiceNames.SET_MANUAL_LEVEL_FIELD), data=json.dumps(data.__dict__)
    )

    if r.status_code != 200:
        _LOGGER.error("Ventilation unit did not return 200")


def sync_time(host: str):
    response = requests.get(get_url(host, ServiceNames.TIME_AND_DATE_FIELD))

    if response.status_code == 200:
        json_result = response.json()
        device_time = datetime.datetime.strptime(
            json_result["Value"], "%d %b %Y %H:%M"
        )
        current_time = datetime.datetime.now()

        if current_time != device_time:
            data = ValueData(current_time.strftime("%d %b %Y %H:%M").lower())
            requests.post(
                get_url(host, ServiceNames.TIME_AND_DATE_FIELD), data=json.dumps(data.__dict__)
            )
    else:
        _LOGGER.error("Ventilation unit did not return 200")


def set_timer_level(host: str, level: TimerLevel, time: int):
    data = ValueData(str(time) + " min " + level)
    r = requests.post(get_url(host, ServiceNames.TIMER_FIELD), data=json.dumps(data.__dict__))

    if r.status_code != 200:
        _LOGGER.error("Ventilation unit did not return 200")


def set_breeze(host: str, level: ManualLevel, temperature: int, activated: bool):
    data = ValueData(level)
    r = requests.post(
        get_url(host, ServiceNames.BREEZE_LEVEL_FIELD), data=json.dumps(data.__dict__)
    )

    if r.status_code != 200:
        _LOGGER.error("Ventilation unit did not return 200")

    data = ValueData(str(temperature))
    r = requests.post(
        get_url(host, ServiceNames.BREEZE_TEMPERATURE_FIELD), data=json.dumps(data.__dict__)
    )

    if r.status_code != 200:
        _LOGGER.error("Ventilation unit did not return 200")

    data = ValueData(str(int(activated)))
    r = requests.post(
        get_url(host, ServiceNames.BREEZE_ENABLE_FIELD), data=json.dumps(data.__dict__)
    )

    if r.status_code != 200:
        _LOGGER.error("Ventilation unit did not return 200")


def set_time(host: str, day: str, night: str):
    data = ValueData(day)
    r = requests.post(get_url(host, ServiceNames.DAYTIME_FIELD), data=json.dumps(data.__dict__))

    if r.status_code != 200:
        _LOGGER.error("Start daytime cannot be set")

    data = ValueData(night)
    r = requests.post(get_url(host, ServiceNames.NIGTHTIME_FIELD), data=json.dumps(data.__dict__))

    if r.status_code != 200:
        _LOGGER.error("Start nighttime cannot be set")


def set_pollution(host: str, day: ManualLevel, night: ManualLevel, humidity_control: bool,
                  airquality_control: bool,
                  co2_control: bool, co2_threshold: bool, co2_hysteresis: bool):
    data = ValueData(day.value)
    r = requests.post(
        get_url(host, ServiceNames.DAY_POLLUTION_FIELD), data=json.dumps(data.__dict__)
    )

    if r.status_code != 200:
        _LOGGER.error("Ventilation unit did not return 200")

    data = ValueData(night.value)
    r = requests.post(
        get_url(host, ServiceNames.NIGHT_POLLUTION_FIELD), data=json.dumps(data.__dict__)
    )

    if r.status_code != 200:
        _LOGGER.error("Ventilation unit did not return 200")

    data = ValueData(str(int(humidity_control)))
    r = requests.post(
        get_url(host, ServiceNames.HUMIDITY_CONTROL_FIELD), data=json.dumps(data.__dict__)
    )

    if r.status_code != 200:
        _LOGGER.error("Ventilation unit did not return 200")

    data = ValueData(str(int(airquality_control)))
    r = requests.post(
        get_url(host, ServiceNames.AIR_QUALITY_CONTROL_FIELD), data=json.dumps(data.__dict__)
    )

    if r.status_code != 200:
        _LOGGER.error("Ventilation unit did not return 200")

    data = ValueData(str(int(co2_control)))
    r = requests.post(
        get_url(host, ServiceNames.CO2_CONTROL_FIELD), data=json.dumps(data.__dict__)
    )

    if r.status_code != 200:
        _LOGGER.error("Ventilation unit did not return 200")

    data = ValueData(str(int(co2_threshold)))
    r = requests.post(
        get_url(host, ServiceNames.CO2_THRESHOLD_FIELD), data=json.dumps(data.__dict__)
    )

    if r.status_code != 200:
        _LOGGER.error("Ventilation unit did not return 200")

    data = ValueData(str(int(co2_hysteresis)))
    r = requests.post(
        get_url(host, ServiceNames.CO2_HYSTERESIS_FIELD), data=json.dumps(data.__dict__)
    )

    if r.status_code != 200:
        _LOGGER.error("Ventilation unit did not return 200")


def set_filter_days(host: str, days: int):
    data = ValueData(str(int(days)))
    r = requests.post(
        get_url(host, ServiceNames.FILTER_DAYS_FIELD), data=json.dumps(data.__dict__)
    )

    if r.status_code != 200:
        _LOGGER.error("Ventilation unit did not return 200")
