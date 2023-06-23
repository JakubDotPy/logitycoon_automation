import datetime
import functools
import logging
import random
import re
import time
from dataclasses import dataclass
from enum import Flag
from enum import auto

from requests_html import HTMLSession

from config import AJAX_URL
from config import ENV
from config import setup_logging

setup_logging()
log = logging.getLogger(__name__)


def random_delay(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(random.randint(5, 10) // 10)
        return func(*args, **kwargs)

    return wrapper


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
    session: HTMLSession
    state: FreightState = FreightState.ACCEPTED

    next_state_command = {
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

    def request_next_state(self):
        log.info(f'transitioning from {self.state}')
        if command := self.next_state_command.get(self.state):
            self._push_the_button(command)
        self.state = next(self.state_gen)
        log.debug(f'now in {self.state}')

    @random_delay
    def _push_the_button(self, command):
        r = self.session.get(
            f"{AJAX_URL}{command}.php",
            params={'f': self._id, 'token': self.session.user_token}
        )

    def start_loading(self) -> None:
        self._push_the_button(self.next_state_command[FreightState.ACCEPTED])

    def drive(self) -> None:
        self._push_the_button(self.next_state_command[FreightState.LOADED])

    def unload(self) -> None:
        self._push_the_button(self.next_state_command[FreightState.ARRIVED])

    def finish(self) -> None:
        self._push_the_button(self.next_state_command[FreightState.UNLOADED])

    @staticmethod
    def state_generator():
        yield from FreightState

    def _assign_employee(self):
        r = self.session.get(
            f"{AJAX_URL}freight_autowhemployee.php",
            params={'n': self._id, 'token': self.session.user_token}
        )

    def _assign_truck(self):
        r = self.session.get(
            f"{AJAX_URL}freight_autotruck.php",
            params={'n': self._id, 'token': self.session.user_token}
        )

    def _assign_trailer(self):
        r = self.session.get(
            f"{AJAX_URL}freight_autotrailer.php",
            params={'n': self._id, 'token': self.session.user_token}
        )

    @random_delay
    def assign_assets(self):
        log.info(f'assigning assets to freight {self._id}')
        self._assign_employee()
        self._assign_truck()
        self._assign_trailer()


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
    def __init__(self):
        # session details
        self.session = HTMLSession()
        self.session.user_token = self.token = None  # session will carry token for further use
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

        # game details
        self.active_freights: list[Freight] = []

        log.debug('agent prepared')

    def _load_token(self) -> None:
        log.info('getting token')
        freight_id = self.active_freights[0]._id
        r = self.session.get(f'https://www.logitycoon.com/eu1/index.php?a=freight&n={freight_id}')
        self.token = self.session.user_token = int(re.findall(r'token: "(\d+)"', r.text)[0])

    def get_trip_id(self) -> int:
        log.info('choosing best trip')
        r = self.session.get('https://www.logitycoon.com/eu1/index.php?a=trips')
        row = r.html.find('input[name="freight[]"]')
        return int(row[0].attrs['value'])

    def accept_trip(self, trip_id: int) -> None:
        """Accept the trip by ID.

        Performs a post request.
        """
        log.info(f'accepting trip {trip_id}')
        self.session.post(f"{AJAX_URL}trip_accept.php", data={'freight[]': trip_id})

    def _read_freight_ids(self) -> list[int]:
        r = self.session.get('https://www.logitycoon.com/eu1/index.php?a=warehouse')
        rows = r.html.find('table:first-of-type tr[onclick]')
        return list(map(int, (re.findall(r'\d+', row.attrs['onclick'])[0] for row in rows)))

    def create_freights(self) -> None:
        self.active_freights = [
            Freight(num, self.session)
            for num in self._read_freight_ids()
        ]
        self._load_token()

    @property
    def car_count(self) -> int:
        # NOTE: so far only counts the number of cars
        r = self.session.get('https://www.logitycoon.com/eu1/index.php?a=garage')
        return len(r.html.find('.mt-action-details')) // 2


def main() -> int:
    log.info(' START '.center(80, '='))

    lt = LTAgent()

    best_trip_id = lt.get_trip_id()
    for _ in range(lt.car_count):
        lt.accept_trip(best_trip_id)

    lt.create_freights()

    for freight in lt.active_freights:
        freight.assign_assets()
        # TODO: go through freight stages
        freight.start_loading()

    # NOTE: find a way to make this async maybe

    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    raise SystemExit(main())
