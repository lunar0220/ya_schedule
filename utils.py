from typing import Callable, Optional, Any
from functools import wraps


def catch_exception(desc: str = "") -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Optional[Any]:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Ошибка при вызове {desc}")
                print(f"Функция - {func.__name__}")
                print(e)
                return None
        return wrapper
    return decorator