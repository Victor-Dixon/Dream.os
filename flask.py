"""Minimal Flask compatibility layer for tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple


class _RequestContext:
    def __init__(self) -> None:
        self._json: Dict[str, Any] | None = None

    def set_json(self, payload: Dict[str, Any] | None) -> None:
        self._json = payload

    def get_json(self) -> Dict[str, Any] | None:
        return self._json


request = _RequestContext()


@dataclass
class _Response:
    payload: Any
    status_code: int

    def get_json(self) -> Any:
        return self.payload


class Blueprint:
    def __init__(self, name: str, import_name: str, url_prefix: str = "") -> None:
        self.name = name
        self.import_name = import_name
        self.url_prefix = url_prefix
        self.routes: Dict[Tuple[str, str], Callable[..., Any]] = {}

    def route(self, path: str, methods: Optional[List[str]] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        methods = methods or ["GET"]

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            for method in methods:
                self.routes[(self.url_prefix + path, method.upper())] = func
            return func

        return decorator


class Flask:
    def __init__(self, name: str) -> None:
        self.name = name
        self.config: Dict[str, Any] = {}
        self._routes: Dict[Tuple[str, str], Callable[..., Any]] = {}

    def register_blueprint(self, blueprint: Blueprint) -> None:
        self._routes.update(blueprint.routes)

    def test_client(self) -> "_TestClient":
        return _TestClient(self)


class _TestClient:
    def __init__(self, app: Flask) -> None:
        self.app = app

    def __enter__(self) -> "_TestClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def _request(self, method: str, path: str, json: Dict[str, Any] | None = None) -> _Response:
        handler = self.app._routes.get((path, method.upper()))
        if not handler:
            return _Response({"error": "not found"}, 404)
        request.set_json(json)
        result = handler()
        if isinstance(result, tuple):
            payload, status = result
        else:
            payload, status = result, 200
        return _Response(payload, status)

    def get(self, path: str) -> _Response:
        return self._request("GET", path)

    def post(self, path: str, json: Dict[str, Any] | None = None) -> _Response:
        return self._request("POST", path, json=json)


def jsonify(payload: Any) -> Any:
    return payload
