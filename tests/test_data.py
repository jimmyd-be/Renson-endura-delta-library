import requests_mock

import pytest
from renson_endura_delta.field_enum import (CO2_FIELD, CURRENT_LEVEL_FIELD,
                                            FROST_PROTECTION_FIELD,
                                            MANUAL_LEVEL_FIELD, CURRENT_AIRFLOW_EXTRACT_FIELD, CO2_QUALITY_FIELD)
from renson_endura_delta.general_enum import ManualLevel, Quality
from renson_endura_delta.renson import RensonVentilation

responseText: str = '{"ModifiedItems":[{"Name":"Device type","Index":[0,0,0],"Value":"ED 330 T2\/B2 L SHT IAQ CO2 ' \
                    'W02"},{"Name":"MAC","Index":[0,0,0],"Value":"11:22:AA:BC:B2:45"},{"Name":"Warranty number",' \
                    '"Index":[0,0,0],"Value":"test"},{"Name":"Registration key","Index":[0,0,0],"Value":"F2685FEC"},' \
                    '{"Name":"Firmware version","Index":[0,0,0],"Value":"Endura Delta 0.0.67"},{"Name":"Hardware ' \
                    'version","Index":[0,0,0],"Value":"7"},{"Name":"Device name","Index":[0,0,0],"Value":"Endura ' \
                    'Delta"},{"Name":"Static IP Address","Index":[0,0,0],"Value":"192.168.0.45"},{"Name":"Static ' \
                    'subnet mask","Index":[0,0,0],"Value":"255.255.255.0"},{"Name":"Static gateway address",' \
                    '"Index":[0,0,0],"Value":"192.168.0.1"},{"Name":"DHCP Enabled","Index":[0,0,0],"Value":"1"},' \
                    '{"Name":"Week program points per day","Index":[0,0,0],"Value":"2"},{"Name":"Week program points ' \
                    'per day","Index":[0,0,1],"Value":"2"},{"Name":"Week program points per day","Index":[0,0,2],' \
                    '"Value":"2"},{"Name":"Week program points per day","Index":[0,0,3],"Value":"2"},{"Name":"Week ' \
                    'program points per day","Index":[0,0,4],"Value":"2"},{"Name":"Week program points per day",' \
                    '"Index":[0,0,5],"Value":"2"},{"Name":"Week program points per day","Index":[0,0,6],"Value":"2"},' \
                    '{"Name":"Week program time","Index":[0,0,0],"Value":"7:00"},{"Name":"Week program time",' \
                    '"Index":[0,0,1],"Value":"22:00"},{"Name":"Week program time","Index":[0,0,2],"Value":"0:00"},' \
                    '{"Name":"Week program time","Index":[0,0,3],"Value":"0:00"},{"Name":"Week program time",' \
                    '"Index":[0,0,4],"Value":"0:00"},{"Name":"Week program time","Index":[0,0,5],"Value":"0:00"},' \
                    '{"Name":"Week program time","Index":[0,1,0],"Value":"7:00"},{"Name":"Week program time",' \
                    '"Index":[0,1,1],"Value":"22:00"},{"Name":"Week program time","Index":[0,1,2],"Value":"0:00"},' \
                    '{"Name":"Week program time","Index":[0,1,3],"Value":"0:00"},{"Name":"Week program time",' \
                    '"Index":[0,1,4],"Value":"0:00"},{"Name":"Week program time","Index":[0,1,5],"Value":"0:00"},' \
                    '{"Name":"Week program time","Index":[0,2,0],"Value":"7:00"},{"Name":"Week program time",' \
                    '"Index":[0,2,1],"Value":"22:00"},{"Name":"Week program time","Index":[0,2,2],"Value":"0:00"},' \
                    '{"Name":"Week program time","Index":[0,2,3],"Value":"0:00"},{"Name":"Week program time",' \
                    '"Index":[0,2,4],"Value":"0:00"},{"Name":"Week program time","Index":[0,2,5],"Value":"0:00"},' \
                    '{"Name":"Week program time","Index":[0,3,0],"Value":"7:00"},{"Name":"Week program time",' \
                    '"Index":[0,3,1],"Value":"22:00"},{"Name":"Week program time","Index":[0,3,2],"Value":"0:00"},' \
                    '{"Name":"Week program time","Index":[0,3,3],"Value":"0:00"},{"Name":"Week program time",' \
                    '"Index":[0,3,4],"Value":"0:00"},{"Name":"Week program time","Index":[0,3,5],"Value":"0:00"},' \
                    '{"Name":"Week program time","Index":[0,4,0],"Value":"7:00"},{"Name":"Week program time",' \
                    '"Index":[0,4,1],"Value":"22:00"},{"Name":"Week program time","Index":[0,4,2],"Value":"0:00"},' \
                    '{"Name":"Week program time","Index":[0,4,3],"Value":"0:00"},{"Name":"Week program time",' \
                    '"Index":[0,4,4],"Value":"0:00"},{"Name":"Week program time","Index":[0,4,5],"Value":"0:00"},' \
                    '{"Name":"Week program time","Index":[0,5,0],"Value":"7:00"},{"Name":"Week program time",' \
                    '"Index":[0,5,1],"Value":"22:00"},{"Name":"Week program time","Index":[0,5,2],"Value":"0:00"},' \
                    '{"Name":"Week program time","Index":[0,5,3],"Value":"0:00"},{"Name":"Week program time",' \
                    '"Index":[0,5,4],"Value":"0:00"},{"Name":"Week program time","Index":[0,5,5],"Value":"0:00"},' \
                    '{"Name":"Week program time","Index":[0,6,0],"Value":"7:00"},{"Name":"Week program time",' \
                    '"Index":[0,6,1],"Value":"22:00"},{"Name":"Week program time","Index":[0,6,2],"Value":"0:00"},' \
                    '{"Name":"Week program time","Index":[0,6,3],"Value":"0:00"},{"Name":"Week program time",' \
                    '"Index":[0,6,4],"Value":"0:00"},{"Name":"Week program time","Index":[0,6,5],"Value":"0:00"},' \
                    '{"Name":"Week program level","Index":[0,0,0],"Value":"Level2"},{"Name":"Week program level",' \
                    '"Index":[0,0,1],"Value":"Level1"},{"Name":"Week program level","Index":[0,0,2],' \
                    '"Value":"Level1"},{"Name":"Week program level","Index":[0,0,3],"Value":"Level1"},{"Name":"Week ' \
                    'program level","Index":[0,0,4],"Value":"Level1"},{"Name":"Week program level","Index":[0,0,5],' \
                    '"Value":"Level1"},{"Name":"Week program level","Index":[0,1,0],"Value":"Level2"},{"Name":"Week ' \
                    'program level","Index":[0,1,1],"Value":"Level1"},{"Name":"Week program level","Index":[0,1,2],' \
                    '"Value":"Level1"},{"Name":"Week program level","Index":[0,1,3],"Value":"Level1"},{"Name":"Week ' \
                    'program level","Index":[0,1,4],"Value":"Level1"},{"Name":"Week program level","Index":[0,1,5],' \
                    '"Value":"Level1"},{"Name":"Week program level","Index":[0,2,0],"Value":"Level2"},{"Name":"Week ' \
                    'program level","Index":[0,2,1],"Value":"Level1"},{"Name":"Week program level","Index":[0,2,2],' \
                    '"Value":"Level1"},{"Name":"Week program level","Index":[0,2,3],"Value":"Level1"},{"Name":"Week ' \
                    'program level","Index":[0,2,4],"Value":"Level1"},{"Name":"Week program level","Index":[0,2,5],' \
                    '"Value":"Level1"},{"Name":"Week program level","Index":[0,3,0],"Value":"Level2"},{"Name":"Week ' \
                    'program level","Index":[0,3,1],"Value":"Level1"},{"Name":"Week program level","Index":[0,3,2],' \
                    '"Value":"Level1"},{"Name":"Week program level","Index":[0,3,3],"Value":"Level1"},{"Name":"Week ' \
                    'program level","Index":[0,3,4],"Value":"Level1"},{"Name":"Week program level","Index":[0,3,5],' \
                    '"Value":"Level1"},{"Name":"Week program level","Index":[0,4,0],"Value":"Level2"},{"Name":"Week ' \
                    'program level","Index":[0,4,1],"Value":"Level1"},{"Name":"Week program level","Index":[0,4,2],' \
                    '"Value":"Level1"},{"Name":"Week program level","Index":[0,4,3],"Value":"Level1"},{"Name":"Week ' \
                    'program level","Index":[0,4,4],"Value":"Level1"},{"Name":"Week program level","Index":[0,4,5],' \
                    '"Value":"Level1"},{"Name":"Week program level","Index":[0,5,0],"Value":"Level2"},{"Name":"Week ' \
                    'program level","Index":[0,5,1],"Value":"Level1"},{"Name":"Week program level","Index":[0,5,2],' \
                    '"Value":"Level1"},{"Name":"Week program level","Index":[0,5,3],"Value":"Level1"},{"Name":"Week ' \
                    'program level","Index":[0,5,4],"Value":"Level1"},{"Name":"Week program level","Index":[0,5,5],' \
                    '"Value":"Level1"},{"Name":"Week program level","Index":[0,6,0],"Value":"Level2"},{"Name":"Week ' \
                    'program level","Index":[0,6,1],"Value":"Level1"},{"Name":"Week program level","Index":[0,6,2],' \
                    '"Value":"Level1"},{"Name":"Week program level","Index":[0,6,3],"Value":"Level1"},{"Name":"Week ' \
                    'program level","Index":[0,6,4],"Value":"Level1"},{"Name":"Week program level","Index":[0,6,5],' \
                    '"Value":"Level1"},{"Name":"Date and time","Index":[0,0,0],"Value":"22 aug 2021 13:12"},' \
                    '{"Name":"Current program level","Index":[0,0,0],"Value":"Level2"},{"Name":"Breeze activation ' \
                    'temperature","Index":[0,0,0],"Value":"20"},{"Name":"Breeze conditions met","Index":[0,0,0],' \
                    '"Value":"1"},{"Name":"Breeze enable","Index":[0,0,0],"Value":"0"},{"Name":"QualiSensor error ' \
                    'count","Index":[0,0,0],"Value":"0"},{"Name":"QualiSensor pollution alert","Index":[0,0,0],' \
                    '"Value":"0"},{"Name":"Trigger internal pollution alert on RH","Index":[0,0,0],"Value":"1"},' \
                    '{"Name":"Trigger internal pollution alert on IAQ","Index":[0,0,0],"Value":"1"},{"Name":"Trigger ' \
                    'internal pollution alert on CO2","Index":[0,0,0],"Value":"1"},{"Name":"Internal RH pollution ' \
                    'alert","Index":[0,0,0],"Value":"0"},{"Name":"Internal IAQ pollution alert","Index":[0,0,0],' \
                    '"Value":"1"},{"Name":"Internal CO2 pollution alert","Index":[0,0,0],"Value":"0"},' \
                    '{"Name":"External pollution alert","Index":[0,0,0],"Value":"0"},{"Name":"CO2 threshold",' \
                    '"Index":[0,0,0],"Value":"600"},{"Name":"CO2 hysteresis","Index":[0,0,0],"Value":"100"},' \
                    '{"Name":"Start daytime","Index":[0,0,0],"Value":"7:00"},{"Name":"Start night-time","Index":[0,0,' \
                    '0],"Value":"21:30"},{"Name":"Day pollution-triggered ventilation level","Index":[0,0,0],' \
                    '"Value":"Level3"},{"Name":"Night pollution-triggered ventilation level","Index":[0,0,0],' \
                    '"Value":"Level2"},{"Name":"Current pollution level","Index":[0,0,0],"Value":"Level3"},' \
                    '{"Name":"Ventilation timer","Index":[0,0,0],"Value":"0 min Level4"},{"Name":"Manual level",' \
                    '"Index":[0,0,0],"Value":"Off"},{"Name":"Current ventilation level","Index":[0,0,0],"Value":"Auto ' \
                    'Level3"},{"Name":"Fireplace remaining time","Index":[0,0,0],"Value":"0"},{"Name":"Fireplace ' \
                    'preset time","Index":[0,0,0],"Value":"15"},{"Name":"Fireplace flow delta","Index":[0,0,0],' \
                    '"Value":"30"},{"Name":"Total nominal airflow","Index":[0,0,0],"Value":"340"},{"Name":"Level1 ' \
                    'airflow percentage","Index":[0,0,0],"Value":"25"},{"Name":"Level2 airflow percentage",' \
                    '"Index":[0,0,0],"Value":"50"},{"Name":"Level3 airflow percentage","Index":[0,0,0],"Value":"75"},' \
                    '{"Name":"Level4 airflow percentage","Index":[0,0,0],"Value":"100"},{"Name":"Breeze level",' \
                    '"Index":[0,0,0],"Value":"Level3"},{"Name":"Target SUP airflow","Index":[0,0,0],' \
                    '"Value":"255.000000"},{"Name":"Target ETA airflow","Index":[0,0,0],"Value":"255.000000"},' \
                    '{"Name":"Current SUP airflow","Index":[0,0,0],"Value":"255.000000"},{"Name":"Current ETA ' \
                    'airflow","Index":[0,0,0],"Value":"255.000000"},{"Name":"Measured SUP airflow","Index":[0,0,0],' \
                    '"Value":"255.491486"},{"Name":"Measured ETA airflow","Index":[0,0,0],"Value":"265.873413"},' \
                    '{"Name":"SUP fan active","Index":[0,0,0],"Value":"1"},{"Name":"ETA fan active","Index":[0,0,0],' \
                    '"Value":"1"},{"Name":"Unbalance","Index":[0,0,0],"Value":"0"},{"Name":"T11","Index":[0,0,0],' \
                    '"Value":"23.710419"},{"Name":"RH11","Index":[0,0,0],"Value":"66.509766"},{"Name":"T21",' \
                    '"Index":[0,0,0],"Value":"23.039999"},{"Name":"T21bis","Index":[0,0,0],"Value":"-63.030334"},' \
                    '{"Name":"T22","Index":[0,0,0],"Value":"23.360001"},{"Name":"T12","Index":[0,0,0],' \
                    '"Value":"23.493334"},{"Name":"RH12","Index":[0,0,0],"Value":"67.327538"},{"Name":"IAQ",' \
                    '"Index":[0,0,0],"Value":"2496"},{"Name":"CO2","Index":[0,0,0],"Value":"533"},{"Name":"Bypass ' \
                    'activation temperature","Index":[0,0,0],"Value":"23"},{"Name":"Bypass level","Index":[0,0,0],' \
                    '"Value":"100"},{"Name":"Frost protection active","Index":[0,0,0],"Value":"0"},{"Name":"Preheater ' \
                    'enabled","Index":[0,0,0],"Value":"0"},{"Name":"Preheater power","Index":[0,0,0],"Value":"0"},' \
                    '{"Name":"Filter used time","Index":[0,0,0],"Value":"31"},{"Name":"Filter remaining time",' \
                    '"Index":[0,0,0],"Value":"149"},{"Name":"Filter preset time","Index":[0,0,0],"Value":"180"},' \
                    '{"Name":"Region","Index":[0,0,0],"Value":"Belgium"},{"Name":"Input 1 function","Index":[0,0,0],' \
                    '"Value":"0"},{"Name":"Input 2 function","Index":[0,0,0],"Value":"0"},{"Name":"Input 3 function",' \
                    '"Index":[0,0,0],"Value":"0"},{"Name":"Input 1 value","Index":[0,0,0],"Value":"0"},{"Name":"Input ' \
                    '2 value","Index":[0,0,0],"Value":"0"},{"Name":"Input 3 value","Index":[0,0,0],' \
                    '"Value":"0.000000"},{"Name":"Output 1 function","Index":[0,0,0],"Value":"0"},{"Name":"Output 2 ' \
                    'function","Index":[0,0,0],"Value":"0"},{"Name":"Output 3 function","Index":[0,0,0],"Value":"0"},' \
                    '{"Name":"Output 1 value","Index":[0,0,0],"Value":"0"},{"Name":"Output 2 value","Index":[0,0,0],' \
                    '"Value":"0"},{"Name":"Output 3 value","Index":[0,0,0],"Value":"0.000000"},{"Name":"Registration ' \
                    'complete","Index":[0,0,0],"Value":"1"},{"Name":"Error list","Index":[0,0,0],"Value":""},' \
                    '{"Name":"Error list","Index":[0,0,1],"Value":""},{"Name":"Error list","Index":[0,0,2],' \
                    '"Value":""},{"Name":"Error list","Index":[0,0,3],"Value":""},{"Name":"Error list","Index":[0,0,' \
                    '4],"Value":""},{"Name":"System startup","Index":[0,0,0],"Value":"1"},{"Name":"SD card mounted",' \
                    '"Index":[0,0,0],"Value":"1"},{"Name":"SUP fan voltage","Index":[0,0,0],"Value":"8.697593"},' \
                    '{"Name":"ETA fan voltage","Index":[0,0,0],"Value":"6.807638"},{"Name":"SUP fan speed",' \
                    '"Index":[0,0,0],"Value":"2364"},{"Name":"ETA fan speed","Index":[0,0,0],"Value":"1839"},' \
                    '{"Name":"SUP constant flow sensor value","Index":[0,0,0],"Value":"54.845024"},{"Name":"ETA ' \
                    'constant flow sensor value","Index":[0,0,0],"Value":"35.548702"},{"Name":"SUP flow offset",' \
                    '"Index":[0,0,0],"Value":"0.000000"},{"Name":"ETA flow offset","Index":[0,0,0],' \
                    '"Value":"0.000000"}],"Wsn":34363714635} '


