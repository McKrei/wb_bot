import re

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from bot.keyboards import only_menu
from db import exec_db
from parser.main import get_query_data
from bot.mes import run_dop_async
from misc import create_line_query


async def get_start(msg: Message):
    await msg.answer(
        'Привет, пришли мне НМ ; человеческий запрос\nА я буду переодически проверять их!',
        reply_markup=only_menu)


async def deleted_query(msg: Message):
    user = msg.from_user.id
    id = int(msg.text[5:])
    q = await exec_db.get_query(id)
    if q:
        if q[0].user_id == user:
            await exec_db.deleted_query(id)
            return await msg.answer(f'Удалил запрос {id}',
                reply_markup=only_menu)
    await msg.answer('НЕТ!',
                reply_markup=only_menu)


async def get_user_query(msg: Message):
    create_mes = lambda l: '\n'.join([
        f'{i+1}) {create_line_query(q)}'
        for i, q in enumerate(l)])
    user = msg.from_user.id
    resp = await exec_db.get_users_query(user)
    for mes, queries in zip(
        ('Запросы в работе:\n', 'НМ нашел по запросу:\n'),
        resp):
        record = create_mes(queries)
        if record:
            await msg.answer(mes + record, reply_markup=only_menu)


async def writing_query(msg: Message):
    block = msg.text.split(';')
    user = msg.from_user.id
    if len(block) != 2:
        return await msg.answer(
            f'Не понял сообщения, нужно разделить НМ и запрос ";" \nпример: 110849880;электробритва',
            reply_markup=only_menu)

    nm, query = map(lambda x: x.strip(), block)
    if not nm.isdigit():
        return await msg.answer(
            f'НМ должна быть первой и состоять только из чисел\nпример: 110849880;электробритва',
            reply_markup=only_menu)

    q = await exec_db.create_query(user, nm, query)
    await msg.answer(
        f'Добавил\nЗапрос : {query}\nNM : {nm}\n/del_{q.id}',
        reply_markup=only_menu)
    await get_query_data(q)



def register_all_handlers(dp: Dispatcher):
    dp.register_message_handler(get_start, commands=['start'])
    dp.register_message_handler(deleted_query , Text(startswith='/del_'))
    dp.register_message_handler(get_user_query, Text(equals='Мои запросы'))

    dp.register_message_handler(writing_query, content_types=['text'])
