import asyncio

from .core import foo

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(foo())
    finally:
        loop.close()
