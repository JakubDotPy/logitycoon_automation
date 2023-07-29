from config import setup_logging

setup_logging()

import logging
from company.managers import GarageManager
from company.managers import FreightManager
from interfaces.web import WebInterface

log = logging.getLogger(__name__)


def refuel_all() -> None:
    """Refuel all trucks."""
    log.info(' refueling trucks '.center(40, '='))

    interface = WebInterface()
    gm = GarageManager(interface)
    gm.create_trucks()

    for num, truck in enumerate(gm.trucks, start=1):
        print(f'{num:->10}')
        gm.refuel(truck, source=None)


def assign_assets() -> None:
    """Assign assets to already accepted trips."""
    log.info(' assign assets '.center(40, '='))

    interface = WebInterface()
    fm = FreightManager(interface)

    fm.create_freights()
    for num, freight in enumerate(fm.active_freights, start=1):
        print(f'{num:->10}')
        freight.assign_assets()
        freight.start_loading()


def accept_and_load() -> None:
    """Accept the best trips, create freights and start loading."""

    log.info(' accept_and_load '.center(40, '='))

    interface = WebInterface()
    fm = FreightManager(interface)
    gm = GarageManager(interface)

    gm.create_trucks()

    best_trip_id = fm.get_trip_id()
    for _ in range(gm.car_count):
        fm.accept_trip(best_trip_id)

    fm.create_freights()

    for num, freight in enumerate(fm.active_freights, start=1):
        print(f'{num:->10}')
        freight.assign_assets()
        freight.start_loading()


def do_next_step() -> None:
    """Go through all freights and press the green button to continue."""

    log.info('-- performing next steps')

    interface = WebInterface()
    fm = FreightManager(interface)
    fm.create_freights()

    for num, freight in enumerate(fm.active_freights, start=1):
        print(f'{num:->10}')
        try:
            next(freight)
        except StopIteration:
            log.info('freight already finished')
