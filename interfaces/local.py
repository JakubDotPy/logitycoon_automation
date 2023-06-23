import logging
import random

from interfaces.base import Interface

log = logging.getLogger(__name__)


class LocalInterface(Interface):

    def accept_trip(self, trip_id: int) -> None:
        pass

    def get_trip_id(self) -> int:
        pass

    def load_token(self, freight_id: int) -> int:
        return random.randint(1_000_000, 9_999_999)
