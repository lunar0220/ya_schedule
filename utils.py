from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional


def catch_exception(desc: str = "") -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Optional[Any]:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                with open("app.log", "a", encoding="utf-8") as file:
                    file.write(
                        f"[{datetime.now()}] Ошибка при вызове {desc} - Функция: {func.__name__} - Текст ошибки: {e}\n"
                    )
                print(e)
                return None

        return wrapper

    return decorator