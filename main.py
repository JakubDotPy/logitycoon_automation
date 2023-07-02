import datetime
import functools
import itertools
import logging
import random
import re
import time
from dataclasses import dataclass
from enum import Flag
from enum import auto

from requests_html import HTMLSession

from config import AJAX_URL
from config import CLICK_DELAY_INTERVAL
from config import ENV
from config import setup_logging

setup_logging()
log = logging.getLogger(__name__)


def random_delay(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        delay = random.randint(*CLICK_DELAY_INTERVAL) / 10
        time.sleep(delay)
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
    def _push_the_button(self, command) -> tuple[int, str]:
        r = self.session.get(
            f"{AJAX_URL}{command}.php",
            params={'f': self._id, 'token': self.session.user_token}
        )
        return r.status_code, r.text

    def start_loading(self) -> tuple[int, str]:
        return self._push_the_button(self.next_state_command[FreightState.ACCEPTED])

    def drive(self) -> tuple[int, str]:
        return self._push_the_button(self.next_state_command[FreightState.LOADED])

    def continue_driving(self) -> tuple[int, str]:
        return self._push_the_button('freight_continue')

    def unload(self) -> tuple[int, str]:
        return self._push_the_button(self.next_state_command[FreightState.ARRIVED])

    def finish(self) -> tuple[int, str]:
        return self._push_the_button(self.next_state_command[FreightState.UNLOADED])

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

    def __str__(self):
        return f'Freight {self._id}'


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
        log.debug('getting token')
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

    def get_step_delay(self) -> int:
        """Read the delay before next step can be performed."""

        def to_seconds(text):
            h, m, s = map(int, re.findall('\d+', text))
            return h * 3_600 + m * 60 + s

        r = self.session.get('https://www.logitycoon.com/eu1/index.php?a=warehouse')
        spans = r.html.find('span[id^="ready-noxs"]')
        seconds = [to_seconds(span.text) for span in spans]
        return max(seconds, default=3) + 10  # add som minimal buffer

    @property
    def car_count(self) -> int:
        # NOTE: so far only counts the number of cars
        r = self.session.get('https://www.logitycoon.com/eu1/index.php?a=garage')
        return len(r.html.find('.mt-action-details')) // 2


def accept_and_load() -> None:
    """Accept the best trips, create freights and start loading."""
    log.info(' accept_and_load '.center(40, '='))

    lt = LTAgent()

    best_trip_id = lt.get_trip_id()
    for _ in range(lt.car_count):
        lt.accept_trip(best_trip_id)

    lt.create_freights()

    for freight in lt.active_freights:
        freight.assign_assets()
        freight.start_loading()


def push_green_button() -> None:
    """Go through all freights and press the green button to continue."""

    log.info('-- performing next steps')

    lt = LTAgent()
    lt.create_freights()

    fns = [
        'drive',
        'continue_driving',
        'unload',
        'finish',
    ]

    # bruteforce try all options

    for freight in lt.active_freights:
        log.info(f'processing {freight}')
        for fn_name in fns:
            code, resp_text = getattr(freight, fn_name)()
            if 'setTimeout' in resp_text:
                log.info(f'- {fn_name}')
                continue


def main() -> int:
    log.info(' AUTOMATION '.center(80, '='))
    log.warning('experimental - use at own risk')

    lt = LTAgent()

    fns = [
        'drive',  # 4:10
        'continue_driving',
        'unload',
        'finish',  # 3:41
    ]

    for trip_no in itertools.count(start=1):
        log.info(f' {trip_no:>2}. trip '.center(80, '='))

        best_trip_id = lt.get_trip_id()

        for _ in range(lt.car_count):
            lt.accept_trip(best_trip_id)

        lt.create_freights()

        # accept and load
        for freight in lt.active_freights:
            freight.assign_assets()
            freight.start_loading()

        delay = lt.get_step_delay()
        log.info(f'sleeping {delay} seconds')
        time.sleep(delay)

        # bruteforce try all options
        for fn_name in fns:

            log.info(f'now - {fn_name}')

            # for all freights, try the option
            for freight in lt.active_freights:
                log.info(f'processing {freight}')
                code, resp_text = getattr(freight, fn_name)()

            delay = lt.get_step_delay()
            log.info(f'sleeping {delay} seconds')
            time.sleep(delay)

    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    raise SystemExit(main())
