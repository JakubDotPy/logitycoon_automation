import logging

from company.managers import FreightManager
from config import setup_logging
from interfaces.web import WebInterface
from utils import random_delay

setup_logging()
log = logging.getLogger(__name__)


def refuel_all() -> None:
    """Refuel all trucks."""
    log.info(' refueling trucks '.center(40, '='))

    interface = WebInterface()
    fm = FreightManager(interface)
    fm.create_trucks()

    for truck in fm.trucks:
        random_delay(truck.refuel)()


def assign_assets() -> None:
    """Assign assets to already accepted trips."""
    log.info(' assign assets '.center(40, '='))

    interface = WebInterface()
    fm = FreightManager(interface)

    fm.create_freights()
    for freight in fm.active_freights:
        freight.assign_assets()
        freight.start_loading()


def accept_and_load() -> None:
    """Accept the best trips, create freights and start loading."""

    log.info(' accept_and_load '.center(40, '='))

    interface = WebInterface()
    fm = FreightManager(interface)

    fm.create_trucks()

    best_trip_id = fm.get_trip_id()
    for _ in range(fm.car_count):
        fm.accept_trip(best_trip_id)

    fm.create_freights()

    for freight in fm.active_freights:
        freight.assign_assets()
        freight.start_loading()


def do_next_step() -> None:
    """Go through all freights and press the green button to continue."""

    log.info('-- performing next steps')

    interface = WebInterface()
    fm = FreightManager(interface)
    fm.create_freights()

    fns = [
        'drive',
        'continue_driving',
        'unload',
        'finish',
    ]

    # bruteforce try all options

    for freight in fm.active_freights:
        log.info(f'processing {freight}')
        for fn_name in fns:
            code, resp_text = getattr(freight, fn_name)()
            if 'setTimeout' in resp_text:
                log.info(f'- {fn_name}')
                continue
