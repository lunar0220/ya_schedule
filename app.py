from datetime import datetime
from typing import Optional

from utils import catch_exception
from ya_schedule import YaSchedule


class Application:
    def __init__(self, api_key: str, api_key_geo: str) -> None:
        self.schedule_api = YaSchedule(api_key=api_key, api_key_geo=api_key_geo)

    @staticmethod
    def show_menu() -> None:
        print("1. Посмотреть расписание")
        print("2. Посмотреть станции города")
        print("3. Выход")

    @catch_exception("Ввод информации о рейсах с пересадками")
    def __input_transfers(self) -> Optional[str]:
        transfers_input = input("Включать маршруты с пересадками? (д/н): ")
        if transfers_input not in ("yes", "no", "y", "n", "д", "да", "н", "нет"):
            raise ValueError("Нужно ввести один из вариантов (д/н)")
        return transfers_input

    @catch_exception("Ввод инофрмации о городе")
    def __input_city(self, city_type: str) -> Optional[str]:
        city = input(f"Введите город {city_type}: ")
        if not city:
            raise ValueError(f"Необходимо ввести город {city_type}")
        return city

    @catch_exception("Ввод информации о типе транспорта")
    def __input_transport_type(self) -> Optional[tuple[str, bool]]:
        transport_type = input("Введите тип транспорта: ")
        if transport_type not in [
            "plane",
            "bus",
            "train",
            "suburban",
            "water",
            "helicopter",
            "",
            None,
        ]:
            raise ValueError(
                "Тип траспорта может быть одним из этих - plane, bus, train, suburban, water, helicopter, либо пустая строка"
            )
        return transport_type, True

    @catch_exception("Ввод информации о дате")
    def __input_date(self) -> Optional[tuple[str, bool]]:
        date = input("Введите дату отправления (YYYY-MM-DD): ")
        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except Exception:
                raise ValueError("Введенная дата не соответствует формату (YYYY-MM-DD)")
        return date, True

    def __get_schedule(self) -> Optional[dict]:
        city_from = self.__input_city(city_type="отправления")
        while not city_from:
            city_from = self.__input_city("отправления")

        city_to = self.__input_city(city_type="назначения")
        while not city_to:
            city_to = self.__input_city("назначения")

        date = self.__input_date()
        while not date:
            date = self.__input_date()

        transport_type = self.__input_transport_type()
        while not transport_type:
            transport_type = self.__input_transport_type()

        transfers_input = self.__input_transfers()
        while not transfers_input:
            transfers_input = self.__input_transfers()

        transfers = False
        if (
            transfers_input == "д"
            or transfers_input == "да"
            or transfers_input == "y"
            or transfers_input == "yes"
        ):
            transfers = True

        return self.schedule_api.get_schedule(
            city_from=city_from,
            city_to=city_to,
            date=date[0],
            transport_types=transport_type[0],
            transfers=transfers,
        )

    def __show_schedule(self, schedule_info: Optional[dict]) -> None:
        if not schedule_info:
            print("Не удалось получить расписание. Попробуйте снова.")
            return

        counter = 1
        for sch in schedule_info.get("segments", []):
            print(
                f"{counter}. {sch.get('thread').get('title')} - {sch.get('thread').get('number')}"
            )
            print(
                f"\t{sch.get('thread').get('transport_type')} - {sch.get('thread').get('vehicle')}"
            )
            print(f"\t{sch.get('departure')} - {sch.get('arrival')}")
            print()
            counter += 1

    def show_city_stations(self) -> None:
        city = self.__input_city(city_type="для просмотра станций")
        while not city:
            city = self.__input_city("для просмотра станций")

        stations = self.schedule_api.get_city_stations(city_name=city)
        if not stations:
            print("Не удалось получить список станций. Попробуйте снова.")
            return

        print(f"\nСтанции города {city}:")
        print("-" * 50)


        for i, station in enumerate(stations, start=1):
            title = station.get("title", "Неизвестно")
            station_type = station.get("station_type", "—")
            transport = station.get("transport_type", "—")

            print(f"{i}. {title}")
            print(f"   Тип станции: {station_type}")
            print(f"   Вид транспорта: {transport}")
            print()



    def run(self) -> None:
            while True:
                self.show_menu()
                try:
                    choice = int(input())
                except ValueError:
                    print("Введите номер пункта меню")
                    continue

                if choice == 1:
                    print("Просмотр расписания (реализовано ранее)")
                elif choice == 2:
                    self.show_city_stations()
                elif choice == 3:
                    print("Выход")
                    return
                else:
                    print("Такого пункта меню нет")