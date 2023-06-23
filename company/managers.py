import logging

from company.warehouse import Freight

log = logging.getLogger(__name__)


class FreightManager:

    def __init__(self, game):
        self.game = game
        self.active_freights: set[Freight] = set()

        log.debug('freight manager ready')

    def get_trip_id(self) -> int:
        log.info('choosing best trip')
        return self.game.interface.get_trip_id()

    def accept_trip(self, trip_id: int) -> None:
        log.info(f'accepting trip {trip_id}')
        self.game.interface.accept_trip(trip_id)

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
