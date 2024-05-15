import datetime
import itertools
import logging
import re
import time

from config import INDEX_URL
from config import LOGS_DIR
from config import setup_logging
from interfaces.web import WebInterface

LOG_CONF = {
    'version': 1,
    'formatters': {
        'file_form': {
            'format': '%(asctime)s - %(levelname)-8s - %(funcName)-22s - %(message)s'
        },
        'console_form': {
            'format': '%(levelname)-8s - %(message)s'
        },
    },
    'handlers': {
        'console_hand': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'level': 'DEBUG',
            'formatter': 'console_form',
        },
        'file_hand_rot': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / f'fuel_thief.log',
            'maxBytes': 3_145_728,  # 3MB
            'backupCount': 5,  # five files with log backup
            'level': 'DEBUG',
            'encoding': 'utf-8',
            'formatter': 'file_form',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console_hand', 'file_hand_rot'],
            'level': 'DEBUG',
        }
    }
}
setup_logging(LOG_CONF)
log = logging.getLogger(__name__)

log.info(' fuel thief starting '.center(80, '='))

interface = WebInterface()
web = interface.session  # shortcut


# company list
# https://www.logitycoon.com/eu1/index.php?a=companylist&p=30

# specific company cars
# https://www.logitycoon.com/eu1/index.php?a=companyprofile_trucks&x=137544

# steal - POST
# https://www.logitycoon.com/eu1/index.php?a=stealfuel
# truck: 851076

def page_company_ids(page_num: int):
    """finds all company ids on a page"""
    log.info(f'generating companies on page {page_num}')

    r = web.get(INDEX_URL, params={'a': 'companylist', 'p': page_num})
    id_matches = re.findall(
        r'href="index\.php\?a\=companyprofile_overview&x=(\d+)"',
        r.text
    )[::3]  # we need to take every third, because every row has 3 links
    yield from map(int, id_matches)


def company_id_gen(start_page: int = 30, end_page: int = 40):
    log.debug('preparing company id generator')
    yield from itertools.chain.from_iterable(
        page_company_ids(page) for page in range(start_page, end_page)
    )


def company_truck_gen(company_id: int):
    """given company id, yield unprotected truck ids"""
    log.info(f'generating available trucks from company {company_id}')

    r = web.get(INDEX_URL, params={'a': 'companyprofile_trucks', 'x': company_id})
    buttons = r.html.find('.tab-content button:not([disabled])')
    truck_ids = (button.attrs['value'] for button in buttons)
    yield from map(int, truck_ids)


def get_timeout(company_id: int):
    """Look for text: "Stealing fuel is available again at 13-07-2023 18:12." """
    r = web.get(INDEX_URL, params={'a': 'companyprofile_trucks', 'x': company_id})

    pattern = r'Stealing fuel is available again at (\d+-\d+-\d+ \d+:\d+)'
    if match := re.findall(pattern, r.text):
        log.info(f'next possible steal at {match[0]}')
        next_time = datetime.datetime.strptime(match[0], '%d-%m-%Y %H:%M')
        delta = next_time - datetime.datetime.now()
        return delta.seconds
    return 1  # NOTE: by default sleep for 1 seconds between attempts


def steal_fuel(truck_id: int):
    log.info(f'stealing fuel from truck {truck_id}')
    r = web.post(INDEX_URL, params={'a': 'stealfuel'}, data={'truck': truck_id})
    print(r)


def wait_the_delay(company_id):
    # sleep until next try
    delay = get_timeout(company_id)
    log.info(f'will wait for {delay} seconds')
    time.sleep(delay)


def main() -> int:
    cid = company_id_gen()
    for company_id in cid:
        # if the script started manually in between waits, wait
        wait_the_delay(company_id)
        try:
            for truck_id in company_truck_gen(company_id):
                steal_fuel(truck_id)
                wait_the_delay(company_id)
        except Exception as e:
            log.exception()
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
