import logging
import re

from requests_html import HTMLSession

from config import AJAX_URL
from config import ENV
from config import INDEX_URL
from interfaces.base import Interface

log = logging.getLogger(__name__)


class WebInterface(Interface):

    def __init__(self) -> None:
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

    def load_token(self, freight_id: int) -> int:
        log.debug('loading token')
        r = self.session.get(INDEX_URL, params={'a': 'freight', 'n': freight_id})
        token = int(re.findall(r'token: "(\d+)"', r.text)[0])
        self.session.user_token = token
        return token

    def get_trip_id(self) -> int:
        """Choose the best available.

        Choose the first best one.
        Trips are available only for free trucks.  TODO: check this

        example:
            AaaaaBbbCc -> A
            BbbCc -> B
        """
        r = self.session.get(INDEX_URL, params={'a': 'trips'})
        row = r.html.find('input[name="freight[]"]')
        return int(row[0].attrs['value'])

    def accept_trip(self, trip_id: int) -> None:
        self.session.post(f"{AJAX_URL}trip_accept.php", data={'freight[]': trip_id})
