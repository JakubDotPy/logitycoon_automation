import logging
from dataclasses import Field
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

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

    fuel_source: ClassVar[dict[str, str]] = {
        'public'     : '',
        'corporation': 'c',
        'fuel_tank'  : 'ft',
    }

    def refuel(self, source: str = 'public') -> None:
        log.debug(f'{self._id} refueling')
        r = self.session.get(
            f"{AJAX_URL}fuelstation_refuel{self.fuel_source[source]}.php",
            params={'x': self._id, 'p': 1, 'returnfr': 0}
        )
        # a=fuelstation & f=14 & p=1 & returnfr=0

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