def test_connect_with_connection():
    with requests_mock.Mocker() as mock:
        mock.get("http://example.mock/JSON/ModifiedItems?wsn=150324488709",
              text=responseText)
        data = RensonVentilation("example.mock")

        assert data.connect()


def test_connect_without_connection():
    data = RensonVentilation("example.mock")

    assert not data.connect()


def test_get_data_numeric():
    with requests_mock.Mocker() as mock:
        mock.get("http://example.mock/JSON/ModifiedItems?wsn=150324488709",
              text=responseText)
        data = RensonVentilation("example.mock")
        all_data = data.get_all_data()
        value = data.get_field_value(all_data, CO2_FIELD)

        assert data.parse_numeric(value) == 533


def test_get_data_with_cache():
    with requests_mock.Mocker() as mock:
        mock.get("http://example.mock/JSON/ModifiedItems?wsn=150324488709",
              text=responseText)
        data = RensonVentilation("example.mock")

        all_data = data.get_all_data()
        co2_value = data.get_field_value(all_data, CO2_FIELD)
        current_level_value = data.get_field_value(all_data, CURRENT_LEVEL_FIELD)

        assert data.parse_numeric(co2_value) == 533
        assert data.get_field_value(all_data, MANUAL_LEVEL_FIELD) == "Off"
        assert data.parse_data_level(current_level_value) == ManualLevel.LEVEL3
        assert mock.called
        assert mock.called_once


