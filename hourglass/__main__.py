import asyncio

from .core import CronJob
from datetime import datetime
from pytz import timezone


async def main():
    cron = CronJob("* * * * * */30", time_zone="America/Denver")
    for i in range(40):
        print(f"i: {i}")
        await cron.next()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
