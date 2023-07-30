import logging
import random

from interfaces.base import Interface

log = logging.getLogger(__name__)


class LocalInterface(Interface):
    session = None

    def load_token(self, freight_id: int) -> int:
        raise NotImplementedError()

    def get_trip_id(self) -> int:
        raise NotImplementedError()

    def accept_trip(self, trip_id: int) -> None:
        raise NotImplementedError()

    def read_freight_ids(self) -> list[int]:
        return [random.randint(100, 200) for _ in range(10)]

    def read_truck_ids(self) -> list[int]:
        return [random.randint(100, 200) for _ in range(10)]

    def refuel(self, truck, source_code: str = '') -> None:
        return None

    def create_freights(self) -> None:
        raise NotImplementedError()

    def get_step_delay(self) -> int:
        raise NotImplementedError()

    def car_count(self) -> int:
        raise NotImplementedError()

    def __str__(self):
        return f'{self.__class__.__name__}'
