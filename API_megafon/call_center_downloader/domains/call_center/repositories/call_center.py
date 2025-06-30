from abc import ABC, abstractmethod
from typing import Any, List


class ICallCenterRepository(ABC):
    @abstractmethod
    async def authenticate(self) -> str:
        pass

    @abstractmethod
    async def fetch_object_data(
        self, obj_name: str, time_filter: bool, token: str, limit: int, offset: int
    ) -> tuple[List[dict], int]:
        pass
