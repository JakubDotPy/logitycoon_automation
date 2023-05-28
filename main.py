import datetime
import logging
from dataclasses import dataclass
from enum import Flag
from enum import auto

from requests_html import HTMLSession

from config import ENV
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
        FreightState.LOADED: 'freight_driving',
        FreightState.ARRIVED: 'freight_unloading',
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


class LTAgent:
    def __init__(self, token):
        self.token = token
        self.session = HTMLSession()
        self.session.headers.update({
            "Accept": "*/*",
            "Accept-Encoding": "br,deflate,gzip,x-gzip",
            "Accept-Language": "cs,en;q=0.9,sk;q=0.8",
            "Dnt": "1",
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        })
        self.session.headers.update({'Cookie': ENV['LT_COOKIE']})
        log.debug('agent prepared')

    def accept_trip(self, trip_id):
        r = self.session.get(
            "https://www.logitycoon.com/eu1/ajax/trip_accept.php",
            params={'freight[]': 335656596},
        )
        print(r.text)

    def _assign_employee(self, freight_n):
        r = self.session.get(
            "https://www.logitycoon.com/eu1/ajax/freight_autowhemployee.php",
            params={'n': freight_n, 'token': self.token}
        )

    def _assign_truck(self, freight_n):
        r = self.session.get(
            "https://www.logitycoon.com/eu1/ajax/freight_autotruck.php",
            params={'n': freight_n, 'token': self.token}
        )

    def _assign_trailer(self, freight_n):
        r = self.session.get(
            "https://www.logitycoon.com/eu1/ajax/freight_autotrailer.php",
            params={'n': freight_n, 'token': self.token}
        )

    def assign_to_freight(self, freight_n):
        self._assign_employee(freight_n)
        self._assign_truck(freight_n)
        self._assign_trailer(freight_n)


def main() -> int:
    log.info(' START '.center(80, '='))

    lt = LTAgent(token=465104375)
    lt.accept_trip(335656596)

    # lt._assign_employee(27520371)

    lt.assign_to_freight(27520371)

    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    raise SystemExit(main())
