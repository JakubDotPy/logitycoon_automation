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

    def read_freights(self) -> list[int]:
        return [random.randint(100, 200) for _ in range(10)]

    def read_truck_ids(self) -> list[int]:
        return [random.randint(100, 200) for _ in range(10)]

    def refuel(self, truck, source_code: str = '') -> None:
        log.debug(f'got {source_code=}')
        return None

    def get_step_delay(self) -> int:
        raise NotImplementedError()