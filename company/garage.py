import logging
from dataclasses import dataclass

from requests_html import HTMLSession

from config import AJAX_URL

log = logging.getLogger(__name__)


@dataclass
class Truck:
    _id: int
    session: HTMLSession

    def refuel(self) -> None:
        log.debug(f'{self._id} refueling')
        r = self.session.get(
            f"{AJAX_URL}fuelstation_refuel.php",
            params={'x': self._id, 'p': 1, 'returnfr': 0}
        )

@dataclass
class Trailer:
    pass


@dataclass
class Tire:
    pass
