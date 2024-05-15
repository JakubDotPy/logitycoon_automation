import itertools
import logging
import time

from company.managers import FreightManager
from config import setup_logging
from interfaces.base import Interface
from interfaces.web import WebInterface

setup_logging()
log = logging.getLogger(__name__)


class Game:

    def __init__(self, interface: Interface):
        log.info(f'initializing game with {interface}')
        self.interface = interface

    def __enter__(self):
        log.info(' START '.center(80, '='))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        log.info(' END '.center(80, '='))

    def play(self):
        log.info(' AUTOMATION '.center(80, '='))
        log.warning('experimental - use at own risk')

        fm = FreightManager(self.interface)

        fns = [
            'drive',  # 4:10
            'continue_driving',
            'unload',
            'finish',  # 3:41
        ]

        for trip_no in itertools.count(start=1):
            log.info(f' {trip_no:>2}. trip '.center(80, '='))

            best_trip_id = fm.get_trip_id()

            for _ in range(fm.car_count):
                fm.accept_trip(best_trip_id)

            fm.create_freights()

            # accept and load
            for freight in fm.active_freights:
                freight.assign_assets()
                freight.start_loading()

            delay = fm.get_step_delay()
            log.info(f'sleeping {delay} seconds')
            time.sleep(delay)

            # bruteforce try all options
            for fn_name in fns:

                log.info(f'now - {fn_name}')

                # for all freights, try the option
                for freight in fm.active_freights:
                    log.info(f'processing {freight}')
                    code, resp_text = getattr(freight, fn_name)()

                delay = fm.get_step_delay()
                log.info(f'sleeping {delay} seconds')
                time.sleep(delay)


def main() -> int:
    interface = WebInterface()
    with Game(interface=interface) as g:
        g.play()
    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from entrypoints import refuel_all
    refuel_all()
    # raise SystemExit(main())
