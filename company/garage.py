import logging
from dataclasses import dataclass

log = logging.getLogger(__name__)


@dataclass
class Truck:
    _id: int


@dataclass
class Trailer:
    pass


@dataclass
class Tire:
    pass
