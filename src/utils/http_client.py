from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import aiohttp


class HttpClient(ABC):
    @abstractmethod
    async def get(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        pass

    @abstractmethod
    async def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass


class AioHttpClient(HttpClient):
    def __init__(self):
        self.session = None

    async def initialize_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def get(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        await self.initialize_session()

        async with self.session.get(url, headers=headers, params=params) as response:
            return await response.json()

    async def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        await self.initialize_session()

        async with self.session.post(url, data=data, json=json) as response:
            return await response.json()

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()


http_client_instance = AioHttpClient()


def get_http_client() -> HttpClient:
    return http_client_instance
