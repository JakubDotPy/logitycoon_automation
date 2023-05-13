import logging

from config import setup_logging


def main() -> int:
    setup_logging()
    log = logging.getLogger(__name__)

    log.info(' START '.center(80, '='))

    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    raise SystemExit(main())
