from db.exec_db import update_activity_false
from aiogram import Bot
from env import TOKEN
from misc import create_line_query

bot = Bot(token=TOKEN, parse_mode='HTML')

async def deactivate_task(query, mes):
    await update_activity_false(query.id)
    await bot.send_message(
        query.user_id,
        f'{create_line_query(query)}\n{mes}')


async def run_dop_async(func, kwargs):
    bot.register_next_step_handler(asyncio.run(func))
