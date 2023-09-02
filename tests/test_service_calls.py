import requests_mock

from renson_endura_delta.general_enum import Level
from renson_endura_delta.renson import RensonVentilation as Services


def test_set_manual_level():
    with requests_mock.Mocker() as m:
        m.post("http://example.mock/JSON/Vars/Manual%20level?index0=0&index1=0&index2=0",
               text='ok')

        service = Services("example.mock")
        service.set_manual_level(Level.LEVEL2)

        assert m.called


def test_set_filter_days():
    with requests_mock.Mocker() as m:
        m.post("http://example.mock/JSON/Vars/Filter%20preset%20time?index0=0&index1=0&index2=0",
               text="{'Value'='30'}")

        service = Services("example.mock")
        service.set_filter_days(30)

        assert m.called