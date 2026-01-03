import requests

from utils import catch_exception


class YaSchedule:
    base_url: str = "https://api.rasp.yandex-net.ru/v3.0"

    def __init__(self, api_key: str, api_key_geo: str) -> None:
        if not api_key:
            raise ValueError("Апи ключ не может быть None")
        
        self.api_key = api_key
        self.api_key_geo = api_key

    def _make_api_request(
            self, 
            method: str,
            params: dict[str, str]
        ) -> dict:
        request_url = self.base_url + f"/{method}/"
        method_params = params.copy()
        method_params["apikey"] = self.api_key

        return requests.get(
            url=request_url,
            params=method_params,
        ).json()
    
    def _get_city_cor(self, city_name: str) -> tuple[str]:
        request_url = "http://api.openweathemap.org/geo/1.0/direct"


        params = {
            "q": city_name,
            "appid": self.api_key_geo,
        }


        res = requests.get(
            url=request_url,
            params=params,
        ).json()

        if len(res) == 0:
            raise ValueError("Введен не корректный город")


        return str(res[0].get("lat")), str(res[0].get("lon"))
    
    def __get_city_info(self, lat: str, lng: str) -> dict:
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
        ) -> dict:

        from_lat, from_lng = self.__get_city_cor(city_from)
        to_lat, to_lng = self.__get_city_cor(city_to)

        from_code: str = self._get_city_info(from_lat, from_lng).get("code")
        to_code: str = self._get_city_info(to_lat, to_lng).get("code")

        params = {
            "from": from_code,
            "to": to_code,
        }
        if date:
            params["date"] = date

        if transport_types:
            if transport_types not in ["plane", "bus", "train", "suburban", "water", "helicopter"]:
                raise ValueError("Тип траспорта может быть одним из этих - plane, bus, train, suburban, water, helicopter")
            
            params["transport_types"] = "false" if not transfers else "true"

        if transfers:
            params["transfers"] = transfers
        
        return self._make_api_request(
            method="search",
            params=params,
        )