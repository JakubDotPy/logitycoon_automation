import functools
import logging

from company.garage import Truck
from company.warehouse import Freight
from interfaces.base import Interface
from utils import random_delay

log = logging.getLogger(__name__)


class FreightManager:

    def __init__(self, interface: Interface):
        self.interface = interface

        # game details
        self.active_freights: list[Freight] = []
        self.trucks: list[Truck] = []

        log.debug('freight manager ready')

    def _load_token(self, freight_id: int) -> None:
        log.debug('getting token')
        self.interface.load_token(freight_id=freight_id)

    def get_trip_id(self) -> int:
        log.info('choosing best trip')
        return self.interface.get_trip_id()

    def accept_trip(self, trip_id: int) -> None:
        """Accept the trip by ID.

        Performs a post request.
        """
        log.info(f'accepting trip {trip_id}')
        self.interface.accept_trip(trip_id=trip_id)

    def create_freights(self) -> None:
        log.debug('creating freights')
        self.active_freights = [
            Freight(num, self.interface.session)
            for num in self.interface.read_freight_ids()
        ]
        self._load_token(self.active_freights[0]._id)

    def get_step_delay(self) -> int:
        return self.interface.get_step_delay()


class GarageManager:

    def __init__(self, interface: Interface):
        self.interface = interface

        # game details
        self.trucks: list[Truck] = []

        log.debug('garage manager ready')

    def create_trucks(self) -> None:
        self.trucks = [Truck(num) for num in self.interface.read_truck_ids()]

    def refuel(self, truck, source: str | None = 'public') -> None:

        fuel_source = {
            'fuel_tank': 'ft',
            'corporation': 'c',
            'public': '',
        }

        if source:
            log.debug(f'{truck._id} refueling from {source}')
            self.interface.refuel(truck, source_code='')
            return

        # refuel from all possible sources
        for source_name, source_code in fuel_source.items():
            log.debug(f'{truck._id} refueling from {source_name}')
            # wait between sources
            fn = functools.partial(self.interface.refuel, truck, source_code=None)
            random_delay(fn)()

    @property
    def car_count(self) -> int:
        return len(self.trucks)

