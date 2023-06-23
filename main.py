import logging
import re

from requests_html import HTMLSession

from config import AJAX_URL
from config import ENV
from config import setup_logging

setup_logging()
log = logging.getLogger(__name__)


class LTAgent:
    def __init__(self):
        # session details
        self.session = HTMLSession()
        self.session.user_token = self.token = None  # session will carry token for further use
        self.session.headers.update({
            "Accept": "*/*",
            "Accept-Encoding": "br,deflate,gzip,x-gzip",
            "Accept-Language": "cs,en;q=0.9,sk;q=0.8",
            "Dnt": "1",
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        })
        self.session.headers.update({'Cookie': ENV['LT_COOKIE']})

        # game details
        self.active_freights: list[Freight] = []

        log.debug('agent prepared')

    def _load_token(self) -> None:
        log.info('getting token')
        freight_id = self.active_freights[0]._id
        r = self.session.get(f'https://www.logitycoon.com/eu1/index.php?a=freight&n={freight_id}')
        self.token = self.session.user_token = int(re.findall(r'token: "(\d+)"', r.text)[0])

    def get_trip_id(self) -> int:
        log.info('choosing best trip')
        r = self.session.get('https://www.logitycoon.com/eu1/index.php?a=trips')
        row = r.html.find('input[name="freight[]"]')
        return int(row[0].attrs['value'])

    def accept_trip(self, trip_id: int) -> None:
        """Accept the trip by ID.

        Performs a post request.
        """
        log.info(f'accepting trip {trip_id}')
        self.session.post(f"{AJAX_URL}trip_accept.php", data={'freight[]': trip_id})

    def _read_freight_ids(self) -> list[int]:
        r = self.session.get('https://www.logitycoon.com/eu1/index.php?a=warehouse')
        rows = r.html.find('table:first-of-type tr[onclick]')
        return list(map(int, (re.findall(r'\d+', row.attrs['onclick'])[0] for row in rows)))

    def create_freights(self) -> None:
        self.active_freights = [
            Freight(num, self.session)
            for num in self._read_freight_ids()
        ]
        self._load_token()

    @property
    def car_count(self) -> int:
        # NOTE: so far only counts the number of cars
        r = self.session.get('https://www.logitycoon.com/eu1/index.php?a=garage')
        return len(r.html.find('.mt-action-details')) // 2


def main() -> int:
    log.info(' START '.center(80, '='))

    lt = LTAgent()

    best_trip_id = lt.get_trip_id()
    for _ in range(lt.car_count):
        lt.accept_trip(best_trip_id)

    lt.create_freights()

    for freight in lt.active_freights:
        freight.assign_assets()
        # TODO: go through freight stages
        freight.start_loading()

    # NOTE: find a way to make this async maybe

    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    raise SystemExit(main())