def test_get_data_string():
    with requests_mock.Mocker() as mock:
        mock.get("http://example.mock/JSON/ModifiedItems?wsn=150324488709",
              text=responseText)
        data = RensonVentilation("example.mock")
        all_data = data.get_all_data()

        assert data.get_field_value(all_data, CURRENT_LEVEL_FIELD) == "Off"


def test_get_data_level():
    with requests_mock.Mocker() as mock:
        mock.get("http://example.mock/JSON/ModifiedItems?wsn=150324488709",
              text=responseText)
        data = RensonVentilation("example.mock")

        all_data = data.get_all_data()
        value = data.get_field_value(all_data, CURRENT_LEVEL_FIELD)

        assert data.parse_data_level(value) == ManualLevel.LEVEL3


def test_get_data_boolean():
    with requests_mock.Mocker() as mock:
        mock.get("http://example.mock/JSON/ModifiedItems?wsn=150324488709",
              text=responseText)
        data = RensonVentilation("example.mock")

        all_data = data.get_all_data()
        value = data.get_field_value(all_data, FROST_PROTECTION_FIELD)

        assert not data.parse_boolean(value)


def test_get_data_quality():
    with requests_mock.Mocker() as mock:
        mock.get("http://example.mock/JSON/ModifiedItems?wsn=150324488709",
              text=responseText)
        data = RensonVentilation("example.mock")

        all_data = data.get_all_data()
        value = data.get_field_value(all_data, CO2_QUALITY_FIELD)

        assert data.parse_quality(value) == Quality.GOOD
