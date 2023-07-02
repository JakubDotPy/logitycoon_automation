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

    @staticmethod
    def read_freight_ids(self) -> list[int]:
        raise NotImplementedError()

    @staticmethod
    def create_freights(self) -> None:
        raise NotImplementedError()

    @staticmethod
    def get_step_delay(self) -> None:
        raise NotImplementedError()

    @staticmethod
    def car_count(self) -> int:
        raise NotImplementedError()

    def __str__(self):
        return f'{self.__class__.__name__}'
