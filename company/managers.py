import logging

from company.garage import Truck
from company.warehouse import Freight
from interfaces.base import Interface

log = logging.getLogger(__name__)


class FreightManager:

    def __init__(self, interface: Interface):
        self.interface = interface

        # game details
        self.active_freights: list[Freight] = []
        self.trucks: list[Truck] = []

        log.debug('agent prepared')

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
        self.active_freights = [
            Freight(num, self.interface.session)
            for num in self.interface.read_freight_ids()
        ]
        self._load_token(self.active_freights[0]._id)

    def create_trucks(self) -> None:
        self.trucks = [
            Truck(num, self.interface.session)
            for num in self.interface.read_truck_ids()
        ]

    def get_step_delay(self) -> int:
        return self.interface.get_step_delay()

    @property
    def car_count(self) -> int:
        return len(self.trucks)
