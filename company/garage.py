import logging
from dataclasses import dataclass

from requests_html import HTMLSession

from config import AJAX_URL
from config import INDEX_URL
from utils import City
from utils import random_delay

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

    @random_delay
    def transfer(self, city: City = City.PILSEN) -> None:
        """Transfer the truck to the given city (specified by city enum).

        defaults to Pilsen
        """
        log.debug(f'{self._id} transferring to {city.name}')
        r = self.session.post(
            f"{INDEX_URL}",
            params={'a': 'truck_transfer', 't': self._id},
            data={'city': city.value, 'transfer': ''}
        )


@dataclass
class Trailer:
    pass


@dataclass
class Tire:
    pass
