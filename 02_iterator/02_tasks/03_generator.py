"""
У каждого фильма есть расписание, по каким дням он идёт в кинотеатрах.

Для эффективности дни проката хранятся периодами дат.

Например, прокат фильма проходит с 1 по 7 января, а потом показ возобновляется с 15 января по 7 февраля:
[(datetime(2020, 1, 1), datetime(2020, 1, 7)), (datetime(2020, 1, 15), datetime(2020, 2, 7))]
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator, List, Tuple


@dataclass
class Movie:
    title: str
    dates: List[Tuple[datetime, datetime]]

    def schedule(self) -> Generator[datetime, None, None]:
        for current_dates in self.dates:
            choice_date, end_date = current_dates
            while choice_date <= end_date:
                yield choice_date
                choice_date = choice_date + timedelta(days=1)


m = Movie('sw', [
    (datetime(2020, 1, 1), datetime(2020, 1, 7)),
    (datetime(2020, 1, 15), datetime(2020, 2, 7))
])

for d in m.schedule():
    print(d)
