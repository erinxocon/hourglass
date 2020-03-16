import asyncio
import time
import uuid
from datetime import datetime

from croniter.croniter import croniter
from pytz import timezone

# Types

EventLoop = asyncio.AbstractEventLoop
TimerHandle = asyncio.TimerHandle
Future = asyncio.Future


async def t():
    now = datetime.now(tz=timezone("America/Denver"))
    print(f"hello world! @ {now.strftime('%T%t%f')}")


class CronJob:
    def __init__(self, cron_expr: str, /, loop: EventLoop = None, time_zone: str = None,) -> None:
        # populate from args and kwargs
        self.cron_expr = cron_expr
        self.time_zone = timezone("UTC") if time_zone is None else timezone(time_zone)
        self.loop = loop if loop is not None else asyncio.get_event_loop()

        # set some initial things
        self.uuid = uuid.uuid4()
        self.croniter: croniter = None
        self.timer_handle: TimerHandle = None
        self.future: Future = None

        # these won't show up until you call init_croniter but I wanna type them
        self.datetime: datetime
        self.time: float
        self.loop_time: float

    def init_croniter(self) -> None:
        if self.croniter is None:
            self.time = time.time()
            self.datetime = datetime.now(self.time_zone)
            self.loop_time = self.loop.time()
            self.croniter = croniter(self.cron_expr, start_time=self.datetime)

    def callback(self) -> None:
        asyncio.gather(t(), return_exceptions=True).add_done_callback(self.resolve_future)

    async def next(self) -> Future:
        self.init_croniter()
        self.future = self.loop.create_future()
        next_time = self.get_next_loop_time()
        print(f"Next: {next_time}")
        self.timer_hande = self.loop.call_at(next_time, self.callback)
        print(
            f"About to await the future @ {datetime.now(tz=timezone('America/Denver')).strftime('%T%t%f')}"
        )
        return await self.future

    def get_next_loop_time(self) -> float:
        next_cron_time = self.croniter.get_next(float)
        return self.loop_time + (next_cron_time - self.time)

    def resolve_future(self, result) -> None:
        result = result.result()[0]
        if self.future is not None:
            if isinstance(result, Exception):
                self.future.set_exception(result)
            else:
                self.future.set_result(result)
            self.future = None
        elif isinstance(result, Exception):
            raise result
