from typing import Optional

import requests

from utils import catch_exception


class YaSchedule:
    base_url: str = "https://api.rasp.yandex-net.ru/v3.0"

    def __init__(self, api_key: str, api_key_geo: str) -> None:
        if not api_key:
            raise ValueError("Апи ключ не может быть None")

        self.api_key = api_key
        self.api_key_geo = api_key_geo

    def _make_api_request(self, method: str, params: dict[str, str]) -> dict:
        request_url = self.base_url + f"/{method}/"
        method_params = params.copy()
        method_params["apikey"] = self.api_key

        response = requests.get(url=request_url, params=method_params)
        response.raise_for_status()
        return response.json()


    def __get_city_coordinates(self, city_name: str) -> tuple[str, str]:
        request_url = "http://api.openweathermap.org/geo/1.0/direct"

        params = {
            "q": city_name,
            "appid": self.api_key_geo,
        }

        res = requests.get(url=request_url, params=params)
        res.raise_for_status()
        res = res.json()

        if len(res) == 0:
            raise ValueError("Введен не корректный город!")

        return str(res[0].get("lat")), str(res[0].get("lon"))

    def _get_city_info(self, lat: str, lng: str) -> dict:
        params = {
            "lat": lat,
            "lng": lng,
        }

        return self._make_api_request(
            method="nearest_settlement",
            params=params,
        )

    @catch_exception("Получение расписания")
    def get_schedule(
        self,
        city_from: str,
        city_to: str,
        date: str = "",
        transport_types: str = "",
        transfers: bool = False,
    ) -> Optional[dict]:
        from_lat, from_lng = self.__get_city_coordinates(city_from)
        to_lat, to_lng = self.__get_city_coordinates(city_to)

        from_code: str = self._get_city_info(from_lat, from_lng).get("code")
        to_code: str = self._get_city_info(to_lat, to_lng).get("code")

        params = {
            "from": from_code,
            "to": to_code,
        }
        if date:
            params["date"] = date

        if transport_types:
            params["transport_types"] = transport_types

        if transfers:
            params["transfers"] = "false" if not transfers else "true"

        return self._make_api_request(
            method="search",
            params=params,
        )
    

    @catch_exception("Получение станций города")
    def get_city_stations(self, city_name: str) -> Optional[list[dict]]:
        lat, lng = self.__get_city_coordinates(city_name)

        params = {
            "lat": lat,
            "lng": lng,
            "distance": 15,
            "lang": "ru_RU",
        }

        response = self._make_api_request(
            method="nearest_stations",
            params=params,
        )

        return response.get("stations", [])