import sys
import platform
from datetime import datetime, timedelta
import logging

import aiohttp
import asyncio

async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    r = await resp.json()
                    return r
                logging.error(f"Error status: {resp.status} for {url}")
                return None
        except aiohttp.ClientConnectorError as err:
            logging.error(f"Connection error: {str(err)}")
            return None


async def get_exchange(n_days, currency_code='USD'):
    if n_days > 10:
        n_days = 10
    #result = await request('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
    current_datetime = datetime.now() - timedelta(days=int(n_days))
    result = await request(f"https://api.privatbank.ua/p24api/exchange_rates?date={current_datetime.date().strftime('%d.%m.%Y')}")
    if result:
        rates = result.get('exchangeRate')
        exc, = list(filter(lambda el: el["currency"] == currency_code, rates))
        return f"{currency_code}: buy: {exc['purchaseRateNB']}, sale: {exc['saleRateNB']}. Date: {current_datetime.date()}"
    return "Failed to retrieve data"


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        n_days = int(sys.argv[1])
    except:
        n_days = 0
    try:
        currency_code = sys.argv[2].upper()
    except:
        currency_code = 'USD'
    result = asyncio.run(get_exchange(n_days, currency_code))
    print(result)

