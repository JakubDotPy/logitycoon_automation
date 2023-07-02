import enum
import logging
from dataclasses import dataclass

from requests_html import HTMLSession

from config import AJAX_URL
from utils import random_delay

log = logging.getLogger(__name__)


class FreightState(enum.Flag):
    ACCEPTED = enum.auto()
    LOADING = enum.auto()
    LOADED = enum.auto()
    DRIVING = enum.auto()
    ARRIVED = enum.auto()
    UNLOADING = enum.auto()
    UNLOADED = enum.auto()
    FINISHING = enum.auto()

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
        return r.status_code, r.text

    def start_loading(self) -> None:
        log.info(f'{self._id} - loading')
        return self._push_the_button(self.next_state_command[FreightState.ACCEPTED])

    def drive(self) -> None:
        log.info(f'{self._id} - driving')
        return self._push_the_button(self.next_state_command[FreightState.LOADED])

    def continue_driving(self) -> tuple[int, str]:
        log.info(f'{self._id} - continue driving')
        return self._push_the_button('freight_continue')

    def unload(self) -> None:
        log.info(f'{self._id} - unloading')
        return self._push_the_button(self.next_state_command[FreightState.ARRIVED])

    def finish(self) -> None:
        log.info(f'{self._id} - finishing')
        return self._push_the_button(self.next_state_command[FreightState.UNLOADED])

    @staticmethod
    def state_generator():
        yield from FreightState

    def _assign_employee(self):
        log.debug(f'{self._id} assigning employees')
        r = self.session.get(
            f"{AJAX_URL}freight_autowhemployee.php",
            params={'n': self._id, 'token': self.session.user_token}
        )

    def _assign_truck(self):
        log.debug(f'{self._id} assigning truck')
        r = self.session.get(
            f"{AJAX_URL}freight_autotruck.php",
            params={'n': self._id, 'token': self.session.user_token}
        )

    def _assign_trailer(self):
        log.debug(f'{self._id} assigning trailer')
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
