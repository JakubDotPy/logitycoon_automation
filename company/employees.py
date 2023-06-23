"""All "living" assets of the company."""

import datetime
import enum
import logging
from dataclasses import dataclass

log = logging.getLogger(__name__)


@dataclass
class Employee:
    name: str
    hired: datetime.date
    salary: int
    age: int
    location: str
    freight: Freight
    awake: float


class DrivingLicense(enum.Flag):
    DEFAULT = enum.auto()
    CONTAINER = enum.auto()
    TIPPER = enum.auto()
    COOLED = enum.auto()
    LIQUID = enum.auto()
    LOW = enum.auto()
    CHEMICAL = enum.auto()
    RADIOACTIVE = enum.auto()
    HEAVY = enum.auto()


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
