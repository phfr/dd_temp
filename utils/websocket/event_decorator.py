import inspect
from functools import wraps
from typing import Any, Callable, Dict

from fastapi import WebSocket


def event_decorator(handlers: Dict[str, Callable], get_client_info: Callable):
    def decorator(event_name: str):
        def wrapper(func: Callable):
            @wraps(func)
            async def inner(data: Dict[Any, Any], websocket: WebSocket):
                client_info = get_client_info(websocket)
                sig = inspect.signature(func)
                params = {
                    param: value
                    for param, value in {
                        "data": data,
                        "websocket": websocket,
                        "client_info": client_info,
                    }.items()
                    if param in sig.parameters
                }
                return await func(**params)

            handlers[event_name] = inner
            return func

        return wrapper

    return decorator
