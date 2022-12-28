from typing import Tuple

import asyncio
import aiohttp
from fake_useragent import UserAgent

from db.exec_db import get_all_active_query
from bot.mes import deactivate_task
from misc import param_is_in_issue
from db.models import Query


async def _is_in_issue(
        query: Query, brandID: int, subjectID: int, headers: dict
        ) -> Tuple[bool, str]:
    '''
    Пробегаю по страницам сайта(АPI) фильтруем по сабжекту и бренду
    собираю нм со страницы и ищу нашу.
    Возвращаю булиан как результат и сообщение где нашел (если нашел)
    '''
    params = param_is_in_issue.copy()
    params['xsubject'] = subjectID
    params['fbrand'] = brandID
    params['query'] = query.query
    URL ='https://search.wb.ru/exactmatch/ru/common/v4/search?'
    page = 1
    mes = ''
    while True:
        params['page'] = page
        async with aiohttp.request(
            'GET', URL, headers=headers, params=params
            ) as resp:
            if resp.status != 200:
                return False, None
            json = await resp.json(content_type=None)
            products = json.get('data', {}).get('products')
            if not products:
                return False, None
            id_list = [p.get('id') for p in products if p.get('id')]
            if int(query.nm) in id_list:
                point = ((page -1) * 100) + (id_list.index(int(query.nm)) + 1)
                search = query.query.replace(" ", "+")
                mes += f'Есть в выдаче на {point} месте'
                mes += f'\nURL https://www.wildberries.ru/catalog/0/search.aspx?page={page}&sort=popular&search={search}'
                mes += f'&xsubject={subjectID}&fbrand={brandID}'
                return True, mes
            page += 1


async def _get_nm_info(nm: int) -> tuple:
    '''
    Принимаю НМ, по ручки 85 забираю BrandID и SubjectID,
    либо ошибку если не получилось
    '''
    url = f'http://director-nm-holders.wbx-search-decision.svc.k8s.wbxsearch-dp/api/v1/get-nm?nmid={nm}'
    async with aiohttp.request('GET', url) as resp:
        if resp.status == 200:
            json = await resp.json(content_type=None)
            brandID = json.get('BrandID')
            subjectID = json.get('SubjectID')
            return brandID, subjectID
        return None, None


async def get_query_data(query: Query, headers=None) -> None:
    '''
    Получаем квери и хедерс для реквеста,
    и пробуем проверить наличие НМ на сайте
    если НМ есть возвращаем ответ и отключаем запрос,
    если НМ неверная отключаем запрос и сообщаем пользователю
    '''
    if not headers:
        headers = {"user-agent": UserAgent().random}
    brandID, subjectID = await _get_nm_info(query.nm)
    if not brandID or not subjectID:
        return await deactivate_task(
            query, 'Не получилось достать brandID и subjectID')
    result, mes = await _is_in_issue(query, brandID, subjectID, headers)
    if result:
        return await deactivate_task(
            query, mes)


async def start_parsing() -> None:
    '''
    Берем все запросы которые активны и составляем
     список задач который передаем на парсинг
    '''
    headers = {"user-agent": UserAgent().random}
    query_list = await get_all_active_query()
    tasks = []
    for query in query_list:
        task = asyncio.create_task(
            get_query_data(query, headers))
        tasks.append(task)
    print(len(tasks), 'Запросов')
    await asyncio.gather(*tasks) # Запускаем асинхронку
