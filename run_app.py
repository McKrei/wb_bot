import time
from multiprocessing import Process

import asyncio
from aiogram.utils import executor
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers import register_all_handlers
from bot.mes import bot
from parser.main import start_parsing
from db.exec_db import run_db


async def create_or_delete_db():
    await run_db()


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_handlers(dp)


def runbot():
    # asyncio.run(create_or_delete_db())
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)


def checking_goods():
    while True:
        start = time.time()
        asyncio.get_event_loop().run_until_complete(start_parsing())
        print(f'Парсинг занял: {time.time() - start:.2f} сек')
        time.sleep(3600)


def main(param_proc_list):
    param_proc_dict = {i: par for i, par in enumerate(param_proc_list)}
    proc_dict = {i: Process(**param) for i, param in param_proc_dict.items()}

    while True:
        for id, proc in proc_dict.items():
            if not proc.is_alive():
                param = param_proc_dict[id]
                proc_dict[id] = Process(**param_proc_dict[id])
                proc_dict[id].start()
        time.sleep(60)


if __name__ == "__main__":
    main(param_proc_list = [{'target' : runbot}, {'target' : checking_goods}])


# if __name__ == '__main__':
#     runbot()
