import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(filename)s:%(lineno)d "
           "[%(asctime)s] - %(name)s - %(message)s",
)

from bot import start_bot
import asyncio
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_bot())
