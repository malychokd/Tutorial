import asyncio
import logging
import websockets
import names
import aiofile
import aiopath
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from get_exchange_PB import get_exchange

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.startswith("exchange"):
                sentences = message.split(" ")
                try:
                    n_days = int(sentences[1])
                except:
                    n_days = 0
                try:
                    currency_code = sentences[2].upper()
                except:
                    currency_code = 'USD'
                message_exchange = await get_exchange(n_days, currency_code)

                 # Записуємо лог до файлу
                async with aiofile.async_open('exchange_log.txt', mode='a') as log_file:
                    await log_file.write(f'name: {ws.name}, message: {message}, message_exchange: {message_exchange}\n')

                await self.send_to_clients(message_exchange)
            else:    
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())