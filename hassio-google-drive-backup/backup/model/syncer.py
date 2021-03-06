from typing import List

from injector import inject, singleton

from .coordinator import Coordinator
from ..time import Time
from ..worker import Worker, Trigger
from ..logger import getLogger

logger = getLogger(__name__)


@singleton
class Scyncer(Worker):
    @inject
    def __init__(self, time: Time, coord: Coordinator, triggers: List[Trigger]):
        super().__init__("Sync Worker", self.checkforSync, time, 0.5)
        self.coord = coord
        self.triggers: List[Trigger] = triggers
        self._time = time

    async def checkforSync(self):
        doSync = False
        for trigger in self.triggers:
            if trigger.check():
                logger.debug("Sync requested by " + str(trigger.name()))
                doSync = True
        if doSync:
            while self.coord.isSyncing():
                await self._time.sleepAsync(3)
            await self.coord.sync()
