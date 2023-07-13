import datetime
import itertools
import logging
import re

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
            'level': 'INFO',
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
    r = web.get(INDEX_URL, params={'a': 'companylist', 'p': page_num})
    id_matches = re.findall(
        r'href="index\.php\?a\=companyprofile_overview&x=(\d+)"',
        r.text
    )[::3]  # we need to take every third, because every row has 3 links
    yield from map(int, id_matches)


def company_id_gen(start_page: int = 30, end_page: int = 40):
    yield from itertools.chain.from_iterable(
        page_company_ids(page) for page in range(start_page, end_page)
    )


def company_truck_gen(company_id: int):
    """given company id, yield unprotected truck ids"""
    r = web.get(INDEX_URL, params={'a': 'companyprofile_trucks', 'x': company_id})
    buttons = r.html.find('.tab-content button:not([disabled])')
    truck_ids = (button.attrs['value'] for button in buttons)
    yield from map(int, truck_ids)


def get_timeout(company_id: int):
    """Look for text: "Stealing fuel is available again at 13-07-2023 18:12." """
    r = web.get(INDEX_URL, params={'a': 'companyprofile_trucks', 'x': company_id})

    pattern = r'Stealing fuel is available again at (\d+-\d+-\d+ \d+:\d+)'
    if match := re.findall(pattern, r.text):
        next_time = datetime.datetime.strptime(match[0], '%d-%m-%Y %H:%M')
        delta = next_time - datetime.datetime.now()
        return delta.seconds
    return 3  # NOTE: by default sleep for 3 seconds between tries


def steal_fuel(truck_id: int):
    r = web.post(
        INDEX_URL,
        params={'a': 'stealfuel'},
        data={'truck': truck_id},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print(r)


cid = company_id_gen()

while True:
    cmp_id = next(cid)
    ctg = company_truck_gen(cmp_id)
    trucks = list(ctg)
    print(trucks)
