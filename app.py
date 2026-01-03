from typing import Optional
from ya_schedule import YaSchedule

class Application:
    def __init__(self, api_key: str, api_key_geo: str) -> None:
        self.schedule_api = YaSchedule(api_key=api_key, api_key_geo=api_key_geo)
   
   
    @staticmethod
    def _show_menu(self) -> None:
        print("1. Посмортреть расписание")
        print("2. Выход")


def __get_schedual(self, ) -> dict:

    city_from = input("Введите город отправления: ")
    if not city_from:
        print("Необходимо ввести город отправления")
        return
    

    city_to = input("Введите город назначения: ")
    if not city_to:
        print("Необходимо ввести город следования")
        return

    date = input("Введите дату отправления: (YYYY-MM-DD) ")
    transport_type = input("Введите тип транспорта: ")
    transfers_input = input("Включать маршруты с пересадкой? (д/н): ")
    
    transfers = False
    if transfers_input not in ("yes", "no", "y", "n", "да", "нет", "д", "н"):
        raise ValueError("Нужно ввести один из варинатов(д/н)")

    if transfers_input == "д" or transfers_input == "да" or transfers_input == "y" or transfers_input == "yes":
        transfers = True


    return self.schedule_api.get_schedule(
        city_from=city_from,
        city_to=city_to,
        date=date,
        transport_types=transport_type,
        transfers=transfers,
    )


def __show_schedule(self, schedule_info: Optional[dict]) -> None:
    if not schedule_info:
        print("Не удалось получить расписание. Попробуйте снова.")
        return
    

    counter = 1
    for sch in schedule_info.get("segments", []):
        print(f"{counter}. {sch.get("thread").get('title')} - {sch.get('thread').get('number')}")
        print(f"\t{sch.get("thread").get("transport_type")} - {sch.get("thread").get("vehicle")}")
        print(f"\t{sch.get("departure")} - {sch.get("arrival")}")
        print()
        counter += 1


    def run(self):
        while True:
            Application.show_menu()

            user_input = int(input())

            if user_input == 1:
                self.__show_schedule(self.__get_schedule())


            elif user_input == 3:
                break