import datetime
import logging
import re
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
    session: HTMLSession
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

    def _assign_employee(self):
        r = self.session.get(
            "https://www.logitycoon.com/eu1/ajax/freight_autowhemployee.php",
            params={'n': self._id, 'token': self.session.user_token}
        )

    def _assign_truck(self):
        r = self.session.get(
            "https://www.logitycoon.com/eu1/ajax/freight_autotruck.php",
            params={'n': self._id, 'token': self.session.user_token}
        )

    def _assign_trailer(self):
        r = self.session.get(
            "https://www.logitycoon.com/eu1/ajax/freight_autotrailer.php",
            params={'n': self._id, 'token': self.session.user_token}
        )

    def assign_freight_assets(self):
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
    def __init__(self, user_token):
        # session details
        self.token = user_token
        self.session = HTMLSession()
        self.session.user_token = user_token  # session will carry token for further use
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
        self.active_freight_ids = set()

        log.debug('agent prepared')

    def get_trip_id(self):
        r = self.session.get('https://www.logitycoon.com/eu1/index.php?a=trips')
        row = r.html.find('input[name="freight[]"]')
        return int(row[0].attrs['value'])

    def accept_trip(self, trip_id):
        r = self.session.get(
            "https://www.logitycoon.com/eu1/ajax/trip_accept.php",
            params={'freight[]': 335656596},
        )
        print(r.text)

    def load_freight_ids(self):
        r = self.session.get('https://www.logitycoon.com/eu1/index.php?a=warehouse')
        rows = r.html.find('table:first-of-type tr[onclick]')
        self.active_freight_ids = set(
            map(int, (re.findall(r'\d+', row.attrs['onclick'])[0] for row in rows))
        )


def main() -> int:
    log.info(' START '.center(80, '='))

    lt = LTAgent(user_token=465104375)

    best_trip_id = lt.get_trip_id()

    # TODO: n times accept best trip

    lt.load_freight_ids()

    # in loop
    # TODO: - create freight
    # TODO: - assign assets
    # TODO: - go through the states

    # fr1 = Freight(27520269, session=lt.session)
    # fr1.assign_freight_assets()
    # fr2 = Freight(27520266, session=lt.session)
    # fr2.assign_freight_assets()

    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    raise SystemExit(main())
