import datetime
import logging
from dataclasses import dataclass
from enum import Flag
from enum import auto

from config import setup_logging

setup_logging()
log = logging.getLogger(__name__)


class FreightState(Flag):
    ACCEPTED = auto()
    LOADING = auto()
    LOADED = auto()
    DRIVING = auto()
    ARRIVED = auto()
    UNLOADING = auto()
    UNLOADED = auto()
    FINISHING = auto()

    TRANSITION = (
            LOADING
            | DRIVING
            | UNLOADING
            | FINISHING
    )


@dataclass
class Freight:
    _id: int
    state: FreightState = FreightState.ACCEPTED

    next_state_url = {
        FreightState.ACCEPTED: 'freight_loading',
        FreightState.LOADED  : 'freight_driving',
        FreightState.ARRIVED : 'freight_unloading',
        FreightState.UNLOADED: 'freight_finish',
    }

    def __post_init__(self):
        self.state_gen = self.state_generator()

    def __iter__(self):
        return self

    def __next__(self):
        if self.state == FreightState.FINISHING:
            raise StopIteration

        state = next(self.state_gen)
        url = self.next_state_url[state]
        self.request_next_state(url)

    def request_next_state(self, url):
        log.info(f'transitioning from {self.state}')
        log.debug(f'here be request with {url}')
        self.state = next(self.state_gen)
        log.debug(f'now in {self.state}')

    @staticmethod
    def state_generator():
        yield from FreightState


@dataclass
class Employee:
    name: str
    hired: datetime.date
    salary: int
    age: int
    location: str
    freight: Freight
    awake: float


class DrivingLicense(Flag):
    DEFAULT = auto()
    CONTAINER = auto()
    TIPPER = auto()
    COOLED = auto()
    LIQUID = auto()
    LOW = auto()
    CHEMICAL = auto()
    RADIOACTIVE = auto()
    HEAVY = auto()


class Trucker(Employee):
    driving_license: DrivingLicense
    damage_risk: float


class WarehouseMan(Employee):
    pass


class Accountant(Employee):
    pass


class HRManager(Employee):
    pass


class Manager(Employee):
    pass


class TechnicalManager(Employee):
    pass


def main() -> int:
    log.info(' START '.center(80, '='))

    f = Freight(123456)

    for _ in f:
        pass

    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    raise SystemExit(main())
