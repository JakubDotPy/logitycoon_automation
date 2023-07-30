from abc import ABC
from abc import abstractmethod


class Interface(ABC):

    # TODO: define methods

    @abstractmethod
    def load_token(self, freight_id: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_trip_id(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def accept_trip(self, trip_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def read_freight_ids(self) -> list[int]:
        raise NotImplementedError()

    @abstractmethod
    def read_truck_ids(self) -> list[int]:
        raise NotImplementedError()

    @abstractmethod
    def refuel(self, truck, source_code: str = '') -> None:
        raise NotImplementedError()

    @abstractmethod
    def create_freights(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_step_delay(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def car_count(self) -> int:
        raise NotImplementedError()

    def __str__(self):
        return f'{self.__class__.__name__}'
