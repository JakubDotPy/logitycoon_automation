import logging

from config import setup_logging
from interfaces import Interface
from interfaces import WebInterface

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
        log.info('playing')


def main() -> int:
    interface = WebInterface()
    with Game(interface=interface) as g:
        g.play()
    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    raise SystemExit(main())
