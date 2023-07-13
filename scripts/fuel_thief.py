import logging

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

r = web.get(INDEX_URL, params={'a': 'trips'})

log.info(r.status_code)
